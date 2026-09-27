# Dashboard e agenda com dados reais

Os dashboards do MEDASE e a agenda do médico usam a API. Essas páginas não importam mais `store.ts` e não usam dados simulados como fallback.

- `GET /dashboard/`: contagens, pacientes recentes e resultados de IA persistidos.
- `GET /agenda/medicos`: profissionais cadastrados no banco.
- `GET /agenda/`: consultas; médicos veem somente suas consultas, secretárias e superusuários veem a agenda geral.
- `POST /agenda/` e `PUT /agenda/{id}`: agendamento, edição e cancelamento por secretárias/superusuários. O perfil da secretária é obtido do usuário autenticado.

Pacientes totais/ativos usam o cadastro compartilhado já existente. Os mais recentes são ordenados pela data de criação; registros antigos sem data ficam depois dos datados, por ID. “Imagens sem resultado” conta uploads sem resultado de IA persistido, incluindo os não processados ou com falha; não afirma que todos estão na fila. Análises do mês usam America/Belem e somente resultados salvos; médicos veem suas próprias análises, superusuários veem todas, e secretárias não recebem resultados clínicos de IA. Não há conversão de classe celular para risco de câncer, percentuais fictícios de crescimento ou versão/saúde da IA inventadas.

Consultas duram uma hora. A API bloqueia sobreposição de horários do mesmo médico; consultas canceladas não ocupam o horário. Consultas antigas que só têm data continuam preservadas e aparecem separadas, sem inventar um horário. Status não vira “consulta feita” automaticamente pelo passar do tempo. “Em espera” conta consultas com status waiting, não pacientes distintos.

O calendário exibe os horários no fuso do navegador; o resumo diário usa America/Belem. Os dados são consultados ao abrir a página e pelo botão Atualizar dados; a secretária também atualiza após salvar. Erros da API são mostrados com opção de tentar novamente.

Aplicar em outro ambiente:

```bash
docker compose up -d --build db prestart backend
```

Testes:

```bash
docker compose cp backend/dashboard_tests/. backend:/app/dashboard_tests/
docker compose exec backend pytest dashboard_tests --confcutdir=dashboard_tests -q
# No MEDASE
npx tsc --noEmit -p tsconfig.app.json
npm test
npm run build
```

Validação no navegador: dashboard do superusuário, criação e persistência de consulta pela secretária, consulta visível para o médico e estado de falha da API. Dados sintéticos de teste removidos ao final. Dados simulados de outras páginas fora deste escopo não foram migrados para o banco.
