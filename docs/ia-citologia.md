# IA de citologia no MEDASE

O fluxo usa exclusivamente `ia_service/lm/model_vgg_mod.h5` e o mapeamento de `ia_service/lm/classes.json`. A API_COPOSCOPIA não participa desta integração.

## Inicialização

Com Docker Desktop aberto, na raiz do smart-health-template:

```bash
docker compose up -d --build db prestart backend redis worker
docker compose logs -f worker
```

O worker precisa exibir `ready` antes da primeira análise. O modelo recebe RGB 244 × 244; o pré-processamento mantém a divisão dos pixels por 255 utilizada no projeto. O Docker do worker usa Python 3.11, compatível com seu pyproject.toml.

No MEDASE:

```bash
cd /Users/gabstaudt/Projetos/medase
npm install
npm run dev
```

Configure `VITE_API_URL=http://localhost:8000` no frontend. Acesse a tela IA - Detecção com médico ou superusuário. Selecione primeiro um paciente, escolha um JPEG/PNG de até 10 MB e clique em Analisar imagem. A seleção do paciente é obrigatória nas novas análises, para médicos e superusuários. O vínculo fica salvo no exame antes do processamento.

## Rotas utilizadas

1. `POST /exame_imagem/`: multipart com `file`, `tipo=citologia`, `descricao` opcional e `paciente_id` obrigatório. Persiste o exame e devolve `exame_id`.
2. `POST /exame_imagem/{exame_id}/analisar`: envia a tarefa `process_image` ao Celery e devolve `task_id`. Chamadas repetidas reutilizam a tarefa existente. `?reiniciar=true` permite tentar novamente um processamento não concluído.
3. `GET /exame_imagem/resultado/{task_id}`: retorna PENDING, STARTED, RETRY, FAILURE ou SUCCESS. Em SUCCESS, persiste o resultado no PostgreSQL; consultas repetidas não inserem duplicatas e continuam disponíveis depois da expiração do resultado temporário no Redis.
4. `GET /exame_imagem/`: últimos 30 exames visíveis, com resultado salvo quando disponível. Aceita `?paciente_id=ID` para filtrar por paciente e retorna o nome do paciente.
5. `GET /exame_imagem/uploads/{nome}`: download autenticado da imagem.

As rotas exigem Bearer token. Médicos consultam os próprios exames; superusuários podem consultar todos. Nomes de arquivo são gerados pelo servidor. API e worker compartilham `backend/uploads`.

## Resposta e gráfico

O worker envia as probabilidades identificadas pelas classes, evitando que o frontend associe índices a nomes por suposição:

```json
{
  "status": "SUCCESS",
  "classe_predita": "nome retornado pelo modelo",
  "confianca": 0.0,
  "probabilidades": {
    "Dyskeratotic": 0.0,
    "Koilocytotic": 0.0,
    "Metaplastic": 0.0,
    "Parabasal": 0.0,
    "Superficial-Intermediate": 0.0
  }
}
```

Os zeros acima ilustram apenas o formato, não uma previsão. A tela multiplica os valores por 100, mostra gráfico de barras e tabela, destaca a classe predita e permite baixar o JSON. Não transforma classes em risco de câncer nem gera recomendações clínicas. Descrição e paciente são metadados; não entram na inferência do modelo.

A interface consulta a tarefa a cada 1,5 segundo por até 3 minutos. Em caso de demora, é possível consultar novamente no histórico. Confira os logs do worker se a tarefa permanecer na fila. Imagens corrompidas são rejeitadas pelo processamento.

## Banco existente após reversão

Foi mantido um marcador vazio para a revisão `d4e6f8a0b2c3`, pois o banco local ainda apontava para ela mesmo após a reversão dos arquivos. O marcador não recria agenda/dashboard e não remove dados existentes. A revisão `a5c7e9f1b3d5` acrescenta somente os campos desta integração e aumenta o tamanho dos campos de imagem.

Não remova volumes do PostgreSQL para resolver divergências de migração.

## Testes

```bash
# Copiar os testes para o container de desenvolvimento, caso necessário:
docker compose cp backend/ia_tests backend:/app/ia_tests
docker compose exec backend pytest ia_tests --confcutdir=ia_tests -q

# Dentro do MEDASE:
npm test
npm run build
```

A validação mecânica com imagem sintética verifica transporte, inferência e gráfico; não demonstra acurácia clínica. Validação clínica exige imagens apropriadas e rótulos de referência.

Validação realizada em 25/09/2026: 3 testes da API e 7 testes do frontend passaram; `npm run build` passou. No navegador, uma imagem sintética percorreu upload → API → Redis/Celery → modelo → PostgreSQL → gráfico com cinco barras, sem erros JavaScript, e o resultado permaneceu disponível após recarregar. O exame sintético foi removido após a validação.

A checagem TypeScript completa (`npx tsc --noEmit -p tsconfig.app.json`) ainda encontra três erros anteriores em `SecretaryDashboard.tsx` (estado tipado com um nome literal de médica). Eles não pertencem à integração de IA; o build Vite não executa essa checagem.

A ficha do paciente mostra as análises vinculadas e suas probabilidades. O botão Nova análise / consultar histórico abre a tela de IA com esse paciente selecionado. O resultado e o JSON identificam o paciente. Exames antigos sem vínculo continuam consultáveis e são identificados como tal. As permissões existentes foram preservadas: médicos veem suas próprias análises e superusuários veem todas; secretárias não acessam os resultados de IA.
