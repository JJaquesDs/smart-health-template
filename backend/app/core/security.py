import bcrypt

from datetime import datetime, timedelta, timezone
from typing import Any

import jwt

from app.core.config import settings

ALGORITHM = "HS256"


def create_access_token(user):
    """ Função que cria um ‘token’ de acesso para 'usuários """

    expiracao = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": str(user.usuario_id),
        "role": user.role,
        "exp": expiracao
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)  # Encode do token com a SecretKey e o algoritmo de encode
    return token


def verify_password(senha_simples: str, senha_hashed: str) -> bool:
    """ Função que verifica as senhas"""

    return bcrypt.checkpw(senha_simples.encode("utf-8"), senha_hashed.encode("utf-8"))  # Enconding de senhas em bytes para utf-8


def get_password_hash(senha: str) -> str:
    """ Função que pega a senha e faz hash (usando bcrypt) """

    hashed = bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt())  ## transformando em bytes para bcrypt trabalhar

    return hashed.decode("utf-8")  ## Devolvendo como utf-8

