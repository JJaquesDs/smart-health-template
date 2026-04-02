from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from typing import List

from app.api.deps import get_current_user, exigir_role, get_session

from app.core.security import get_password_hash, verify_password, create_access_token

from app.domains.users.models import Usuario
from app.domains.users.schemas import UserPublic, UserCreate, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/eu", response_model=UserPublic)
def read_usuario_atual(user: Usuario = Depends(get_current_user)):
    """ Função read do usuario atual """

    return user


@router.post("/", response_model=UserPublic)
def create_user(user_novo: UserCreate, session: Session = Depends(get_session)):
    """ Rota para criar usuario """

    usuario_existente = session.query(Usuario).filter_by(email=user_novo.email).first()

    if usuario_existente:
        raise HTTPException(
            status_code=400,
            detail="Email já cadastrado"
        )


#  criando usuário caso nao esteja cadastrado
    user = Usuario(
        email=user_novo.email,
        senha=get_password_hash(user_novo.senha),
        nome=user_novo.telefone,
        telefone=user_novo.telefone,
        role=user_novo.role
    )

    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.post("/login")
def login(formulario: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    """ Rota login com Formulário OAuth2Password """

    user = session.query(Usuario).filter_by(email=formulario.username).first()

    if not user or not verify_password(formulario.password, user.senha):
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")

    access_token = create_access_token(user)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/list-todos", response_model=List[UserPublic])
def read_users(
        user: Usuario = Depends(exigir_role(["admin"])),
        session: Session = Depends(get_session)
):
    """ Rota de listar 'usuários' (somente admin)"""

    return session.query(Usuario).all()


@router.put("{user_id}", response_model=UserPublic)
def update_user(
        user_id: int,
        user_up: UserUpdate,
        session: Session = Depends(get_session),
        user_atual: Usuario = Depends(exigir_role(["admin"]))
):
    """ Rota para atualizar usuário (exige admin) """

    user = session.query(Usuario).filter_by(usuario_id=user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    if user_up.senha:
        user_up.senha = get_password_hash(user_up.senha)

    for campo, valor in user_up.dict(exclude_unset=True).items():
        setattr(user, campo, valor)

    session.commit()
    session.refresh(user)

    return user


@router.delete("{user_id}", status_code=204)
def delete_user(
        user_id: int,
        session: Session = Depends(get_session),
        user_atual: Usuario = Depends(exigir_role(["admin"]))
):
    """ Rota para deletar usuário (exige admin)"""

    user = session.query(Usuario).filter_by(usuario_id=user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    session.delete(user)
    session.commit()

    return


@router.get("/admin-area", response_model=UserPublic)
def admin_area(user: Usuario = Depends(exigir_role(["admin"]))):
    """ Rota protegida que exige papel admin """

    return user
