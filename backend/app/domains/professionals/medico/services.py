from fastapi import HTTPException

import traceback

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.domains.users.models import Usuario
from app.domains.users.enums import UserRole

from app.domains.professionals.medico.models import Medico

from app.domains.professionals.medico.medico_esp.model import MedicoEspecialidade

from app.domains.professionals.medico.medico_esp.schemas import MedicoEspCreate

from app.domains.professionals.medico.medico_esp.enums_med_esp import StatusEsp

from app.domains.professionals.medico.especialidade.repository import (
    get_esp_by_id
)


from app.domains.professionals.medico.medico_esp.repository import (
    create_med_esp_db
)

from app.domains.users.services import (
    create_user_service
)

from app.domains.professionals.medico.repository import (
    create_medico_db
)


def create_medico_service(
        session: Session,
        nome: str,
        telefone: str,
        email: str,
        senha: str,
        cpf: str,
        rg: str,
        crm_num: str,
        crm_uf: str,
        med_esps: list[MedicoEspCreate],
        role: UserRole.MEDICO,
        user_atual: Usuario | None = None
):
    """ Service para criar um médico """

    try:
        user = create_user_service(
            session=session,
            usuer_atual=user_atual,
            nome=nome,
            telefone=telefone,
            email=email,
            senha=senha,
            role=role
        )

        # Garantindo do banco o 'usario_id' por ser autoincrement
        session.flush()

        # Criação 'médico'
        medico = Medico(
            cpf=cpf,
            rg=rg,
            crm_numero=crm_num,
            crm_UF=crm_uf,
            usuario_id=user.usuario_id
        )

        create_medico_db(session=session, medico=medico)


        # Criação de relações 'N:N'
        for esp in med_esps:

            especialidade = get_esp_by_id(session=session, esp_id=esp.esp_id)

            if not especialidade:
                raise HTTPException(
                    status_code=404,
                    detail=f"Especialidade não encontrada {esp.esp_id} não encontrada"
                )

            relacao = MedicoEspecialidade(
                medico_id=medico.medico_id,
                esp_id=esp.esp_id,
                status=esp.status
            )

            create_med_esp_db(session=session, med_esp=relacao)

        return medico

    except IntegrityError:
        print(traceback.format_exc())

        raise HTTPException(
            status_code=400,
            detail="Erro ao criar usuário médico"
        )
