from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from contextlib import asynccontextmanager

from sqlmodel import Session

from app.core.db import engine, init_db

from app.core.base_exception import AppException

from app.api.main import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """ Função assíncrona para inicializar primeira vez db ao subir aplicação """

    with Session(engine) as session:
        init_db(session)
    yield
    # Se quizer futuramente aqui pode ser feito: fechar conexões, limpar cache, etc.


app = FastAPI(lifespan=lifespan)

app.include_router(api_router)


@app.exception_handler(AppException)
async def app_exception_handler(resquest: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )
