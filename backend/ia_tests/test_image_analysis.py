"""Execute pytest ia_tests --confcutdir=ia_tests -q com o banco local migrado."""
import base64
from types import SimpleNamespace
from unittest.mock import patch
from uuid import uuid4
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.core.db import engine, get_session
from app.core.security import create_access_token
from app.domains.users.models import Usuario
from app.domains.users.enums import UserRole
from app.domains.exames.imagem.models import ResultadoExameImagemIa
from app.domains.exames.imagem import service
from app.api.routes import image_exame_routes

PNG = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+j1ioAAAAASUVORK5CYII=')

@pytest.fixture
def ctx(tmp_path, monkeypatch):
    conn = engine.connect(); transaction = conn.begin()
    def dependency():
        with Session(bind=conn, join_transaction_mode='create_savepoint') as session:
            yield session
    app.dependency_overrides[get_session] = dependency
    monkeypatch.setattr(service, 'UPLOAD_DIR', tmp_path)
    monkeypatch.setattr(image_exame_routes, 'UPLOAD_DIR', tmp_path)
    def headers(role):
        with Session(bind=conn, join_transaction_mode='create_savepoint') as session:
            user = Usuario(nome='IA teste', email=f'{uuid4().hex[:12]}@example.com', telefone='000', senha='unused', role=role)
            session.add(user); session.flush()
            token = create_access_token(user); session.commit()
            return {'Authorization': 'Bearer ' + token}
    client = TestClient(app)
    try:
        yield client, headers, conn, tmp_path
    finally:
        client.close(); app.dependency_overrides.clear(); transaction.rollback(); conn.close()


def test_upload_validation_and_authorization(ctx):
    client, headers, _, directory = ctx
    doctor = headers(UserRole.MEDICO); secretary = headers(UserRole.SECRETARIA)
    assert client.post('/exame_imagem/', files={'file':('a.png',PNG,'image/png')}).status_code == 401
    assert client.post('/exame_imagem/', headers=secretary, files={'file':('a.png',PNG,'image/png')}).status_code == 403
    assert client.post('/exame_imagem/', headers=doctor, files={'file':('a.png',b'not image','image/png')}).status_code == 415
    response = client.post('/exame_imagem/', headers=doctor, files={'file':('../../unsafe.png',PNG,'image/png')})
    assert response.status_code == 200, response.text
    name = response.json()['link_imagem'].rsplit('/',1)[-1]
    assert name != 'unsafe.png' and (directory/name).is_file()
    assert client.get(response.json()['link_imagem'], headers=doctor).status_code == 200
    other = headers(UserRole.MEDICO)
    assert client.get(response.json()['link_imagem'], headers=other).status_code == 403
    assert client.get('/exame_imagem/', headers=other).json() == []


def test_start_poll_save_and_repeat(ctx):
    client, headers, connection, _ = ctx
    doctor=headers(UserRole.MEDICO)
    exam=client.post('/exame_imagem/',headers=doctor,files={'file':('sample.png',PNG,'image/png')}).json()['exame_id']
    with patch.object(image_exame_routes.celery_app,'send_task') as send:
        response=client.post(f'/exame_imagem/{exam}/analisar',headers=doctor)
        assert response.status_code==200
        task=response.json()['task_id']
        assert client.post(f'/exame_imagem/{exam}/analisar',headers=doctor).json()['task_id']==task
        assert send.call_count==1
    other=headers(UserRole.MEDICO)
    assert client.get(f'/exame_imagem/resultado/{task}',headers=other).status_code==403
    assert client.get(f'/exame_imagem/resultado/{task}').status_code==401
    for status in ['PENDING','STARTED','RETRY','FAILURE']:
        with patch.object(service,'AsyncResult',return_value=SimpleNamespace(state=status)):
            assert client.get(f'/exame_imagem/resultado/{task}',headers=doctor).json()['status']==status
    probabilities={'Dyskeratotic':0.1,'Koilocytotic':0.5,'Metaplastic':0.2,'Parabasal':0.1,'Superficial-Intermediate':0.1}
    data=dict(exame_img_id=exam,classe='Koilocytotic',confianca=0.5,probabilidades=probabilities)
    with patch.object(service,'AsyncResult',return_value=SimpleNamespace(state='SUCCESS',result=data)):
        response=client.get(f'/exame_imagem/resultado/{task}',headers=doctor)
        assert response.status_code==200,response.text
        assert response.json()['probabilidades']==probabilities
    # O resultado continua disponível mesmo sem o resultado temporário do Redis.
    with patch.object(service,'AsyncResult',side_effect=RuntimeError('Redis indisponível')):
        assert client.get(f'/exame_imagem/resultado/{task}',headers=doctor).json()['status']=='SUCCESS'
    with Session(bind=connection,join_transaction_mode='create_savepoint') as session:
        assert session.query(ResultadoExameImagemIa).filter_by(exame_imagem_id=exam).count()==1
    assert client.get('/exame_imagem/',headers=doctor).json()[0]['resultado']['classe_predita']=='Koilocytotic'


def test_broker_failure_and_unknown_task(ctx):
    client,headers,_,_=ctx;doctor=headers(UserRole.MEDICO)
    exam=client.post('/exame_imagem/',headers=doctor,files={'file':('sample.png',PNG,'image/png')}).json()['exame_id']
    with patch.object(image_exame_routes.celery_app,'send_task',side_effect=ConnectionError()):
        assert client.post(f'/exame_imagem/{exam}/analisar',headers=doctor).status_code==503
    assert client.get('/exame_imagem/resultado/unknown',headers=doctor).status_code==404
