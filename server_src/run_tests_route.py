from typing import List, Optional
from fastapi import APIRouter
from src.utils.models import get_models, Model, get_model_by_id
from src.runners.runners import (
    available_tests,
    TestSelections,
    TestResults,
    run_selected_tests,
    map_test_name_to_field,
)
from pydantic import BaseModel

router = APIRouter()


@router.post("/api/run-tests")
async def run_tests(
    models: List[str], tests: List[str], confirmer_model: Optional[str] = "gpt-4.1-nano"
):
    model_selections: List[Model] = [get_model_by_id(model_id) for model_id in models]
    test_selections = TestSelections()
    for test_name in tests:
        field_name = map_test_name_to_field(test_name)
        if field_name:
            setattr(test_selections, field_name, True)

    results = run_selected_tests(model_selections, test_selections, confirmer_model)
    return results
