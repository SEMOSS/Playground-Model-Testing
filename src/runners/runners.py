from typing import Dict, Optional
from src.utils.models import Model, models
from src.tests.response_models import StandardResponse
from src.tests.standard_text_test import StandardTextTest
from src.tests.basic_param_values_test import BasicParamValuesTest
from src.tests.image_urls_test import ImageURLsTest
from src.tests.tool_calling_with_tool_choice_test import ToolCallingWithToolChoiceTest
from src.tests.structured_json_test import StructuredJSONTest
from src.tests.image_base64_test import ImageBase64Test
from pydantic import BaseModel

available_tests = [
    "Standard Text Test",
    "Basic Param Values Test",
    "Prompt with Image URLs",
    "Tool calling with tool choice",
    "Structured JSON Output Test",
    "Prompt with Base64 Image Test",
]


class TestSelections(BaseModel):
    standard_text_test: bool = False
    prompt_with_image_urls: bool = False
    basic_param_values: bool = False
    tool_calling_with_tool_choice: bool = False
    structured_json_test: bool = False
    prompt_with_base64_images: bool = False


class TestResults(BaseModel):
    standard_text_test: Optional[StandardResponse] = None
    prompt_with_image_urls: Optional[StandardResponse] = None
    basic_param_values: Optional[StandardResponse] = None
    tool_calling_with_tool_choice: Optional[StandardResponse] = None
    structured_json_test: Optional[StandardResponse] = None
    prompt_with_base64_images: Optional[StandardResponse] = None


def run_selected_tests(
    models: list[Model],
    selections: TestSelections,
    confirmer_model: Optional[str] = "gpt-4.1-nano",
) -> Dict[str, TestResults]:
    selected_responses = {}
    for model in models:
        results = TestResults()

        standard_text_tester = StandardTextTest(
            models=[model], confirmer_model=confirmer_model
        )
        basic_param_values_tester = BasicParamValuesTest(
            models=[model], confirmer_model=confirmer_model
        )
        image_urls_tester = ImageURLsTest(
            models=[model], confirmer_model=confirmer_model
        )
        tool_calling_with_tool_choice_tester = ToolCallingWithToolChoiceTest(
            models=[model], confirmer_model=confirmer_model
        )
        structured_json_tester = StructuredJSONTest(
            models=[model], confirmer_model=confirmer_model
        )
        image_base64_tester = ImageBase64Test(
            models=[model], confirmer_model=confirmer_model
        )

        if selections.standard_text_test:
            results.standard_text_test = standard_text_tester.test()[0]
        if selections.basic_param_values:
            results.basic_param_values = basic_param_values_tester.test()[0]
        if selections.prompt_with_image_urls:
            results.prompt_with_image_urls = image_urls_tester.test()[0]
        if selections.tool_calling_with_tool_choice:
            results.tool_calling_with_tool_choice = (
                tool_calling_with_tool_choice_tester.test()[0]
            )
        if selections.structured_json_test:
            results.structured_json_test = structured_json_tester.test()[0]
        if selections.prompt_with_base64_images:
            results.prompt_with_base64_images = (
                image_base64_tester.prompt_with_base64_images()[0]
            )
        selected_responses[model.name] = results
    return selected_responses


def get_available_models() -> list[Model]:
    return models
