from typing import List
from fastapi import APIRouter
from src.utils.models import get_models, Model
from src.runners.runners import available_tests
from pydantic import BaseModel


class ModelsAndTests(BaseModel):
    models: List[Model]
    available_tests: List[str]


router = APIRouter()


@router.get("/api/get-models-and-tests", response_model=ModelsAndTests)
async def get_models_and_tests():
    models = get_models()
    return ModelsAndTests(models=models, available_tests=available_tests)
