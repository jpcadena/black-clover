"""
API script
"""
from fastapi import APIRouter
from app.api.api_v1.router import authentication, student

api_router: APIRouter = APIRouter()
api_router.include_router(authentication.router)
api_router.include_router(student.router)
# api_router.include_router(utils.router)
