from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.api.deps import (
    get_session,
    get_current_user_dep,
    exigir_role
)

from app.domains.users.models import Usuario
from app.domains.users.enums import UserRole

from app.domains.professionals.secretaria.schemas import (
    SecretariaPublic,
    SecretariaCreate,
    SecretariaUpdate
)

from app.domains.professionals.secretaria.services import (
    create_secretaria_service
)


router = APIRouter(prefix="/secretaria", tags=["secretarias"])


@router.post(path="/",
             response_model=SecretariaPublic,
             summary="Criar secretária",
             description="Cria um usuário secretária com role 'secretaria'"
)
def create_secretaria_route(
        user: SecretariaCreate,
        session: Session = Depends(get_session)
):
    """ Rota para criar secretárias """

    secretaria = create_secretaria_service(
        session=session,
        nome=user.nome,

    )