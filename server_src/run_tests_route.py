import os
from typing import List, Optional
from fastapi import APIRouter, HTTPException
from src.utils.models import Model, get_model_by_id
from src.runners.runners import (
    TestSelections,
    run_selected_tests,
    map_test_name_to_field,
)

router = APIRouter()


@router.post("/api/run-tests")
async def run_tests(
    models: List[str],
    tests: List[str],
    confirmer_model: Optional[str] = "gpt-4.1-nano",
    secret_key: Optional[str] = None,
):
    is_deployed = os.getenv("is_deployed", "false").lower() == "true"
    env_secret_key = os.getenv("secret_key")

    if is_deployed:
        if not env_secret_key:
            raise HTTPException(
                status_code=500,
                detail="Server configuration error: secret_key not set in environment.",
            )

        if secret_key != env_secret_key:
            raise HTTPException(
                status_code=401, detail="Unauthorized: Invalid or missing secret key."
            )

    model_selections: List[Model] = [get_model_by_id(model_id) for model_id in models]
    test_selections = TestSelections()
    for test_name in tests:
        field_name = map_test_name_to_field(test_name)
        if field_name:
            setattr(test_selections, field_name, True)

    results = run_selected_tests(model_selections, test_selections, confirmer_model)
    return results
