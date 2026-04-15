from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager
from sqlmodel import Session

from app.core.db import engine, init_db
from app.core.config import settings

from app.api.main import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """ Função assíncrona para inicializar primeira vez db ao subir aplicação """

    with Session(engine) as session:
        init_db(session)
    yield
    # Se quizer futuramente aqui pode ser feito: fechar conexões, limpar cache, etc.

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.all_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
