FROM python:3.11-slim

WORKDIR /app

# instalar uv
RUN pip install uv

# copiar arquivos de dependência
COPY pyproject.toml uv.lock ./

# instalar dependências
RUN python -m uv sync --frozen

# copiar código do projeto
COPY . .

# rodar worker (recomendado para IA)
CMD ["python", "-m", "uv", "run", "celery", "-A", "app.core.worker.celery_app", "worker", "--loglevel=info"]