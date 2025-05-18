from fastapi import APIRouter
from .views import core_router

router = APIRouter(prefix="/todos", tags=["Todos"])
router.include_router(core_router)