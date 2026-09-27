from datetime import datetime, timedelta, timezone
from typing import Literal
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, field_validator
from sqlalchemy.orm import Session

from app.api.deps import exigir_role, get_session
from app.domains.consultas.models import Consulta
from app.domains.exames.imagem.models import ExameImagem, ResultadoExameImagemIa
from app.domains.pacientes.models import Paciente
from app.domains.pacientes.services import serialize_patient_for_user
from app.domains.professionals.medico.models import Medico
from app.domains.professionals.secretaria.models import Secretaria
from app.domains.users.enums import UserRole
from app.domains.users.models import Usuario

router = APIRouter(tags=["Dashboard"])
access = exigir_role([UserRole.MEDICO, UserRole.SUPERUSER, UserRole.SECRETARIA])
scheduling_access = exigir_role([UserRole.SECRETARIA, UserRole.SUPERUSER])
LOCAL = ZoneInfo("America/Belem")


def appointments_query(session, user):
    q = session.query(Consulta)
    if user.role == UserRole.MEDICO:
        q = q.join(Medico).filter(Medico.usuario_id == user.usuario_id)
    return q


def appointment_data(row):
    return {
        "id": row.consulta_id,
        "paciente_id": row.paciente_id,
        "paciente_nome": row.paciente.nome,
        "medico_id": row.medico_id,
        "medico_nome": row.medico.usuario.nome,
        "especialidade": row.medico.usuario.especialidade_principal,
        "starts_at": row.starts_at,
        "data_consulta": row.data_consulta,
        "status": row.status,
        "observacoes": row.observacoes,
    }


@router.get("/dashboard/")
def dashboard(session: Session = Depends(get_session), user: Usuario = Depends(access)):
    patients = session.query(Paciente)
    recent = (
        patients.order_by(
            Paciente.created_at.desc().nullslast(), Paciente.paciente_id.desc()
        )
        .limit(5)
        .all()
    )
    appointments = appointments_query(session, user)
    today = datetime.now(LOCAL).date()
    data = {
        "total_patients": patients.count(),
        "active_patients": patients.filter(Paciente.status == "active").count(),
        "recent_patients": [serialize_patient_for_user(p, user) for p in recent],
        "appointments_today": appointments.filter(
            Consulta.data_consulta == today.isoformat(), Consulta.status != "cancelled"
        ).count(),
        "waiting_appointments": appointments.filter(
            Consulta.status == "waiting"
        ).count(),
    }
    if user.role != UserRole.SECRETARIA:
        images = session.query(ExameImagem)
        results = session.query(ResultadoExameImagemIa).join(ExameImagem)
        if user.role == UserRole.MEDICO:
            images = images.filter(ExameImagem.usuario_id == user.usuario_id)
            results = results.filter(ExameImagem.usuario_id == user.usuario_id)
        month_start = (
            datetime.now(LOCAL)
            .replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            .astimezone(timezone.utc)
            .replace(tzinfo=None)
        )
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        data.update(
            images_without_result=images.filter(~ExameImagem.resultados.any()).count(),
            ai_this_month=results.filter(
                ResultadoExameImagemIa.data_analise >= month_start,
                ResultadoExameImagemIa.data_analise <= now,
            ).count(),
            recent_analyses=[
                {
                    "id": r.resultado_id,
                    "exame_id": r.exame_imagem_id,
                    "classe": r.classe_predita,
                    "confianca": r.confianca,
                    "data_analise": r.data_analise.replace(tzinfo=timezone.utc)
                    if r.data_analise
                    else None,
                }
                for r in results.order_by(
                    ResultadoExameImagemIa.data_analise.desc(),
                    ResultadoExameImagemIa.resultado_id.desc(),
                ).limit(5)
            ],
        )
    return data


@router.get("/agenda/medicos")
def doctors(session: Session = Depends(get_session), _user: Usuario = Depends(access)):
    return [
        {
            "id": m.medico_id,
            "nome": m.usuario.nome,
            "especialidade": m.usuario.especialidade_principal,
        }
        for m in session.query(Medico).join(Usuario).order_by(Usuario.nome).all()
    ]


@router.get("/agenda/")
def appointments(
    session: Session = Depends(get_session), user: Usuario = Depends(access)
):
    return [
        appointment_data(a)
        for a in appointments_query(session, user)
        .order_by(Consulta.data_consulta, Consulta.starts_at)
        .all()
    ]


class AppointmentInput(BaseModel):
    paciente_id: int
    medico_id: int
    starts_at: datetime
    status: Literal["waiting", "confirmed", "cancelled"] = "waiting"
    observacoes: str | None = Field(default=None, max_length=2000)

    @field_validator("starts_at")
    @classmethod
    def aware(cls, value):
        if value.tzinfo is None:
            raise ValueError("Informe o fuso horário da consulta")
        return value


def save_appointment(session, user, data, row=None):
    doctor = (
        session.query(Medico)
        .filter_by(medico_id=data.medico_id)
        .with_for_update()
        .first()
    )
    if not doctor or not session.get(Paciente, data.paciente_id):
        raise HTTPException(404, "Médico ou paciente não encontrado")
    # O bloqueio do médico serializa tentativas de reservar o mesmo horário.
    conflict = session.query(Consulta).filter(
        Consulta.medico_id == data.medico_id,
        Consulta.starts_at > data.starts_at - timedelta(hours=1),
        Consulta.starts_at < data.starts_at + timedelta(hours=1),
        Consulta.status != "cancelled",
    )
    if row:
        conflict = conflict.filter(Consulta.consulta_id != row.consulta_id)
    if data.status != "cancelled" and conflict.first():
        raise HTTPException(409, "Médico já possui consulta neste horário")
    if row is None:
        secretary = (
            session.query(Secretaria).filter_by(usuario_id=user.usuario_id).first()
        )
        if user.role == UserRole.SECRETARIA and not secretary:
            raise HTTPException(409, "Perfil profissional de secretária não cadastrado")
        row = Consulta(secretaria_id=secretary.secretaria_id if secretary else None)
        session.add(row)
    for key, value in data.model_dump().items():
        setattr(row, key, value)
    row.data_consulta = data.starts_at.astimezone(LOCAL).date().isoformat()
    session.commit()
    session.refresh(row)
    return appointment_data(row)


@router.post("/agenda/")
def create_appointment(
    data: AppointmentInput,
    session: Session = Depends(get_session),
    user: Usuario = Depends(scheduling_access),
):
    return save_appointment(session, user, data)


@router.put("/agenda/{appointment_id}")
def update_appointment(
    appointment_id: int,
    data: AppointmentInput,
    session: Session = Depends(get_session),
    user: Usuario = Depends(scheduling_access),
):
    row = session.get(Consulta, appointment_id)
    if not row:
        raise HTTPException(404, "Consulta não encontrada")
    return save_appointment(session, user, data, row)
