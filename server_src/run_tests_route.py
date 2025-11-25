import os
from typing import List, Optional
from fastapi import APIRouter, HTTPException
from src.utils.models import Model, get_model_by_id
from src.runners.runners import (
    TestSelections,
    run_selected_tests,
    map_test_name_to_field,
)
from src.utils.models import DeploymentKeys

router = APIRouter()


@router.post("/api/run-tests")
async def run_tests(
    models: List[str],
    tests: List[str],
    confirmer_model: Optional[str] = "gpt-4.1-nano",
    openai_secret_key: Optional[str] = None,
    url: Optional[str] = None,
    access_key: Optional[str] = None,
    secret_key: Optional[str] = None,
):

    deployment_keys = resolve_keys(openai_secret_key, url, access_key, secret_key)

    model_selections: List[Model] = [get_model_by_id(model_id) for model_id in models]
    test_selections = TestSelections()
    for test_name in tests:
        field_name = map_test_name_to_field(test_name)
        if field_name:
            setattr(test_selections, field_name, True)

    results = run_selected_tests(
        model_selections, test_selections, deployment_keys, confirmer_model
    )
    return results


def resolve_keys(
    openai_secret_key: Optional[str] = None,
    url: Optional[str] = None,
    access_key: Optional[str] = None,
    secret_key: Optional[str] = None,
) -> DeploymentKeys:

    openai_secret = openai_secret_key or os.getenv("OPENAI_API_KEY", None)
    deployment_url = url or os.getenv("DEPLOYMENT_URL", None)
    deployment_access_key = access_key or os.getenv("DEPLOYMENT_ACCESS_KEY", None)
    deployment_secret_key = secret_key or os.getenv("DEPLOYMENT_SECRET_KEY", None)

    if (
        not openai_secret
        or not deployment_url
        or not deployment_access_key
        or not deployment_secret_key
    ):
        raise HTTPException(
            status_code=400,
            detail="Missing required deployment keys. Please provide all necessary keys.",
        )
    return DeploymentKeys(
        url=deployment_url,
        access_key=deployment_access_key,
        secret_key=deployment_secret_key,
        openai_secret_key=openai_secret,
    )
