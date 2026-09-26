# Cadastro de pacientes

Médicos, secretárias e superusuários podem cadastrar, consultar e editar pacientes. Superusuários também podem acessar os campos e registros clínicos. As restrições de campos clínicos da secretária foram preservadas.

CPF: POST e PUT aceitam 11 dígitos ou `000.000.000-00`, validam os dígitos verificadores e armazenam somente números. O banco possui um índice único que ignora pontuação. CPFs antigos formatados são normalizados pela migração; valores antigos inválidos não são excluídos e precisam ser corrigidos ao editar. Se outro ambiente tiver CPFs equivalentes duplicados, a migração será revertida e será necessário resolver os cadastros duplicados antes de executá-la novamente.

`created_at` e `updated_at` são timestamps com fuso horário gerados no PostgreSQL. Um trigger atualiza `updated_at` e preserva `created_at` em alterações. Datas históricas desconhecidas permanecem nulas; a interface mostra “Não registrada”. Não é usada a data de hoje como se fosse a data original do cadastro.

`status` vem do banco (`active` ou `inactive`), com padrão `active` para novos cadastros e registros existentes. Pode ser alterado via PUT; editar um cadastro não reativa automaticamente um paciente inativo.

Aplicar em outro ambiente:

```bash
docker compose up -d --build db prestart backend
```

Testes de integração com rollback:

```bash
docker compose cp backend/patient_tests backend:/app/patient_tests
docker compose exec backend pytest patient_tests --confcutdir=patient_tests -q
```

Validações de entrada (POST e PUT): campos obrigatórios não aceitam nulo ou somente espaços; textos são aparados; limites dos campos VARCHAR seguem o banco; nascimento exige uma data real no formato AAAA-MM-DD e não pode estar no futuro. Atualizações parciais continuam permitidas.

Para criar outro acesso de demonstração de secretária (gera e exibe uma nova senha, sem modificar contas existentes):

```bash
docker compose exec backend python scripts/seed_secretaria.py
```

O seed cria tanto o usuário quanto o registro profissional de secretária, com dados sintéticos. As credenciais não são gravadas no código.
