from fastapi import APIRouter
from api.route_user import router

api_router = APIRouter()
api_router.include_router(router=router, prefix="/users", tags=["users"])