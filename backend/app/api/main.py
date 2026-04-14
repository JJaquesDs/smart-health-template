from fastapi import APIRouter

from app.api.routes import (
    exam_routes,
    medication_routes,
    patient_routes,
    user_route,
    admin_routes,
    secretaria_routes
)

api_router = APIRouter()

api_router.include_router(user_route.router)
api_router.include_router(admin_routes.router)
api_router.include_router(secretaria_routes.router)
api_router.include_router(exam_routes.router)
api_router.include_router(medication_routes.router)
api_router.include_router(patient_routes.router)
