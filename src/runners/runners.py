from typing import Dict, Optional
from src.utils.models import Model
from src.tests.response_models import StandardResponse
from src.tests.standard_tests import StandardTests
from pydantic import BaseModel


class TestSelections(BaseModel):
    standard_text_test: bool = False
    prompt_with_image_urls: bool = False


class TestResults(BaseModel):
    standard_text_test: Optional[StandardResponse] = None
    prompt_with_image_urls: Optional[StandardResponse] = None


def run_selected_tests(
    models: list[Model],
    selections: TestSelections,
    confirmer_model: Optional[str] = "gpt-4.1-nano",
) -> Dict[str, TestResults]:
    selected_responses = {}
    for model in models:
        results = TestResults()
        tester = StandardTests(models=[model], confirmer_model=confirmer_model)
        if selections.standard_text_test:
            results.standard_text_test = tester.standard_text_test()
        if selections.prompt_with_image_urls:
            results.prompt_with_image_urls = tester.prompt_with_image_urls()
        selected_responses[model.name] = results
    return selected_responses


def run_full_test_suite(
    models: list[Model], confirmer_model: Optional[str] = "gpt-4.1-nano"
) -> Dict[str, TestResults]:
    full_suite_responses = {}
    for model in models:
        results = TestResults()
        tester = StandardTests(models=models, confirmer_model=confirmer_model)
        results.standard_text_test = tester.standard_text_test()
        results.prompt_with_image_urls = tester.prompt_with_image_urls()
        full_suite_responses[model.name] = results
    return full_suite_responses
