Backend desenvolvido com **FastAPI**, organizado por **Grupo de Pesquisa Smarth Health**, seguindo boas práticas de arquitetura, segurança e escalabilidade.

---

## Pré-requisitos

Antes de começar, você precisa ter instalado:

- **Python 3.10+**
- **pip**
- **virtualenv**
- **Git**
- **UV**
- Banco de dados (ex: PostgreSQL ou SQLite, conforme configuração)

Verifique:
```bash
python --version
pip --version
```

### Criar Ambiente Virtual

Windows (PowerShell) / CMD

```bash
python -m venv venv
```

Ativar o ambiente virtual

```bash
venv\Scripts\Activate
```

### Após criar o Ambiente Virtual, instale o **UV**, biblioteca necessária para instalar as dependências do projeto

```bash
pip install uv
```

Após instalar o UV, entre no diretório [backend](.backend) onde está o arquivo **pyproject.toml** com as dependências do projeto

CMD
```bash
cd backend
```

#### Nota

Para **desenvolvimento** ultilize essa instalação dos projetos, pois algumas dependências de desenvolvedor estão nesse grupo definidas em **pyproject.toml**.

Essa instalação abrange dependências gerais e de desenvolvimento

```bash
uv pip install -e . --group dev
```

Apenas para dependências gerais e produção

```bash
uv pip install -e .
```

IREI COLOCAR MAIS COISAS PARA RODAR APLICAÇÃO NO AR