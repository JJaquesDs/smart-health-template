from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import exigir_role, get_session
from app.domains.pacientes.schemas import PacienteCreate, PacientePublic, PacienteUpdate
from app.domains.pacientes.schemas import (
    PacienteExameCreate,
    PacienteExamePublic,
    PacienteExameUpdate,
    PacienteHistoricoClinicoCreate,
    PacienteHistoricoClinicoPublic,
    PacienteHistoricoClinicoUpdate,
    PacienteMedicamentoCreate,
    PacienteMedicamentoPublic,
    PacienteMedicamentoUpdate,
)
from app.domains.pacientes.services import (
    create_patient_service,
    create_patient_exam_service,
    create_patient_history_service,
    create_patient_medication_service,
    delete_patient_exam_service,
    delete_patient_history_service,
    delete_patient_medication_service,
    delete_patient_service,
    get_patient_exam_service,
    get_patient_history_service,
    get_patient_service,
    get_patient_medication_service,
    list_patients_service,
    list_patient_exams_service,
    list_patient_histories_service,
    list_patient_medications_service,
    serialize_patient_for_user,
    update_patient_exam_service,
    update_patient_history_service,
    update_patient_medication_service,
    update_patient_service,
)
from app.domains.users.enums import UserRole
from app.domains.users.models import Usuario

router = APIRouter(prefix="/pacientes", tags=["pacientes"])

RoleProtegida = Annotated[
    Usuario,
    Depends(exigir_role([UserRole.MEDICO, UserRole.SECRETARIA])),
]
RoleMedico = Annotated[
    Usuario,
    Depends(exigir_role([UserRole.MEDICO])),
]


@router.post(
    "/",
    response_model=PacientePublic,
    summary="Criar paciente",
    description=(
        "Cria um novo paciente. Secretárias e médicos podem cadastrar pacientes, "
        "mas campos exclusivos do médico só podem ser enviados por usuários com role medico."
    ),
    response_description="Paciente criado com sucesso.",
    responses={
        400: {"description": "Erro de integridade, CPF/email duplicado ou dados inválidos."},
        401: {"description": "Usuário não autenticado."},
        403: {
            "description": (
                "Usuário sem permissão para acessar a rota ou tentando alterar campos "
                "exclusivos do médico."
            )
        },
    },
)
def create_patient(
    patient_in: PacienteCreate,
    user_atual: RoleProtegida,
    session: Session = Depends(get_session),
):
    try:
        patient = create_patient_service(session, patient_in, user_atual)
        session.commit()
        session.refresh(patient)
        return serialize_patient_for_user(patient, user_atual)
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Erro ao criar paciente")


@router.get(
    "/",
    response_model=list[PacientePublic],
    summary="Listar pacientes",
    description="Lista os pacientes cadastrados no sistema com visibilidade ajustada pelo perfil do usuário.",
    response_description="Lista de pacientes retornada com sucesso.",
    responses={
        401: {"description": "Usuário não autenticado."},
        403: {"description": "Usuário sem permissão para acessar a listagem de pacientes."},
    },
)
def read_patients(
    user_atual: RoleProtegida,
    session: Session = Depends(get_session),
):
    patients = list_patients_service(session)
    return [serialize_patient_for_user(patient, user_atual) for patient in patients]


@router.get(
    "/{patient_id}",
    response_model=PacientePublic,
    summary="Consultar paciente",
    description="Retorna os dados de um paciente específico.",
    response_description="Paciente retornado com sucesso.",
    responses={
        401: {"description": "Usuário não autenticado."},
        403: {"description": "Usuário sem permissão para acessar o paciente."},
        404: {"description": "Paciente não encontrado."},
    },
)
def read_patient(
    user_atual: RoleProtegida,
    patient_id: int = Path(..., description="Identificador do paciente."),
    session: Session = Depends(get_session),
):
    patient = get_patient_service(session, patient_id)
    return serialize_patient_for_user(patient, user_atual)


@router.put(
    "/{patient_id}",
    response_model=PacientePublic,
    summary="Atualizar paciente",
    description=(
        "Atualiza os dados de um paciente. Secretárias e médicos podem alterar os campos compartilhados. "
        "Campos exclusivos do médico só podem ser alterados por médicos."
    ),
    response_description="Paciente atualizado com sucesso.",
    responses={
        400: {"description": "Erro de integridade, CPF/email duplicado ou dados inválidos."},
        401: {"description": "Usuário não autenticado."},
        403: {
            "description": (
                "Usuário sem permissão para acessar a rota ou tentando alterar campos "
                "exclusivos do médico."
            )
        },
        404: {"description": "Paciente não encontrado."},
    },
)
def update_patient(
    patient_in: PacienteUpdate,
    user_atual: RoleProtegida,
    patient_id: int = Path(..., description="Identificador do paciente."),
    session: Session = Depends(get_session),
):
    try:
        patient = update_patient_service(session, patient_id, patient_in, user_atual)
        session.commit()
        session.refresh(patient)
        return serialize_patient_for_user(patient, user_atual)
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Erro ao atualizar paciente")


@router.delete(
    "/{patient_id}",
    status_code=204,
    summary="Excluir paciente",
    description="Remove um paciente do sistema.",
    responses={
        204: {"description": "Paciente removido com sucesso."},
        400: {"description": "Erro ao remover o paciente."},
        401: {"description": "Usuário não autenticado."},
        403: {"description": "Usuário sem permissão para excluir o paciente."},
        404: {"description": "Paciente não encontrado."},
    },
)
def delete_patient(
    _user_atual: RoleProtegida,
    patient_id: int = Path(..., description="Identificador do paciente."),
    session: Session = Depends(get_session),
):
    try:
        delete_patient_service(session, patient_id)
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Erro ao deletar paciente")


@router.get(
    "/{patient_id}/historico-clinico",
    response_model=list[PacienteHistoricoClinicoPublic],
    summary="Listar histórico clínico do paciente",
    description="Retorna o histórico clínico detalhado de um paciente. Acesso exclusivo de médico.",
    response_description="Histórico clínico retornado com sucesso.",
    responses={
        401: {"description": "Usuário não autenticado."},
        403: {"description": "Usuário sem permissão para acessar o histórico clínico."},
        404: {"description": "Paciente não encontrado."},
    },
)
def read_patient_histories(
    user_atual: RoleMedico,
    patient_id: int = Path(..., description="Identificador do paciente."),
    session: Session = Depends(get_session),
):
    return list_patient_histories_service(session, patient_id)


@router.post(
    "/{patient_id}/historico-clinico",
    response_model=PacienteHistoricoClinicoPublic,
    summary="Adicionar item ao histórico clínico do paciente",
    description="Cria um novo registro de histórico clínico para o paciente. Acesso exclusivo de médico.",
    response_description="Registro de histórico clínico criado com sucesso.",
    responses={
        400: {"description": "Erro ao criar o registro de histórico clínico."},
        401: {"description": "Usuário não autenticado."},
        403: {"description": "Usuário sem permissão para criar histórico clínico."},
        404: {"description": "Paciente não encontrado."},
    },
)
def create_patient_history(
    history_in: PacienteHistoricoClinicoCreate,
    user_atual: RoleMedico,
    patient_id: int = Path(..., description="Identificador do paciente."),
    session: Session = Depends(get_session),
):
    try:
        history = create_patient_history_service(session, patient_id, history_in)
        session.commit()
        session.refresh(history)
        return history
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Erro ao criar histórico clínico")


@router.get(
    "/{patient_id}/historico-clinico/{history_id}",
    response_model=PacienteHistoricoClinicoPublic,
    summary="Consultar item do histórico clínico do paciente",
    description="Retorna um item específico do histórico clínico do paciente. Acesso exclusivo de médico.",
    response_description="Item de histórico clínico retornado com sucesso.",
    responses={
        401: {"description": "Usuário não autenticado."},
        403: {"description": "Usuário sem permissão para acessar o histórico clínico."},
        404: {"description": "Paciente ou item de histórico clínico não encontrado."},
    },
)
def read_patient_history(
    user_atual: RoleMedico,
    patient_id: int = Path(..., description="Identificador do paciente."),
    history_id: int = Path(..., description="Identificador do item de histórico clínico."),
    session: Session = Depends(get_session),
):
    return get_patient_history_service(session, patient_id, history_id)


@router.put(
    "/{patient_id}/historico-clinico/{history_id}",
    response_model=PacienteHistoricoClinicoPublic,
    summary="Atualizar item do histórico clínico do paciente",
    description="Atualiza um item do histórico clínico do paciente. Acesso exclusivo de médico.",
    response_description="Item de histórico clínico atualizado com sucesso.",
    responses={
        400: {"description": "Erro ao atualizar o item de histórico clínico."},
        401: {"description": "Usuário não autenticado."},
        403: {"description": "Usuário sem permissão para atualizar o histórico clínico."},
        404: {"description": "Paciente ou item de histórico clínico não encontrado."},
    },
)
def update_patient_history(
    history_in: PacienteHistoricoClinicoUpdate,
    user_atual: RoleMedico,
    patient_id: int = Path(..., description="Identificador do paciente."),
    history_id: int = Path(..., description="Identificador do item de histórico clínico."),
    session: Session = Depends(get_session),
):
    try:
        history = update_patient_history_service(session, patient_id, history_id, history_in)
        session.commit()
        session.refresh(history)
        return history
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Erro ao atualizar histórico clínico")


@router.delete(
    "/{patient_id}/historico-clinico/{history_id}",
    status_code=204,
    summary="Excluir item do histórico clínico do paciente",
    description="Remove um item do histórico clínico do paciente. Acesso exclusivo de médico.",
    responses={
        204: {"description": "Item de histórico clínico removido com sucesso."},
        400: {"description": "Erro ao excluir o item de histórico clínico."},
        401: {"description": "Usuário não autenticado."},
        403: {"description": "Usuário sem permissão para excluir o histórico clínico."},
        404: {"description": "Paciente ou item de histórico clínico não encontrado."},
    },
)
def delete_patient_history(
    user_atual: RoleMedico,
    patient_id: int = Path(..., description="Identificador do paciente."),
    history_id: int = Path(..., description="Identificador do item de histórico clínico."),
    session: Session = Depends(get_session),
):
    try:
        delete_patient_history_service(session, patient_id, history_id)
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Erro ao deletar histórico clínico")


@router.get(
    "/{patient_id}/exames",
    response_model=list[PacienteExamePublic],
    summary="Listar exames do paciente",
    description="Retorna os exames registrados para o paciente. Acesso exclusivo de médico.",
    response_description="Exames do paciente retornados com sucesso.",
    responses={
        401: {"description": "Usuário não autenticado."},
        403: {"description": "Usuário sem permissão para acessar os exames do paciente."},
        404: {"description": "Paciente não encontrado."},
    },
)
def read_patient_exams(
    user_atual: RoleMedico,
    patient_id: int = Path(..., description="Identificador do paciente."),
    session: Session = Depends(get_session),
):
    return list_patient_exams_service(session, patient_id)


@router.post(
    "/{patient_id}/exames",
    response_model=PacienteExamePublic,
    summary="Adicionar exame ao paciente",
    description="Cria um novo registro de exame para o paciente. Acesso exclusivo de médico.",
    response_description="Exame do paciente criado com sucesso.",
    responses={
        400: {"description": "Erro ao criar o exame do paciente."},
        401: {"description": "Usuário não autenticado."},
        403: {"description": "Usuário sem permissão para criar exame do paciente."},
        404: {"description": "Paciente não encontrado."},
    },
)
def create_patient_exam(
    exam_in: PacienteExameCreate,
    user_atual: RoleMedico,
    patient_id: int = Path(..., description="Identificador do paciente."),
    session: Session = Depends(get_session),
):
    try:
        exam = create_patient_exam_service(session, patient_id, exam_in)
        session.commit()
        session.refresh(exam)
        return exam
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Erro ao criar exame do paciente")


@router.get(
    "/{patient_id}/exames/{exam_id}",
    response_model=PacienteExamePublic,
    summary="Consultar exame do paciente",
    description="Retorna um exame específico do paciente. Acesso exclusivo de médico.",
    response_description="Exame do paciente retornado com sucesso.",
    responses={
        401: {"description": "Usuário não autenticado."},
        403: {"description": "Usuário sem permissão para acessar o exame do paciente."},
        404: {"description": "Paciente ou exame do paciente não encontrado."},
    },
)
def read_patient_exam(
    user_atual: RoleMedico,
    patient_id: int = Path(..., description="Identificador do paciente."),
    exam_id: int = Path(..., description="Identificador do exame do paciente."),
    session: Session = Depends(get_session),
):
    return get_patient_exam_service(session, patient_id, exam_id)


@router.put(
    "/{patient_id}/exames/{exam_id}",
    response_model=PacienteExamePublic,
    summary="Atualizar exame do paciente",
    description="Atualiza um exame registrado para o paciente. Acesso exclusivo de médico.",
    response_description="Exame do paciente atualizado com sucesso.",
    responses={
        400: {"description": "Erro ao atualizar o exame do paciente."},
        401: {"description": "Usuário não autenticado."},
        403: {"description": "Usuário sem permissão para atualizar o exame do paciente."},
        404: {"description": "Paciente ou exame do paciente não encontrado."},
    },
)
def update_patient_exam(
    exam_in: PacienteExameUpdate,
    user_atual: RoleMedico,
    patient_id: int = Path(..., description="Identificador do paciente."),
    exam_id: int = Path(..., description="Identificador do exame do paciente."),
    session: Session = Depends(get_session),
):
    try:
        exam = update_patient_exam_service(session, patient_id, exam_id, exam_in)
        session.commit()
        session.refresh(exam)
        return exam
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Erro ao atualizar exame do paciente")


@router.delete(
    "/{patient_id}/exames/{exam_id}",
    status_code=204,
    summary="Excluir exame do paciente",
    description="Remove um exame registrado para o paciente. Acesso exclusivo de médico.",
    responses={
        204: {"description": "Exame do paciente removido com sucesso."},
        400: {"description": "Erro ao excluir o exame do paciente."},
        401: {"description": "Usuário não autenticado."},
        403: {"description": "Usuário sem permissão para excluir o exame do paciente."},
        404: {"description": "Paciente ou exame do paciente não encontrado."},
    },
)
def delete_patient_exam(
    user_atual: RoleMedico,
    patient_id: int = Path(..., description="Identificador do paciente."),
    exam_id: int = Path(..., description="Identificador do exame do paciente."),
    session: Session = Depends(get_session),
):
    try:
        delete_patient_exam_service(session, patient_id, exam_id)
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Erro ao deletar exame do paciente")


@router.get(
    "/{patient_id}/medicamentos",
    response_model=list[PacienteMedicamentoPublic],
    summary="Listar medicamentos do paciente",
    description="Retorna os medicamentos registrados para o paciente. Acesso exclusivo de médico.",
    response_description="Medicamentos do paciente retornados com sucesso.",
    responses={
        401: {"description": "Usuário não autenticado."},
        403: {"description": "Usuário sem permissão para acessar os medicamentos do paciente."},
        404: {"description": "Paciente não encontrado."},
    },
)
def read_patient_medications(
    user_atual: RoleMedico,
    patient_id: int = Path(..., description="Identificador do paciente."),
    session: Session = Depends(get_session),
):
    return list_patient_medications_service(session, patient_id)


@router.post(
    "/{patient_id}/medicamentos",
    response_model=PacienteMedicamentoPublic,
    summary="Adicionar medicamento ao paciente",
    description="Cria um novo registro de medicamento para o paciente. Acesso exclusivo de médico.",
    response_description="Medicamento do paciente criado com sucesso.",
    responses={
        400: {"description": "Erro ao criar o medicamento do paciente."},
        401: {"description": "Usuário não autenticado."},
        403: {"description": "Usuário sem permissão para criar medicamento do paciente."},
        404: {"description": "Paciente não encontrado."},
    },
)
def create_patient_medication(
    medication_in: PacienteMedicamentoCreate,
    user_atual: RoleMedico,
    patient_id: int = Path(..., description="Identificador do paciente."),
    session: Session = Depends(get_session),
):
    try:
        medication = create_patient_medication_service(session, patient_id, medication_in)
        session.commit()
        session.refresh(medication)
        return medication
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Erro ao criar medicamento do paciente")


@router.get(
    "/{patient_id}/medicamentos/{medication_id}",
    response_model=PacienteMedicamentoPublic,
    summary="Consultar medicamento do paciente",
    description="Retorna um medicamento específico do paciente. Acesso exclusivo de médico.",
    response_description="Medicamento do paciente retornado com sucesso.",
    responses={
        401: {"description": "Usuário não autenticado."},
        403: {"description": "Usuário sem permissão para acessar o medicamento do paciente."},
        404: {"description": "Paciente ou medicamento do paciente não encontrado."},
    },
)
def read_patient_medication(
    user_atual: RoleMedico,
    patient_id: int = Path(..., description="Identificador do paciente."),
    medication_id: int = Path(..., description="Identificador do medicamento do paciente."),
    session: Session = Depends(get_session),
):
    return get_patient_medication_service(session, patient_id, medication_id)


@router.put(
    "/{patient_id}/medicamentos/{medication_id}",
    response_model=PacienteMedicamentoPublic,
    summary="Atualizar medicamento do paciente",
    description="Atualiza um medicamento registrado para o paciente. Acesso exclusivo de médico.",
    response_description="Medicamento do paciente atualizado com sucesso.",
    responses={
        400: {"description": "Erro ao atualizar o medicamento do paciente."},
        401: {"description": "Usuário não autenticado."},
        403: {"description": "Usuário sem permissão para atualizar o medicamento do paciente."},
        404: {"description": "Paciente ou medicamento do paciente não encontrado."},
    },
)
def update_patient_medication(
    medication_in: PacienteMedicamentoUpdate,
    user_atual: RoleMedico,
    patient_id: int = Path(..., description="Identificador do paciente."),
    medication_id: int = Path(..., description="Identificador do medicamento do paciente."),
    session: Session = Depends(get_session),
):
    try:
        medication = update_patient_medication_service(
            session,
            patient_id,
            medication_id,
            medication_in,
        )
        session.commit()
        session.refresh(medication)
        return medication
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Erro ao atualizar medicamento do paciente")


@router.delete(
    "/{patient_id}/medicamentos/{medication_id}",
    status_code=204,
    summary="Excluir medicamento do paciente",
    description="Remove um medicamento registrado para o paciente. Acesso exclusivo de médico.",
    responses={
        204: {"description": "Medicamento do paciente removido com sucesso."},
        400: {"description": "Erro ao excluir o medicamento do paciente."},
        401: {"description": "Usuário não autenticado."},
        403: {"description": "Usuário sem permissão para excluir o medicamento do paciente."},
        404: {"description": "Paciente ou medicamento do paciente não encontrado."},
    },
)
def delete_patient_medication(
    user_atual: RoleMedico,
    patient_id: int = Path(..., description="Identificador do paciente."),
    medication_id: int = Path(..., description="Identificador do medicamento do paciente."),
    session: Session = Depends(get_session),
):
    try:
        delete_patient_medication_service(session, patient_id, medication_id)
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Erro ao deletar medicamento do paciente")
