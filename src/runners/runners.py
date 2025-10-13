from typing import Dict, Optional, List
from src.utils.models import Model, models
from src.tests.response_models import StandardResponse
from src.tests.standard_tests import StandardTests
from pydantic import BaseModel

available_tests = [
    "Standard Text Test",
    "Prompt with Image URLs",
    "Basic Param Values Test",
    "Tool Calling Test",
]


class TestSelections(BaseModel):
    standard_text_test: bool = False
    prompt_with_image_urls: bool = False
    basic_param_values: bool = False
    test_tool_calling: bool = False


class TestResults(BaseModel):
    standard_text_test: Optional[StandardResponse] = None
    prompt_with_image_urls: Optional[StandardResponse] = None
    basic_param_values: Optional[StandardResponse] = None
    test_tool_calling: Optional[List[StandardResponse]] = None


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
            results.standard_text_test = tester.standard_text_test()[0]
        if selections.prompt_with_image_urls:
            results.prompt_with_image_urls = tester.prompt_with_image_urls()[0]
        if selections.basic_param_values:
            results.basic_param_values = tester.basic_param_values()[0]
        if selections.test_tool_calling:
            results.test_tool_calling = tester.test_tool_calling()

        selected_responses[model.name] = results
    return selected_responses


def run_full_test_suite(
    models: list[Model], confirmer_model: Optional[str] = "gpt-4.1-nano"
) -> Dict[str, TestResults]:
    full_suite_responses = {}
    for model in models:
        results = TestResults()
        tester = StandardTests(models=[model], confirmer_model=confirmer_model)
        results.standard_text_test = tester.standard_text_test()[0]
        results.prompt_with_image_urls = tester.prompt_with_image_urls()[0]
        results.basic_param_values = tester.basic_param_values()[0]
        results.test_tool_calling = tester.test_tool_calling()
        full_suite_responses[model.name] = results
    return full_suite_responses


def get_available_models() -> list[Model]:
    return models
