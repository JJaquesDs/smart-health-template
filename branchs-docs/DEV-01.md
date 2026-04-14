# DEV-01

## Objetivo

Este documento registra as alterações feitas no backend do `smart-health-template` para suportar:

- expansão do CRUD de usuários
- campos profissionais para médico e admin
- integração com o frontend `medase`
- bootstrap correto do primeiro superusuário
- liberação de CORS para consumo local pelo frontend

## Resumo das mudanças

O backend originalmente tinha um CRUD básico de usuários e rotas separadas por domínio. Para atender o fluxo do `medase`, o domínio `users` foi ajustado para aceitar cadastro real com:

- `email`
- `senha`
- `nome`
- `telefone`
- `role`

E, quando a role for `admin` ou `medico`, também:

- `registro_profissional`
- `especialidade_principal`
- `instituicao`
- `universidade`
- `ano_formacao`
- `residencia_medica`
- `especializacoes`

Também foi necessário corrigir o startup da aplicação e habilitar CORS para o frontend em `http://localhost:5173`.

## Arquivos alterados

### 1. [app/domains/users/models.py](/smart-health-template/backend/app/domains/users/models.py)

Alterações:

- inclusão de novos campos na tabela `usuarios`
- os novos campos adicionados foram:
  - `registro_profissional`
  - `especialidade_principal`
  - `instituicao`
  - `universidade`
  - `ano_formacao`
  - `residencia_medica`
  - `especializacoes`

Impacto:

- a entidade base `Usuario` passou a suportar dados profissionais diretamente
- isso permitiu que o endpoint de criação de usuário atendesse o cadastro vindo do `medase`

### 2. [app/domains/users/schemas.py](/smart-health-template/backend/app/domains/users/schemas.py)

Alterações:

- expansão dos schemas de entrada e saída de usuário
- criação de mixin para dados profissionais
- ajuste dos schemas:
  - `User`
  - `UserPublic`
  - `UserCreate`
  - `UserUpdate`
- inclusão de validação com `model_validator`

Regras adicionadas:

- para `admin` e `medico`, os campos profissionais se tornam obrigatórios
- `especializacoes` deve ter ao menos um item nesses perfis

Impacto:

- o contrato da API passou a refletir o novo cadastro
- o frontend consegue enviar um payload completo e receber o usuário já com estrutura coerente

### 3. [app/domains/users/services.py](/smart-health-template/backend/app/domains/users/services.py)

Alterações:

- expansão da assinatura de `create_user_service()`
- adição da função `validate_professional_profile()`
- adição da função `can_bootstrap_superuser()`
- adição do parâmetro `allow_superuser_bootstrap`
- ajuste de `update_user_service()` para validar alteração de perfil profissional

Regras implementadas:

- validação dos campos profissionais para `admin` e `medico`
- permissão especial para bootstrap do primeiro `superuser`
- manutenção da regra de permissão para criação de `admin` e `superuser`

Impacto:

- o backend passou a aceitar cadastro completo de médico
- o update de usuário passou a manter coerência entre role e campos profissionais
- o startup deixou de quebrar ao tentar criar o primeiro `superuser`

### 4. [app/api/routes/user_route.py](/smart-health-template/backend/app/api/routes/user_route.py)

Alterações:

- a rota `POST /users/` deixou de criar sempre `USER`
- agora usa a `role` enviada no payload
- repassa também todos os campos profissionais para o service

Impacto:

- o endpoint passou a funcionar como ponto de cadastro usado pelo `medase`

### 5. [app/api/routes/admin_routes.py](/smart-health-template/backend/app/api/routes/admin_routes.py)

Alterações:

- a rota de admin passou a validar explicitamente `role == ADMIN`
- repassa os campos profissionais para o `create_user_service()`

Impacto:

- evita payload inconsistente na rota de admin
- mantém o domínio administrativo alinhado com o novo contrato

### 6. [app/core/db.py](/smart-health-template/backend/app/core/db.py)

Alterações:

- ajuste do `init_db()`
- a criação do primeiro superusuário agora usa:
  - `allow_superuser_bootstrap=True`

Impacto:

- a aplicação consegue inicializar mesmo sem usuário autenticado
- essa exceção ficou restrita ao bootstrap inicial

### 7. [app/main.py](/smart-health-template/backend/app/main.py)

Alterações:

- adição de `CORSMiddleware`
- uso de `settings.all_cors_origins`

Configuração aplicada:

- `allow_origins=settings.all_cors_origins`
- `allow_credentials=True`
- `allow_methods=["*"]`
- `allow_headers=["*"]`

Impacto:

- o frontend `medase` em `http://localhost:5173` consegue consumir o backend local
- sem isso, o navegador bloqueava requisições com erro `Failed to fetch`

### 8. [app/alembic/versions/a4d2b5f1c9e3_adiciona_campos_profissionais_em_usuarios.py](/smart-health-template/backend/app/alembic/versions/a4d2b5f1c9e3_adiciona_campos_profissionais_em_usuarios.py)

Alterações:

- migration nova para adicionar os campos profissionais à tabela `usuarios`

Campos adicionados:

- `registro_profissional`
- `especialidade_principal`
- `instituicao`
- `universidade`
- `ano_formacao`
- `residencia_medica`
- `especializacoes`

Impacto:

- persistência real no banco dos novos campos aceitos pela API

## Integração com o frontend `medase`

O frontend `medase` passou a consumir este backend usando:

- `POST /users/` para cadastro
- `POST /users/login` para autenticação
- `GET /users/eu` para recuperação do usuário autenticado

### Contrato usado no cadastro

Payload básico:

```json
{
  "email": "usuario@dominio.com",
  "senha": "senha123",
  "nome": "Nome Sobrenome",
  "telefone": "11999999999",
  "role": "secretaria"
}
```

Payload para médico:

```json
{
  "email": "medico@dominio.com",
  "senha": "senha123",
  "nome": "Nome Sobrenome",
  "telefone": "11999999999",
  "role": "medico",
  "registro_profissional": "CRM123456",
  "especialidade_principal": "Ginecologia",
  "instituicao": "Hospital X",
  "universidade": "Universidade Y",
  "ano_formacao": 2018,
  "residencia_medica": "Residência em Ginecologia",
  "especializacoes": ["Ultrassonografia", "Obstetrícia"]
}
```

### Observações importantes

- o enum de `role` do backend aceita valores em minúsculas:
  - `user`
  - `superuser`
  - `admin`
  - `secretaria`
  - `medico`
- o frontend precisou adequar esse casing para integração correta
- o backend ainda mantém domínios separados para `secretaria` e `medico`, mas o fluxo integrado atual do `medase` foi conectado ao domínio `users`

## Problemas encontrados durante a integração

### 1. CORS bloqueando o navegador

Sintoma:

- `Failed to fetch` no frontend
- `OPTIONS /users/ 405 Method Not Allowed` no backend

Causa:

- ausência de `CORSMiddleware`

Correção:

- adição do middleware em `app/main.py`

### 2. Startup falhando ao criar o primeiro superusuário

Sintoma:

- `HTTPException: 401: Você não tem permissão para criar esse tipo de usuário`
- falha no `init_db()`

Causa:

- o bootstrap do primeiro `superuser` passava pela mesma regra de permissão usada para criação comum

Correção:

- criação da exceção controlada com `allow_superuser_bootstrap=True`

### 3. Role incompatível entre frontend e backend

Sintoma:

- erro de validação:
  - `Input should be 'user', 'superuser', 'admin', 'secretaria' or 'medico'`

Causa:

- o frontend enviava `MEDICO` e `SECRETARIA` em maiúsculas

Correção:

- o frontend `medase` passou a enviar `medico` e `secretaria`

## Estado atual

O backend ficou preparado para:

- cadastrar usuário com dados básicos
- cadastrar médico com dados profissionais
- autenticar por login
- retornar usuário autenticado
- responder ao frontend local com CORS habilitado

## Pontos pendentes de arquitetura

Hoje ainda existe separação entre:

- `usuarios`
- `secretarias`
- `medicos`

Ou seja, a `role` define acesso, mas não cria automaticamente a entidade de domínio correspondente.

Se o projeto evoluir, o próximo ajuste ideal é:

- `role=secretaria` criar `usuario + secretaria`
- `role=medico` criar `usuario + medico`

Assim o endpoint de cadastro fica unificado e o domínio continua consistente.
