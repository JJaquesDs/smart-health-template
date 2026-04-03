from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.api.deps import get_current_user_dep, exigir_role, get_session

from app.domains.users.models import Usuario
from app.domains.users.schemas import UserPublic, UserCreate

from app.domains.users.services import create_user_service

router = APIRouter(prefix="/admin", tags=['admin'])


@router.post("/", response_model=UserPublic)
def create_admin(
        admin_novo: UserCreate,
        session: Session = Depends(get_session),
        usuario_atual: Usuario = Depends(exigir_role(["superuser"]))
):
    """ Rota para criar 'admins' (somente 'Superusuário') """

    return create_user_service(
        session=session,
        nome=admin_novo.nome,
        telefone=admin_novo.telefone,
        email=admin_novo.email,
        senha=admin_novo.senha,
        role="admin"
    )


@router.get("/area", response_model=UserPublic)
def admin_area(user: Usuario = Depends(exigir_role(["admin", "superuser"]))):
    """ Rota protegida que exige papel admin """

    return user
