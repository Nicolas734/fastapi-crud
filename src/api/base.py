from fastapi import APIRouter
from api.route_user import router as routes_user
from api.route_login import router as routes_login


api_router = APIRouter()
api_router.include_router(router=routes_user, prefix="/users", tags=["users"])
api_router.include_router(router=routes_login, prefix="", tags=["login"])