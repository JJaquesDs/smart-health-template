# DEV-03

## Escopo

Esta documentação cobre o que foi implementado no backend do `smart-health-template` durante a DEV-03, com foco em:

- CRUD de pacientes
- histórico clínico do paciente
- exames do paciente
- medicamentos do paciente
- suporte a anexo PDF em exame do paciente
- documentação Swagger das rotas novas
- ajustes de infraestrutura de desenvolvimento para refletir mudanças sem `down/up` constante

## Arquivos alterados

### Domínio de pacientes

- [models.py](c:/Users/gabib/smart-health-template/backend/app/domains/pacientes/models.py)
- [schemas.py](c:/Users/gabib/smart-health-template/backend/app/domains/pacientes/schemas.py)
- [repository.py](c:/Users/gabib/smart-health-template/backend/app/domains/pacientes/repository.py)
- [services.py](c:/Users/gabib/smart-health-template/backend/app/domains/pacientes/services.py)

### Rotas

- [patient_routes.py](c:/Users/gabib/smart-health-template/backend/app/api/routes/patient_routes.py)
- [exam_routes.py](c:/Users/gabib/smart-health-template/backend/app/api/routes/exam_routes.py)
- [medication_routes.py](c:/Users/gabib/smart-health-template/backend/app/api/routes/medication_routes.py)
- [main.py](c:/Users/gabib/smart-health-template/backend/app/main.py)
- [api/main.py](c:/Users/gabib/smart-health-template/backend/app/api/main.py)

### Infra e inicialização

- [db.py](c:/Users/gabib/smart-health-template/backend/app/core/db.py)
- [docker-compose.yml](c:/Users/gabib/smart-health-template/docker-compose.yml)
- [docker-compose.override.yml](c:/Users/gabib/smart-health-template/docker-compose.override.yml)

### Migrations

- [e8a1c2f4d6b7_expande_pacientes_para_crud_clinico.py](c:/Users/gabib/smart-health-template/backend/app/alembic/versions/e8a1c2f4d6b7_expande_pacientes_para_crud_clinico.py)
- [f1a2b3c4d5e6_cria_historico_exames_e_medicamentos_do_paciente.py](c:/Users/gabib/smart-health-template/backend/app/alembic/versions/f1a2b3c4d5e6_cria_historico_exames_e_medicamentos_do_paciente.py)
- [9b7a6c5d4e3f_adiciona_pdf_url_em_paciente_exames.py](c:/Users/gabib/smart-health-template/backend/app/alembic/versions/9b7a6c5d4e3f_adiciona_pdf_url_em_paciente_exames.py)

## Pacientes

Foi implementado o CRUD base de pacientes com os campos:

- obrigatórios: `nome`, `cpf`, `data_nascimento`, `genero`, `email`, `telefone`
- endereço: `rua`, `numero`, `complemento`, `cidade`, `estado`, `cep`
- dados compartilhados entre médico e secretária: `dados_clinicos`, `tipo_sanguineo`, `ultimo_exame`, `alergias`
- contato de emergência: `contato_emergencia_nome`, `contato_emergencia_parentesco`, `contato_emergencia_telefone`
- campos exclusivos do médico: `medicamentos`, `historico_medico`, `observacoes`

### Regras de permissão

- `medico` e `secretaria` podem criar, listar, consultar, atualizar e excluir pacientes
- `secretaria` não pode alterar campos exclusivos do médico
- ao consultar/listar paciente como `secretaria`, os campos exclusivos do médico são retornados como `null`

### Rotas

- `POST /pacientes/`
- `GET /pacientes/`
- `GET /pacientes/{patient_id}`
- `PUT /pacientes/{patient_id}`
- `DELETE /pacientes/{patient_id}`

## Histórico clínico do paciente

Foi adicionado um subdomínio clínico para histórico detalhado do paciente.

### Estrutura

- entidade: `PacienteHistoricoClinico`
- campos: `titulo`, `descricao`, `data_registro`

### Permissão

- acesso exclusivo de `medico`

### Rotas

- `GET /pacientes/{patient_id}/historico-clinico`
- `POST /pacientes/{patient_id}/historico-clinico`
- `GET /pacientes/{patient_id}/historico-clinico/{history_id}`
- `PUT /pacientes/{patient_id}/historico-clinico/{history_id}`
- `DELETE /pacientes/{patient_id}/historico-clinico/{history_id}`

## Exames do paciente

Foi adicionada a persistência de exames vinculados ao paciente, separada do catálogo principal de exames.

### Estrutura

- entidade: `PacienteExame`
- campos: `nome`, `data_exame`, `status`, `resultado`, `descricao`, `observacoes`, `pdf_nome`, `pdf_url`

### Anexo de exame

O backend passou a aceitar e persistir:

- `pdf_nome`: nome original do arquivo
- `pdf_url`: conteúdo/URL serializado usado pelo frontend para download/abertura do anexo

Observação:
- `pdf_url` foi incluído depois por migration incremental, pois inicialmente o fluxo salvava apenas `pdf_nome`

### Permissão

- acesso exclusivo de `medico`

### Rotas

- `GET /pacientes/{patient_id}/exames`
- `POST /pacientes/{patient_id}/exames`
- `GET /pacientes/{patient_id}/exames/{exam_id}`
- `PUT /pacientes/{patient_id}/exames/{exam_id}`
- `DELETE /pacientes/{patient_id}/exames/{exam_id}`

## Medicamentos do paciente

Foi adicionada a persistência de medicamentos vinculados ao paciente, separada do catálogo principal de medicamentos.

### Estrutura

- entidade: `PacienteMedicamento`
- campos: `nome`, `dosagem`, `periodo`, `status`, `descricao`, `observacoes`

### Permissão

- acesso exclusivo de `medico`

### Rotas

- `GET /pacientes/{patient_id}/medicamentos`
- `POST /pacientes/{patient_id}/medicamentos`
- `GET /pacientes/{patient_id}/medicamentos/{medication_id}`
- `PUT /pacientes/{patient_id}/medicamentos/{medication_id}`
- `DELETE /pacientes/{patient_id}/medicamentos/{medication_id}`

## Catálogos de exames e medicamentos

O backend também recebeu os catálogos centrais consumidos pelo frontend.

### Exames de catálogo

Campos:

- `nome`
- `categoria`
- `descricao`
- `preco`
- `preparacao`
- `observacoes`
- `ativo`

Rotas:

- `POST /exames/`
- `GET /exames/`
- `GET /exames/{exam_id}`
- `PUT /exames/{exam_id}`
- `DELETE /exames/{exam_id}`

Permissão:

- `medico`
- `admin`
- `superuser`

### Medicamentos de catálogo

Campos:

- `nome`
- `principio_ativo`
- `dosagem`
- `forma_farmaceutica`
- `fabricante`
- `descricao`
- `contraindicacoes`
- `efeitos_colaterais`
- `ativo`

Rotas:

- `POST /medicamentos/`
- `GET /medicamentos/`
- `GET /medicamentos/{medication_id}`
- `PUT /medicamentos/{medication_id}`
- `DELETE /medicamentos/{medication_id}`

Permissão:

- `medico`
- `admin`
- `superuser`

## Swagger

A documentação OpenAPI/Swagger foi padronizada para as rotas novas.

### Cobertura

As rotas novas passaram a ter:

- `summary`
- `description`
- `response_description`
- `responses` por status onde aplicável
- `Path(...)` com descrição dos identificadores

### Arquivos

- [patient_routes.py](c:/Users/gabib/smart-health-template/backend/app/api/routes/patient_routes.py)
- [exam_routes.py](c:/Users/gabib/smart-health-template/backend/app/api/routes/exam_routes.py)
- [medication_routes.py](c:/Users/gabib/smart-health-template/backend/app/api/routes/medication_routes.py)

## CORS e inicialização

Foram feitos ajustes no backend para suportar a integração com o `medase`.

### CORS

Em [main.py](c:/Users/gabib/smart-health-template/backend/app/main.py):

- adicionado `CORSMiddleware`
- leitura das origens a partir da configuração já existente

Objetivo:

- permitir chamadas do frontend `medase`, em especial a partir de `http://localhost:5173`

### Bootstrap do superusuário

Em [services.py](c:/Users/gabib/smart-health-template/backend/app/domains/users/services.py) e [db.py](c:/Users/gabib/smart-health-template/backend/app/core/db.py):

- a criação inicial do primeiro `superuser` foi ajustada para não quebrar o startup
- foi introduzido um fluxo explícito de bootstrap controlado

## Infra de desenvolvimento

Para reduzir a necessidade de `docker compose down && up` em toda alteração:

- [docker-compose.override.yml](c:/Users/gabib/smart-health-template/docker-compose.override.yml) foi ajustado para montar o código local do backend no container
- [docker-compose.yml](c:/Users/gabib/smart-health-template/docker-compose.yml) teve o healthcheck corrigido
- [main.py](c:/Users/gabib/smart-health-template/backend/app/main.py) recebeu `GET /health`

Resultado esperado:

- alterações comuns de código Python passam a refletir com reload
- `restart backend` tende a ser suficiente na maioria dos casos

## Integrações consumidas pelo frontend

O `medase` passou a consumir do backend, nesta DEV-03:

- CRUD de pacientes
- histórico clínico do paciente
- exames do paciente
- medicamentos do paciente
- catálogos de exames
- catálogos de medicamentos

Esses contratos foram pensados para uso com `Bearer token` obtido no login real do sistema.

## Validações executadas

- `python -m py_compile` em arquivos alterados do backend
- validação das rotas após ajustes de Swagger

## Passos necessários em ambiente local

### Aplicar migrations

```powershell
docker compose exec backend alembic upgrade head
```

### Reiniciar backend

```powershell
docker compose restart backend
```

### Verificar versão atual de migration

```powershell
docker compose exec backend alembic current
```
