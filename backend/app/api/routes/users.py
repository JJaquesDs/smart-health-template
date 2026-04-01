from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def listar_usuarios():
    return [{"id": 1, "nome": "Teste"}]

