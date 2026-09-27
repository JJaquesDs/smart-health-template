from uuid import uuid4
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.core.db import engine, get_session
from app.core.security import create_access_token
from app.domains.users.models import Usuario
from app.domains.users.enums import UserRole

@pytest.fixture
def ctx():
    conn=engine.connect(); transaction=conn.begin()
    def dependency():
        with Session(bind=conn, join_transaction_mode='create_savepoint') as session:
            yield session
    app.dependency_overrides[get_session]=dependency
    def headers(role):
        with Session(bind=conn, join_transaction_mode='create_savepoint') as session:
            user=Usuario(nome='Teste',email=uuid4().hex[:12]+'@example.com',telefone='000',senha='unused',role=role)
            session.add(user); session.flush()
            token=create_access_token(user);session.commit()
            return {'Authorization':'Bearer '+token}
    with TestClient(app) as client:
        try: yield client,headers
        finally:
            app.dependency_overrides.clear();transaction.rollback();conn.close()

def payload():
    # CPF sintético com dígitos verificadores válidos.
    digits=[int(x) for x in str(uuid4().int)[:9]]
    for size in (9,10):
        check=sum(digits[i]*(size+1-i) for i in range(size))*10%11
        digits.append(0 if check==10 else check)
    return dict(nome='Teste paciente',cpf=''.join(map(str,digits)),data_nascimento='2000-01-01',genero='feminino',email=uuid4().hex[:12]+'@example.com',telefone='000')


def test_dashboard_and_agenda_persistence(ctx):
    from app.domains.professionals.medico.models import Medico
    from app.domains.professionals.secretaria.models import Secretaria
    from app.core.security import ALGORITHM
    from app.core.config import settings
    import jwt
    c,headers=ctx
    admin=headers(UserRole.SUPERUSER); doctor=headers(UserRole.MEDICO); secretary=headers(UserRole.SECRETARIA)
    def uid(h):return int(jwt.decode(h['Authorization'].split()[1],settings.SECRET_KEY,algorithms=[ALGORITHM])['sub'])
    # Usa a sessão transacional do fixture, sem deixar registros de teste.
    dep=app.dependency_overrides[get_session]
    with next(dep()) as s:
        m=Medico(usuario_id=uid(doctor),cpf=uuid4().hex[:14],rg='TESTE',crm_numero=uuid4().hex,crm_UF='PA')
        sec=Secretaria(usuario_id=uid(secretary),cpf=uuid4().hex[:14],rg='TESTE')
        s.add_all([m,sec]);s.flush();mid=m.medico_id;s.commit()
    assert c.get('/dashboard/').status_code==401
    before=c.get('/dashboard/',headers=admin).json()
    patient=c.post('/pacientes/',headers=admin,json=payload()).json()
    after=c.get('/dashboard/',headers=admin).json()
    assert after['total_patients']==before['total_patients']+1
    assert after['active_patients']==before['active_patients']+1
    data=dict(paciente_id=patient['paciente_id'],medico_id=mid,starts_at='2030-01-01T10:00:00-03:00',status='waiting')
    response=c.post('/agenda/',headers=secretary,json=data)
    assert response.status_code==200,response.text
    ap=response.json();assert ap['data_consulta']=='2030-01-01'
    assert any(x['id']==ap['id'] for x in c.get('/agenda/',headers=doctor).json())
    other=headers(UserRole.MEDICO)
    assert c.get('/agenda/',headers=other).json()==[]
    assert c.post('/agenda/',headers=doctor,json=data).status_code==403
    assert c.post('/agenda/',headers=secretary,json=data).status_code==409
    assert c.post('/agenda/',headers=secretary,json={**data,'starts_at':'2030-01-01T10:30:00-03:00'}).status_code==409
    assert c.put(f"/agenda/{ap['id']}",headers=secretary,json={**data,'status':'cancelled'}).status_code==200
    assert c.post('/agenda/',headers=admin,json=data).status_code==200
    assert 'recent_analyses' not in c.get('/dashboard/',headers=secretary).json()
    assert c.get('/dashboard/',headers=other).json()['ai_this_month']==0
    assert c.post('/agenda/',headers=secretary,json={**data,'starts_at':'2030-01-01T10:00:00'}).status_code==422

def test_ai_dashboard_filters_owner_and_month(ctx):
    from datetime import datetime, timedelta
    import jwt
    from app.core.security import ALGORITHM
    from app.core.config import settings
    from app.domains.exames.imagem.models import ExameImagem, ResultadoExameImagemIa
    c,headers=ctx; doctor=headers(UserRole.MEDICO);other=headers(UserRole.MEDICO)
    uid=int(jwt.decode(doctor['Authorization'].split()[1],settings.SECRET_KEY,algorithms=[ALGORITHM])['sub'])
    dep=app.dependency_overrides[get_session]
    with next(dep()) as s:
        for delta in (0,45):
            e=ExameImagem(tipo='citologia',usuario_id=uid);s.add(e);s.flush()
            s.add(ResultadoExameImagemIa(exame_imagem_id=e.exame_id,classe_predita='Parabasal',confianca=.8,probabilidades={'Parabasal':.8},data_analise=datetime.utcnow()-timedelta(days=delta)))
        s.add(ExameImagem(tipo='citologia',usuario_id=uid));s.commit()
    data=c.get('/dashboard/',headers=doctor).json()
    assert data['ai_this_month']==1
    assert data['images_without_result']==1
    assert len(data['recent_analyses'])==2
    assert all(a['classe']=='Parabasal' and 'risk' not in a for a in data['recent_analyses'])
    other_data=c.get('/dashboard/',headers=other).json()
    assert other_data['recent_analyses']==[] and other_data['images_without_result']==0
