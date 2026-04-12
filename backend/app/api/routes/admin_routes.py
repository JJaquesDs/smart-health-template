from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.api.deps import get_current_user_dep, exigir_role, get_session

from app.domains.users.models import Usuario
from app.domains.users.schemas import UserPublic, UserCreate
from app.domains.users.enums import UserRole

from app.domains.users.services import create_user_service

router = APIRouter(prefix="/admin", tags=['admin'])


@router.post("/", response_model=UserPublic)
def create_admin(
        admin_novo: UserCreate,
        session: Session = Depends(get_session),
        user_atual: Usuario = Depends(exigir_role([UserRole.SUPERUSER]))
):
    """ Rota para criar 'admins' (somente 'Superusuário') """

    try:
        with session.begin():
            return create_user_service(
                session=session,
                nome=admin_novo.nome,
                telefone=admin_novo.telefone,
                email=admin_novo.email,
                senha=admin_novo.senha,
                role=UserRole.ADMIN,
                usuer_atual=user_atual
            )
    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Erro ao criar Usuário administrador"
        )


@router.get("/current_admin_area", response_model=UserPublic)
def admin_area(user: Usuario = Depends(exigir_role([UserRole.ADMIN, UserRole.SUPERUSER]))):
    """ Rota protegida que exige papel admin """

    return user
