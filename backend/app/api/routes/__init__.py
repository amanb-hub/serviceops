from fastapi import APIRouter

from app.api.routes import auth, cities, clients, health, users, vehicles

api_router = APIRouter(prefix="/api")
api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(clients.router)
api_router.include_router(cities.router)
api_router.include_router(users.router)
api_router.include_router(vehicles.router)
