from fastapi import APIRouter
from .attendence import router as attendence_router

router = APIRouter()

router.include_router(attendence_router, tags=["attendence"], prefix="/attendence")
