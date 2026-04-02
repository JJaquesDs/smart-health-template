from sqlalchemy.orm import Session
from app.core.security import get_password_hash, verify_password

from app.domains.users.models import Usuario
from app.domains.users.schemas import UserUpdate


def create_user(
        session: Session,
        email: str,
        senha: str,
        nome: str,
        telefone: str,
        role: str
):
    """ Service Create Usuário """

    hashed_senha = get_password_hash(senha)    ## Função de app/core/security.py para pegar senha com hash
    user = Usuario(email=email, senha=hashed_senha, nome=nome, telefone=telefone, role=role)

    session.add(user)   ## session objeto cria sessoes no banco de dados
    session.commit()
    session.refresh(user)
    return user


def authenticate_user(session: Session, email: str, senha: str):
    """ Função que verifica autenticação do usuário """

    user = session.query(Usuario).filter(Usuario.email == email).first()  ## Verificando se o usuário existe pelo email através de query

    if not user:
        return None
    if not verify_password(senha, user.senha):  ## Função de verificação de senha de app/core/security.py
        return None

    return user


def update_user(session: Session, user: Usuario, user_up: UserUpdate):
    """ Função para atualizar usuário"""

    if user_up.senha:
        user_up.senha = get_password_hash(user_up.senha)

    for chave, valor in user_up.dict(exclude_unset=True).items():
        setattr(user, chave, valor)

    session.add(user)
    session.commit()
    session.refresh(user)

    return user
