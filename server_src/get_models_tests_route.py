import os
from typing import List, Optional
from fastapi import APIRouter
from src.utils.models import get_models, Model
from src.runners.runners import available_tests
from pydantic import BaseModel


class ModelsAndTests(BaseModel):
    models: List[Model]
    available_tests: List[str]
    deployment_url: Optional[str] = None
    deployment_access_key: Optional[str] = None
    deployment_secret_key: Optional[str] = None


router = APIRouter()


@router.get("/api/get-models-and-tests", response_model=ModelsAndTests)
async def get_models_and_tests():
    models = get_models()
    return ModelsAndTests(
        models=models,
        available_tests=available_tests,
        deployment_url=os.getenv("DEPLOYMENT_URL"),
        deployment_access_key=os.getenv("DEPLOYMENT_ACCESS_KEY"),
        deployment_secret_key=os.getenv("DEPLOYMENT_SECRET_KEY"),
    )
