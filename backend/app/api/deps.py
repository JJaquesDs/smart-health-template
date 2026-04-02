from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

import jwt

from app.core.config import settings
from app.core.db import get_session

from app.domains.users.models import Usuario

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")   #muda aqui


def get_current_user(token: str = Depends(oauth2_scheme),
                     session: Session = Depends(get_session)
):
    """ Função que verifica usuário por token e se existe """

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = int(payload.get("sub"))

        if not user_id:
            raise HTTPException(status_code=401, detail="Token inválido")

    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    user = session.query(Usuario).filter_by(usuario_id=user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user


def exigir_role(roles: list[str]):
    """ Função que exige um papel para permissão de usuários """

    def checar(usuario_atual: Usuario = Depends(get_current_user)):
        """ Função que checa se o papel está presente em papéis"""

        if usuario_atual.role not in roles:
            raise HTTPException(
                status_code=403,
                detail="Usuário sem permissão"
            )

        return usuario_atual
    return checar


