from fastapi import APIRouter

from app.api.routes import (
    exam_routes,
    medication_routes,
    patient_routes,
    user_route,
    admin_routes,
    secretaria_routes,
    medico_routes,
    medico_esp_routes
)

api_router = APIRouter()

# Rotas de 'Usuarios'
api_router.include_router(user_route.router)

# Rotas de 'Administradores'
api_router.include_router(admin_routes.router)

# Rotas de 'Médicos'
api_router.include_router(medico_routes.router)

# Rotas de 'Especialidades Médicas'
api_router.include_router(medico_esp_routes.router)

# Rotas de 'Secretárias'
api_router.include_router(secretaria_routes.router)
api_router.include_router(exam_routes.router)
api_router.include_router(medication_routes.router)
api_router.include_router(patient_routes.router)
