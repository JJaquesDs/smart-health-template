from fastapi import APIRouter

from app.domains.users.schemas import UserPublic

route = APIRouter()

@route.get("/admin")
def rota_admin():
    pass