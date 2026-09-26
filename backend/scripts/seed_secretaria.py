"""Cria um acesso de secretária de demonstração sem alterar contas existentes."""
import secrets
from sqlalchemy.orm import Session
from app.core.db import engine
from app.core.security import get_password_hash
from app.domains.users.models import Usuario
from app.domains.users.enums import UserRole
from app.domains.professionals.secretaria.models import Secretaria


def main():
    with Session(engine) as session:
        email = 'secretaria.demo@medase.com'
        if session.query(Usuario).filter_by(email=email).first():
            email = f'secretaria.{secrets.token_hex(3)}@medase.com'
        password = secrets.token_urlsafe(15)
        user = Usuario(nome='Secretária Demonstração',email=email,telefone='91999990000',role=UserRole.SECRETARIA,senha=get_password_hash(password))
        session.add(user)
        session.flush()
        while True:
            digits=[secrets.randbelow(10) for _ in range(9)]
            for size in (9,10):
                check=sum(digits[i]*(size+1-i) for i in range(size))*10%11
                digits.append(0 if check==10 else check)
            cpf=''.join(map(str,digits))
            if len(set(cpf))>1 and not session.query(Secretaria).filter_by(cpf=cpf).first(): break
        session.add(Secretaria(usuario_id=user.usuario_id,cpf=cpf,rg='DEMO'+secrets.token_hex(4)))
        session.commit()
        print(f'EMAIL={email}\nPASSWORD={password}\nROLE=secretaria')

if __name__ == '__main__':
    main()
