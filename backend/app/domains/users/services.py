from fastapi import HTTPException

from typing import List, Type
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

import jwt

from app.domains.users.models import Usuario
from app.domains.users.schemas import UserUpdate

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


def create_user_service(
        session: Session,
        nome: str,
        telefone: str,
        email: str,
        senha: str,
        role: str
):
    """ Service Create Usuário """

    if unique_email(session, email):
        raise HTTPException(400, "Email já cadastrado")

    hashed_senha = get_password_hash(senha)    ## Função de app/core/security.py para pegar senha com hash

    # Criação de objeto Usuario com os dados vindos dos parametros de entrada da função
    user = Usuario(
        email=email,
        senha=hashed_senha,
        nome=nome,
        telefone=telefone,
        role=role
    )

    try:
        return create_user_in_db(session, user)

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=400,
            detail="Email ja cadastrado"
        )


def authenticate_user(session: Session, email: str, senha: str):
    """ Service que verifica autenticação do Usuario """

    user = get_user_by_email(session, email)                ## Verificando se o Usuario existe pelo email por função de repository

    if not user:
        return None

    if not verify_password(senha, user.senha):              ## Função de verificação de senha de app/core/security.py
        return None

    return user                                             # Se 'email' existe e 'senha' verificada retorna usuario autenticado


def login_service(session: Session, email: str, senha: str):
    """ Service de login """

    user = get_user_by_email(session, email)                ## Verificando se o Usuario existe pelo 'email' por função de repository

    if not user or not verify_password(senha, user.senha):
        raise HTTPException(
            status_code=401,
            detail="Email ou senha incorretos"
        )

    acces_token = create_access_token(user)                 # Se houver 'email' e senha verificada, cria um 'token' de acesso para 'user'

    return {                                                # retorna tupla com 'token'
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


def update_user_service(session: Session, user_id: int, user_up: UserUpdate):
    """ Service para atualizar Usuario"""

    user = get_user_by_id(session, user_id)  ## Verificando se o Usuario existe no banco

    if not user:                             ## Se o Usuario já existir no banco logo não vai ser criado o objeto 'user', então lança a Exception
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    if user_up.senha:
        user_up.senha = get_password_hash(user_up.senha)  ## Criando o hash do Usuario

    for chave, valor in user_up.dict(exclude_unset=True).items():
        setattr(user, chave, valor)

    return update_user_in_db(session, user)


def delete_user_service(session: Session,user_id: int) -> None:
    """ Service de deletar usuário """

    user = get_user_by_id(session, user_id)  ## Verificando se o Usuario existe no banco

    if not user:  ## Se o Usuario já existir no banco logo não vai ser criado o objeto 'user', então lança a Exception
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    if user.role == "superuser":
        raise HTTPException(
            status_code=403,
            detail="Somente um Super Usuário pode deletar outro Super Usuário"
        )

    return delete_user_in_db(session, user)
