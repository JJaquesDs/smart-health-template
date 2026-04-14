# DEV-02

## Escopo

Este documento registra a implementação do catálogo de exames e medicamentos no backend do `smart-health-template`, além das integrações consumidas pelo frontend `medase`.

O objetivo foi disponibilizar um CRUD autenticado para:

- catálogo de exames
- catálogo de medicamentos

Esses catálogos foram pensados para uso operacional do sistema e para consumo direto pela interface médica do `medase`.

## Rotas novas

### Exames

Prefixo: `/exames`

Endpoints:

- `POST /exames/`
- `GET /exames/`
- `GET /exames/{exam_id}`
- `PUT /exames/{exam_id}`
- `DELETE /exames/{exam_id}`

Permissão:

- `medico`
- `admin`
- `superuser`

Contrato principal:

- `nome`
- `categoria`: `laboratorial | imagem | funcional | outros`
- `descricao`
- `preco`
- `preparacao`
- `observacoes`
- `ativo`

### Medicamentos

Prefixo: `/medicamentos`

Endpoints:

- `POST /medicamentos/`
- `GET /medicamentos/`
- `GET /medicamentos/{medication_id}`
- `PUT /medicamentos/{medication_id}`
- `DELETE /medicamentos/{medication_id}`

Permissão:

- `medico`
- `admin`
- `superuser`

Contrato principal:

- `nome`
- `principio_ativo`
- `dosagem`
- `forma_farmaceutica`: `comprimido | capsula | injetavel | liquido | topico | outros`
- `fabricante`
- `descricao`
- `contraindicacoes`
- `efeitos_colaterais`
- `ativo`

## Arquivos alterados no backend

### Exames

- [models.py](C:/Users/gabib/smart-health-template/backend/app/domains/exames/clinicos/models.py)
  - inclusão do modelo de catálogo de exames
- [schemas.py](C:/Users/gabib/smart-health-template/backend/app/domains/exames/clinicos/schemas.py)
  - schemas de criação, atualização e resposta pública
- [repository.py](C:/Users/gabib/smart-health-template/backend/app/domains/exames/clinicos/repository.py)
  - operações de persistência do catálogo
- [services.py](C:/Users/gabib/smart-health-template/backend/app/domains/exames/clinicos/services.py)
  - regras de CRUD

### Medicamentos

- [models.py](C:/Users/gabib/smart-health-template/backend/app/domains/medicamentos/models.py)
  - inclusão do modelo de catálogo de medicamentos
- [schemas.py](C:/Users/gabib/smart-health-template/backend/app/domains/medicamentos/schemas.py)
  - schemas de criação, atualização e resposta pública
- [repository.py](C:/Users/gabib/smart-health-template/backend/app/domains/medicamentos/repository.py)
  - operações de persistência do catálogo
- [services.py](C:/Users/gabib/smart-health-template/backend/app/domains/medicamentos/services.py)
  - regras de CRUD

### API

- [exam_routes.py](C:/Users/gabib/smart-health-template/backend/app/api/routes/exam_routes.py)
  - rotas REST de catálogo de exames
  - proteção por role
  - documentação Swagger com `summary`, `description`, `responses` e `Path(...)`
- [medication_routes.py](C:/Users/gabib/smart-health-template/backend/app/api/routes/medication_routes.py)
  - rotas REST de catálogo de medicamentos
  - proteção por role
  - documentação Swagger com `summary`, `description`, `responses` e `Path(...)`
- [main.py](C:/Users/gabib/smart-health-template/backend/app/api/main.py)
  - inclusão dos routers novos

### Infra

- [b7c1e4a2d9f0_cria_catalogos_de_exames_e_medicamentos.py](C:/Users/gabib/smart-health-template/backend/app/alembic/versions/b7c1e4a2d9f0_cria_catalogos_de_exames_e_medicamentos.py)
  - migration das tabelas de catálogo
- [main.py](C:/Users/gabib/smart-health-template/backend/app/main.py)
  - adição de `GET /health`
  - manutenção do `CORSMiddleware`
- [docker-compose.yml](C:/Users/gabib/smart-health-template/docker-compose.yml)
  - healthcheck corrigido para `GET /health`
- [docker-compose.override.yml](C:/Users/gabib/smart-health-template/docker-compose.override.yml)
  - bind mounts do código do backend para facilitar desenvolvimento sem rebuild completo

## Estrutura de dados

### Catálogo de exames

Campos persistidos:

- `exame_id`
- `nome`
- `categoria`
- `descricao`
- `preco`
- `preparacao`
- `observacoes`
- `ativo`

### Catálogo de medicamentos

Campos persistidos:

- `medicamento_id`
- `nome`
- `principio_ativo`
- `dosagem`
- `forma_farmaceutica`
- `fabricante`
- `descricao`
- `contraindicacoes`
- `efeitos_colaterais`
- `ativo`

## Segurança e autenticação

As rotas usam o mesmo mecanismo de autenticação do sistema:

- login em `POST /users/login`
- token `Bearer`
- usuário atual resolvido por dependência FastAPI

O controle de acesso é feito por `exigir_role(...)`.

Para os catálogos, a regra final ficou:

- médico autenticado pode acessar
- admin autenticado pode acessar
- superuser autenticado pode acessar

Isso foi necessário porque o módulo de catálogo foi destinado ao fluxo clínico do médico no frontend.

## Integração com o frontend `medase`

O frontend consome diretamente estas rotas:

- `GET /exames/`
- `POST /exames/`
- `PUT /exames/{id}`
- `DELETE /exames/{id}`
- `GET /medicamentos/`
- `POST /medicamentos/`
- `PUT /medicamentos/{id}`
- `DELETE /medicamentos/{id}`

Todas as chamadas exigem:

- `Authorization: Bearer <token>`

O token é gerado no login e armazenado no frontend.

## Swagger

As rotas foram documentadas para aparecer corretamente em `/docs`.

Informações adicionadas:

- resumo da operação
- descrição de negócio
- descrição dos parâmetros de rota
- respostas esperadas

Isso foi feito para facilitar:

- teste manual via Swagger UI
- validação do contrato pelo frontend
- manutenção posterior da API

## Fluxo de uso esperado

1. Usuário médico faz login.
2. Backend retorna `access_token`.
3. Frontend armazena o token.
4. Tela de catálogo faz chamadas autenticadas.
5. Backend valida a role.
6. CRUD é executado conforme a rota chamada.

## Observações de ambiente

Para desenvolvimento local, o backend foi ajustado para reduzir a necessidade de rebuild completo:

- o container usa `fastapi run --reload`
- o código da pasta `backend/app` agora é montado diretamente no container no override local

Na prática:

- alterações em código Python tendem a refletir sem `docker compose down`
- mudanças em dependências, imagem ou estrutura de build ainda exigem rebuild

## Validações executadas

- `python -m py_compile` nas rotas novas
- verificação do carregamento dos routers
- ajuste do healthcheck para evitar falso erro de serviço

## Pendências operacionais

- aplicar migration no banco, se ainda não aplicada
- reiniciar o backend para garantir que as rotas novas e permissões estejam carregadas
