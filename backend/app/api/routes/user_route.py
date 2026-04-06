from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.api.deps import get_current_user_dep, exigir_role, get_session

from app.domains.users.models import Usuario
from app.domains.users.schemas import UserPublic, UserCreate, UserUpdate
from app.domains.users.enums import UserRole

from app.domains.users.services import (
    create_user_service,
    login_service,
    update_user_service,
    delete_user_service,
    get_all_users_service
)

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/eu", response_model=UserPublic)
def read_usuario_atual(user: Usuario = Depends(get_current_user_dep)):
    """ Função read do usuario atual """

    return user


@router.post("/", response_model=UserPublic)
def create_user(user_novo: UserCreate, session: Session = Depends(get_session)):
    """ Rota para criar usuario """

    user = create_user_service(
        session=session,
        nome=user_novo.nome,
        telefone=user_novo.telefone,
        email=user_novo.email,
        senha=user_novo.senha,
        role=user_novo.role
    )

    return user


@router.post("/login")
def login(formulario: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    """ Rota login com Formulário OAuth2Password """

    return login_service(session, formulario.username, formulario.password)    ## OAuth2PasswordRequestForm lê 'username' como email, entende-se como parâmetros 'email' e 'senha'


@router.get("/list-todos", response_model=list[UserPublic])
def read_users(
        user: Usuario = Depends(exigir_role([UserRole.ADMIN, UserRole.SUPERUSER])),
        session: Session = Depends(get_session)
):
    """ Rota de listar 'Usuarios' (somente admin)"""

    return get_all_users_service(session)


@router.put("/{user_id}", response_model=UserPublic)
def update_user(
        user_id: int,
        user_up: UserUpdate,
        user_atual: Usuario = Depends(get_current_user_dep),
        session: Session = Depends(get_session)
):
    """ Rota para atualizar Usuario (exige admin e superuser) """

    return update_user_service(session, user_atual, user_id, user_up)


@router.delete("/{user_id}", status_code=204)
def delete_user(
        user_id: int,
        user_atual: Usuario = Depends(get_current_user_dep),
        session: Session = Depends(get_session),
):
    """ Rota para deletar Usuario (exige admin ou superuser)"""

    delete_user_service(session, user_atual, user_id)

    return {
        "message": "Usuário deletado com sucesso"
    }

