from fastapi import Depends, HTTPException

from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordBearer

from app.core.db import get_session

from app.domains.users.models import Usuario
from app.domains.users.enums import UserRole

from app.domains.users.services import get_current_user_service

from app.domains.users.repository import UsuarioRepository
from app.domains.professionals.medico.repository import MedicoRepository
from app.domains.professionals.secretaria.repository import SecretariaRepository
from app.domains.professionals.medico.medico_esp.repository import MedicoEspRepository
from app.domains.professionals.medico.especialidade.repository import EspecialidadeRepository


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")   #muda aqui


def get_user_repo():
    """ Função para injetar dependência de Repositório """

    return UsuarioRepository()


def get_secretaria_repo():
    """ Função para injetar dependência de Repositório """

    return SecretariaRepository()


def get_medico_repo():
    """ Função para injetar dependência de Repositório """

    return MedicoRepository()


def get_esp_repo():
    """ Função para injetar dependência de Repositório """

    return EspecialidadeRepository()


def get_med_esp_repo():
    """ Função para injetar dependência de Repositório """

    return MedicoEspRepository()


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


