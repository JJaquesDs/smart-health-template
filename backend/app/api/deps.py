from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.db import get_session

from app.domains.users.models import Usuario
from app.domains.users.enums import UserRole

from app.domains.users.services import get_current_user_service


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")   #muda aqui


def get_current_user_dep(
        token: str = Depends(oauth2_scheme),
        session: Session = Depends(get_session)
):
    """ Função que verifica 'Usuario' por 'token' e se existe """

    return get_current_user_service(session, token)


def exigir_role(roles: list[UserRole]):
    """ Função que exige um papel para permissão de 'Usuario' """

    def checar(usuario_atual: Usuario = Depends(get_current_user_dep)):
        """ Dentro de exigir possui a função que checa se o papel está presente em papéis """

        if usuario_atual.role not in roles:
            raise HTTPException(
                status_code=403,
                detail="Usuário sem permissão"
            )

        return usuario_atual  # Retorna usuario atual ou excessão para a função 'exigir_role()'
    return checar             # Que retorna a o dado de 'checar()'


