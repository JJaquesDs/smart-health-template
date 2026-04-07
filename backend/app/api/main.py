from fastapi import APIRouter

from app.api.routes import (
    user_route,
    admin_routes,
    secretaria_routes
)

api_router = APIRouter()

api_router.include_router(user_route.router)
api_router.include_router(admin_routes.router)
api_router.include_router(secretaria_routes.router)
