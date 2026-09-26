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

@pytest.mark.parametrize('role',[UserRole.MEDICO,UserRole.SECRETARIA,UserRole.SUPERUSER])
def test_create_read_update_metadata(ctx,role):
    c,headers=ctx;h=headers(role);p=payload();cpf=p['cpf']
    p['cpf']=f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'
    if role==UserRole.SUPERUSER: p['observacoes']='Campo clínico'
    r=c.post('/pacientes/',headers=h,json=p)
    assert r.status_code==200,r.text
    d=r.json();assert d['cpf']==cpf
    assert d['created_at'] and d['updated_at'] and d['status']=='active'
    url=f"/pacientes/{d['paciente_id']}"
    assert c.get(url,headers=h).json()==d
    assert any(row['paciente_id']==d['paciente_id'] for row in c.get('/pacientes/',headers=h).json())
    p['cpf']=cpf;p['email']=uuid4().hex[:12]+'@example.com'
    assert c.post('/pacientes/',headers=h,json=p).status_code==400
    changed=c.put(url,headers=h,json={'status':'inactive','nome':'Atualizado'}).json()
    assert changed['status']=='inactive' and changed['created_at']==d['created_at']
    assert changed['updated_at']>d['updated_at']
    assert c.get(url,headers=h).json()['status']=='inactive'

@pytest.mark.parametrize('cpf',['11111111111','12345678900','123','abc12345678900',None])
def test_invalid_cpf(ctx,cpf):
    c,headers=ctx;h=headers(UserRole.SUPERUSER);p=payload();p['cpf']=cpf
    assert c.post('/pacientes/',headers=h,json=p).status_code==422

def test_secretary_clinical_permissions_and_update_validation(ctx):
    c,headers=ctx;h=headers(UserRole.SECRETARIA);p=payload()
    assert c.post('/pacientes/',headers=h,json={**p,'observacoes':'restrito'}).status_code==403
    r=c.post('/pacientes/',headers=h,json=p);assert r.status_code==200
    url=f"/pacientes/{r.json()['paciente_id']}"
    for invalid in ({'cpf':None},{'cpf':'00000000000'},{'status':None},{'status':'invalid'}):
        assert c.put(url,headers=h,json=invalid).status_code==422

@pytest.mark.parametrize('invalid',[
    {'nome':'   '},{'nome':'x'*256},{'data_nascimento':'2999-01-01'},
    {'data_nascimento':'2000-02-30'},{'data_nascimento':'not-a-date'},
    {'telefone':None},{'email':'a'*34+'@example.com'},
    {'rua':'x'*256},{'cidade':'x'*121},{'numero':'x'*46},
    {'contato_emergencia_parentesco':'x'*121},
])
def test_additional_validation_create_and_update(ctx,invalid):
    c,headers=ctx;h=headers(UserRole.SUPERUSER);p=payload()
    assert c.post('/pacientes/',headers=h,json={**p,**invalid}).status_code==422
    r=c.post('/pacientes/',headers=h,json=p);assert r.status_code==200
    assert c.put(f"/pacientes/{r.json()['paciente_id']}",headers=h,json=invalid).status_code==422


def test_trim_name_and_partial_update(ctx):
    c,headers=ctx;h=headers(UserRole.SUPERUSER);p=payload();p['nome']='  Paciente Teste  '
    r=c.post('/pacientes/',headers=h,json=p);assert r.status_code==200
    assert r.json()['nome']=='Paciente Teste'
    assert c.put(f"/pacientes/{r.json()['paciente_id']}",headers=h,json={'rua':None}).status_code==200
