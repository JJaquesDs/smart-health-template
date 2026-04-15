from fastapi import HTTPException

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

import jwt

import traceback

from app.domains.users.models import Usuario
from app.domains.users.enums import UserRole
from app.domains.users.schemas import UserUpdate

from app.domains.users.repository import UsuarioRepository

from app.core.config import settings

from app.core.security import (
    get_password_hash, verify_password,
    create_access_token,
    ALGORITHM
)

from app.core.exceptions.user_exceptions import (
    EmailExistenteException,
    UsuarioNaoAutorizadoException,
    UsuarioNaoEncontradoException
)


def create_user_service(
        session: Session,
        user_repo: UsuarioRepository,
        nome: str,
        telefone: str,
        email: str,
        senha: str,
        role: UserRole,
        usuer_atual: Usuario | None = None
):
    """ Service Create Usuário """

    # Regra de endereço eletrónico único
    unique_email(session, email, user_repo)

    #  Regra de permissão de criacão
    if role in {UserRole.ADMIN, UserRole.SUPERUSER}:  ## Se quem tentar criar um 'admin' ou um 'superuser' e não tiver esses roles ou não for um 'Usuario' não tem permissão
        if not usuer_atual or usuer_atual.role != UserRole.SUPERUSER:  ## Essa verificação só é feita no service caso ele seja importado e outro dev esquecer de usar função exigir_role()
            raise UsuarioNaoAutorizadoException("Você não tem permissão para criar esse usuário")

    # Função para criar senha com hash
    hashed_senha = get_password_hash(senha)

    # Criação de objeto Usuario com os dados vindos dos parametros de entrada da função
    user = Usuario(
        email=email,
        senha=hashed_senha,
        nome=nome,
        telefone=telefone,
        role=role
    )

    # Garantindo do banco o 'usario_id' por ser autoincrement
    session.flush()

    # Persiste os dados, mas ainda não envia pro banco (dando commit())
    return user_repo.create(session=session, obj_input=user)


def is_admin_or_superuser(user: Usuario) -> bool:
    """ Função só para verificar se Usuario é admin ou 'Superuser' comparando com um bool com os roles """

    return user.role in {UserRole.ADMIN, UserRole.SUPERUSER}


def authenticate_user(
        session: Session,
        email: str,
        senha: str,
        user_repo: UsuarioRepository
):
    """ Service que verifica autenticação do Usuario (SEM USO NO MOMENTO)"""

    # Verificando se o Usuario existe pelo 'email' por função de repository
    user = unique_email(session=session, email=email, user_repo=user_repo)

    if not user:
        return None

    # Função de verificação de senha de 'app/core/security.py'
    if not verify_password(senha, user.senha):
        return None

    return user  # Se 'email' existe e 'senha' verificada retorna usuario autenticado


def login_service(
        session: Session,
        email: str,
        senha: str,
        user_repo: UsuarioRepository
):
    """ Service de login """

    # Verificando se o Usuario existe pelo 'email' por função de repository
    user = user_repo.get_by_email(session, email)

    if not user or not verify_password(senha, user.senha):
        raise UsuarioNaoEncontradoException("Usuário não encontrado no sistema")

    # Se houver 'email' e senha verificada, cria um 'token' de acesso para 'user'
    acces_token = create_access_token(user)

    return {  # retorna tupla com 'token'
        "access_token": acces_token,
        "token_type": "bearer"
    }


def get_current_user_service(
        session: Session,
        token: str,
        user_repo: UsuarioRepository
) -> Usuario:
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

    user = user_repo.get_one_by_campo(session=session, campo=Usuario.usuario_id, valor=user_id)

    if not user:
        raise UsuarioNaoEncontradoException("Usuário não encontrado no sistema")

    return user


def unique_email(
        session: Session,
        email: str,
        user_repo: UsuarioRepository
):
    """ Service para verificar e-mail único """

    user = user_repo.get_by_email(session=session, email=email)

    if user:
        raise EmailExistenteException("Email já cadastrado")


def get_all_users_service(
        session: Session,
        user_repo: UsuarioRepository
) -> list[Usuario]:
    """ Service para listar Usuarios"""

    return user_repo.get_all(session)


def update_user_service(
        session: Session,
        user_atual: Usuario,
        user_id: int,
        user_up: UserUpdate,
        user_repo: UsuarioRepository
):
    """ Service para atualizar Usuario"""

    # Verificando se o Usuario existe no banco
    user = user_repo.get_or_not_found(
        session=session,
        campo=Usuario.usuario_id,
        valor=user_id,
        exception=UsuarioNaoEncontradoException("Usuário não encontrado no sistema")
    )

    # Regra de permissão: verificação que não permite atualizar um admin ou 'superuser' a não ser 'superusers'
    if is_admin_or_superuser(user) and not is_admin_or_superuser(user_atual):
        raise UsuarioNaoAutorizadoException("Você não tem permissão para atualizar esse usuário")

    # Criação de senha hash para 'Usuario' (caso ele altere)
    if user_up.senha:
        user_up.senha = get_password_hash(user_up.senha)

    # Atualização dos dados
    for chave, valor in user_up.model_dump(exclude_unset=True).items():
        setattr(user, chave, valor)

    return user_repo.update(session=session, obj_input=user)


def delete_user_service(
        session: Session,
        user_atual: Usuario,
        user_id: int,
        user_repo: UsuarioRepository
) -> None:
    """ Service de deletar usuário """

    # Verificando se o 'Usuario' existe no banco
    user = user_repo.get_or_not_found(
        session=session,
        campo=Usuario.usuario_id,
        valor=user_id,
        exception=UsuarioNaoEncontradoException("Usuário não encontrado no sistema")
    )

    # Regra de permissão
    if is_admin_or_superuser(user) and not is_admin_or_superuser(user_atual):  ## Verificação que não permite atualizar um admin ou 'superuser' a não ser 'superusers'
        raise UsuarioNaoAutorizadoException("Você não tem permissão para deletar esse usuário")

    return user_repo.delete(session=session, obj_model=user)
