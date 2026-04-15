from fastapi import HTTPException

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

import jwt

import traceback

from app.domains.users.models import Usuario
from app.domains.users.schemas import UserUpdate
from app.domains.users.enums import UserRole

from app.core.config import settings

from app.core.security import (
    get_password_hash, verify_password,
    create_access_token,
    ALGORITHM
)

from app.domains.users.repository import (
    get_user_by_id,
    get_user_by_email,
    create_user_in_db,
    delete_user_in_db,
    update_user_in_db,
    get_all_users_in_db
)


PROFESSIONAL_ROLES = {UserRole.ADMIN, UserRole.MEDICO}


def validate_professional_profile(role: UserRole, payload: dict) -> None:
    """Valida os campos profissionais exigidos para perfis médicos e admins."""

    if role not in PROFESSIONAL_ROLES:
        return

    required_fields = (
        "registro_profissional",
        "especialidade_principal",
        "instituicao",
        "universidade",
        "ano_formacao",
        "residencia_medica",
    )
    missing_fields = [field_name for field_name in required_fields if payload.get(field_name) in (None, "")]

    if not payload.get("especializacoes"):
        missing_fields.append("especializacoes")

    if missing_fields:
        fields = ", ".join(missing_fields)
        raise HTTPException(
            status_code=400,
            detail=f"Campos profissionais obrigatórios para a role '{role}': {fields}"
        )


def can_bootstrap_superuser(session: Session, role: UserRole, user_atual: Usuario | None) -> bool:
    """Permite criar o primeiro superusuário durante a inicialização da aplicação."""

    if role != UserRole.SUPERUSER or user_atual is not None:
        return False

    existing_superuser = session.query(Usuario).filter_by(role=UserRole.SUPERUSER).first()
    return existing_superuser is None


def create_user_service(
        session: Session,
        nome: str,
        telefone: str,
        email: str,
        senha: str,
        role: UserRole,
        registro_profissional: str | None = None,
        especialidade_principal: str | None = None,
        instituicao: str | None = None,
        universidade: str | None = None,
        ano_formacao: int | None = None,
        residencia_medica: str | None = None,
        especializacoes: list[str] | None = None,
        usuer_atual: Usuario | None = None,
        allow_superuser_bootstrap: bool = False,
):
    """ Service Create Usuário """

    # Regra de endereço eletrónico único
    if unique_email(session, email):
        raise HTTPException(400, "Email já cadastrado")

    hashed_senha = get_password_hash(senha)  ## Função de app/core/security.py para criar senha com hash

    validate_professional_profile(
        role=role,
        payload={
            "registro_profissional": registro_profissional,
            "especialidade_principal": especialidade_principal,
            "instituicao": instituicao,
            "universidade": universidade,
            "ano_formacao": ano_formacao,
            "residencia_medica": residencia_medica,
            "especializacoes": especializacoes or [],
        }
    )

    # Criação de objeto Usuario com os dados vindos dos parametros de entrada da função
    user = Usuario(
        email=email,
        senha=hashed_senha,
        nome=nome,
        telefone=telefone,
        role=role,
        registro_profissional=registro_profissional,
        especialidade_principal=especialidade_principal,
        instituicao=instituicao,
        universidade=universidade,
        ano_formacao=ano_formacao,
        residencia_medica=residencia_medica,
        especializacoes=especializacoes or [],
    )

    # Garantindo do banco o 'usario_id' por ser autoincrement
    session.flush()

    #  Regra de permissão de criacão
    if role in {UserRole.ADMIN, UserRole.SUPERUSER}:  ## Se quem tentar criar um 'admin' ou um 'superuser' e não tiver esses roles ou não for um 'Usuario' não tem permissão
        if allow_superuser_bootstrap and can_bootstrap_superuser(session, role, usuer_atual):
            return create_user_in_db(session, user)

        if not usuer_atual or usuer_atual.role != UserRole.SUPERUSER:  ## Essa verificação só é feita no service caso ele seja importado e outro dev esquecer de usar função exigir_role()
            raise HTTPException(
                status_code=401,
                detail="Você não tem permissão para criar esse tipo de usuário"
            )

    # Persiste os dados, mas ainda não envia pro banco (dando commit())
    return create_user_in_db(session, user)


def is_admin_or_superuser(user: Usuario) -> bool:
    """ Função só para verificar se Usuario é admin ou 'Superuser' comparando com um bool com os roles """

    return user.role in {UserRole.ADMIN, UserRole.SUPERUSER}


def authenticate_user(session: Session, email: str, senha: str):
    """ Service que verifica autenticação do Usuario (SEM USO NO MOMENTO)"""

    user = get_user_by_email(session, email)  ## Verificando se o Usuario existe pelo email por função de repository

    if not user:
        return None

    if not verify_password(senha, user.senha):  ## Função de verificação de senha de app/core/security.py
        return None

    return user  # Se 'email' existe e 'senha' verificada retorna usuario autenticado


def login_service(session: Session, email: str, senha: str):
    """ Service de login """

    user = get_user_by_email(session, email)  ## Verificando se o Usuario existe pelo 'email' por função de repository

    if not user or not verify_password(senha, user.senha):
        raise HTTPException(
            status_code=401,
            detail="Email ou senha incorretos"
        )

    acces_token = create_access_token(user)  # Se houver 'email' e senha verificada, cria um 'token' de acesso para 'user'

    return {  # retorna tupla com 'token'
        "access_token": acces_token,
        "token_type": "bearer"
    }


def get_current_user_service(session: Session, token: str) -> Usuario:
    """ Service que valida token e retorna Usuario """

    exception_credenciais = HTTPException(
        status_code=401,
        detail="Token inválido",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])  ## ALGORITHM vindo de security
        user_id: str | None = payload.get("sub")

        if user_id is None:
            raise exception_credenciais

    except jwt.PyJWTError:
        raise exception_credenciais

    user = get_user_by_id(session, int(user_id))

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    return user


def unique_email(session: Session, email: str):
    """ Service para verificar e-mail único """

    if session.query(Usuario).filter_by(email=email).first():
        raise HTTPException(
            status_code=400,
            detail="Email já cadastrado"
        )


def get_all_users_service(session: Session) -> list[Usuario]:
    """ Service para listar Usuarios"""

    return get_all_users_in_db(session)


def update_user_service(
        session: Session,
        user_atual: Usuario,
        user_id: int,
        user_up: UserUpdate
):
    """ Service para atualizar Usuario"""

    user = get_user_by_id(session, user_id)  ## Verificando se o Usuario existe no banco

    # Se o Usuario já existir no banco logo não vai ser criado o objeto 'user', então lança a Exception
    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    # Regra de permissão
    if is_admin_or_superuser(user) and not is_admin_or_superuser(user_atual):  # Verificação que não permite atualizar um admin ou 'superuser' a não ser 'superusers'
        raise HTTPException(
            status_code=404,
            detail=" Você não tem autorização para atualizar esse Usuário "
        )

    # Criação de senha hash para 'Usuario' (caso ele altere)
    if user_up.senha:
        user_up.senha = get_password_hash(user_up.senha)

    update_data = user_up.model_dump(exclude_unset=True)
    final_role = update_data.get("role", user.role)
    merged_payload = {
        "registro_profissional": update_data.get("registro_profissional", user.registro_profissional),
        "especialidade_principal": update_data.get("especialidade_principal", user.especialidade_principal),
        "instituicao": update_data.get("instituicao", user.instituicao),
        "universidade": update_data.get("universidade", user.universidade),
        "ano_formacao": update_data.get("ano_formacao", user.ano_formacao),
        "residencia_medica": update_data.get("residencia_medica", user.residencia_medica),
        "especializacoes": update_data.get("especializacoes", user.especializacoes or []),
    }

    validate_professional_profile(role=final_role, payload=merged_payload)

    # Atualização dos dados
    for chave, valor in update_data.items():
        setattr(user, chave, valor)

    return update_user_in_db(session, user)


def delete_user_service(
        session: Session,
        user_atual: Usuario,
        user_id: int
) -> None:
    """ Service de deletar usuário """

    user = get_user_by_id(session, user_id)  ## Verificando se o Usuario existe no banco

    if not user:  ## Se o Usuario já existir no banco logo não vai ser criado o objeto 'user', então lança a Exception
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    # Regra de permissão
    if is_admin_or_superuser(user) and not is_admin_or_superuser(user_atual):  ## Verificação que não permite atualizar um admin ou 'superuser' a não ser 'superusers'
        raise HTTPException(
            status_code=403,
            detail=" Você não tem permissão para deletar esse Usuário "
        )

    return delete_user_in_db(session, user)
