from fastapi import FastAPI
from {{ project_name }}.database import engine
from {{ project_name }}.settings import settings
from core import models as core_models
# from users import models as users_models

from core.urls import core_router
# from users.urls import users_router

core_models.Base.metadata.create_all(bind=engine)
# users_models.Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)
app.include_router(core_router)
# app.include_router(users_router)
