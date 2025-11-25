from typing import Dict, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from pydantic import BaseModel
from src.utils.models import Model, models
from src.tests.response_models import StandardResponse
from src.tests.standard_text_test import StandardTextTest
from src.tests.basic_param_values_test import BasicParamValuesTest
from src.tests.image_urls_test import ImageURLsTest
from src.tests.tool_calling_with_tool_choice_test import ToolCallingWithToolChoiceTest
from src.tests.structured_json_test import StructuredJSONTest
from src.tests.image_base64_test import ImageBase64Test
from src.utils.models import DeploymentKeys


available_tests = [
    "Standard Text Test",
    "Basic Param Values Test",
    "Prompt with Image URLs",
    "Tool calling with tool choice",
    "Structured JSON Output Test",
    # "Prompt with Base64 Image Test",
]


class TestSelections(BaseModel):
    standard_text_test: bool = False
    prompt_with_image_urls: bool = False
    basic_param_values: bool = False
    tool_calling_with_tool_choice: bool = False
    structured_json_test: bool = False
    prompt_with_base64_images: bool = False


def map_test_name_to_field(test_name: str) -> Optional[str]:
    mapping = {
        "Standard Text Test": "standard_text_test",
        "Prompt with Image URLs": "prompt_with_image_urls",
        "Basic Param Values Test": "basic_param_values",
        "Tool calling with tool choice": "tool_calling_with_tool_choice",
        "Structured JSON Output Test": "structured_json_test",
        "Prompt with Base64 Image Test": "prompt_with_base64_images",
    }
    return mapping.get(test_name)


class TestResults(BaseModel):
    standard_text_test: Optional[StandardResponse] = None
    prompt_with_image_urls: Optional[StandardResponse] = None
    basic_param_values: Optional[StandardResponse] = None
    tool_calling_with_tool_choice: Optional[StandardResponse] = None
    structured_json_test: Optional[StandardResponse] = None
    prompt_with_base64_images: Optional[StandardResponse] = None


def run_tests_for_single_model(
    model: Model,
    selections: TestSelections,
    deployment_keys: DeploymentKeys,
    confirmer_model: Optional[str],
) -> Tuple[str, TestResults]:
    """
    Runs the selected tests for a SINGLE model.
    Returns a tuple of (model_name, test_results).
    """
    results = TestResults()

    # --- 1. Initialize Testers based on Capabilities ---

    standard_text_tester = None
    if model.capabilities.standard_text_test:
        standard_text_tester = StandardTextTest(
            models=[model],
            deployment_keys=deployment_keys,
            confirmer_model=confirmer_model,
        )

    basic_param_values_tester = None
    if model.capabilities.basic_param_values:
        basic_param_values_tester = BasicParamValuesTest(
            models=[model],
            deployment_keys=deployment_keys,
            confirmer_model=confirmer_model,
        )

    image_urls_tester = None
    if model.capabilities.prompt_with_image_urls:
        image_urls_tester = ImageURLsTest(
            models=[model],
            deployment_keys=deployment_keys,
            confirmer_model=confirmer_model,
        )

    tool_calling_tester = None
    if model.capabilities.tool_calling_with_tool_choice:
        tool_calling_tester = ToolCallingWithToolChoiceTest(
            models=[model],
            deployment_keys=deployment_keys,
            confirmer_model=confirmer_model,
        )

    structured_json_tester = None
    if model.capabilities.structured_json_test:
        structured_json_tester = StructuredJSONTest(
            models=[model],
            deployment_keys=deployment_keys,
            confirmer_model=confirmer_model,
        )

    # image_base64_tester = None
    # if model.capabilities.prompt_with_base64_images:
    #     image_base64_tester = ImageBase64Test(
    #         models=[model], confirmer_model=confirmer_model
    #     )

    # --- 2. Execute Tests based on Selections ---

    if selections.standard_text_test and standard_text_tester:
        # .test() returns a list, we take the first item [0]
        results.standard_text_test = standard_text_tester.test()[0]

    if selections.basic_param_values and basic_param_values_tester:
        results.basic_param_values = basic_param_values_tester.test()[0]

    if selections.prompt_with_image_urls and image_urls_tester:
        results.prompt_with_image_urls = image_urls_tester.test()[0]

    if selections.tool_calling_with_tool_choice and tool_calling_tester:
        results.tool_calling_with_tool_choice = tool_calling_tester.test()[0]

    if selections.structured_json_test and structured_json_tester:
        results.structured_json_test = structured_json_tester.test()[0]

    # if selections.prompt_with_base64_images and image_base64_tester:
    #    results.prompt_with_base64_images = image_base64_tester.test()[0]

    return model.name, results


def run_selected_tests(
    models: list[Model],
    selections: TestSelections,
    deployment_keys: DeploymentKeys,
    confirmer_model: Optional[str] = "gpt-4.1-nano",
    batch_size: Optional[int] = 5,
) -> Dict[str, TestResults]:
    """
    Runs tests in parallel batches using ThreadPoolExecutor.
    """
    selected_responses = {}

    with ThreadPoolExecutor(max_workers=batch_size) as executor:
        future_to_model = {
            executor.submit(
                run_tests_for_single_model,
                model,
                selections,
                deployment_keys,
                confirmer_model,
            ): model
            for model in models
        }

        for future in as_completed(future_to_model):
            model_obj = future_to_model[future]
            try:
                model_name, result = future.result()
                selected_responses[model_name] = result
            except Exception as exc:
                print(f"Model {model_obj.name} generated an exception: {exc}")
                selected_responses[model_obj.name] = TestResults()

    return selected_responses


def get_available_models() -> list[Model]:
    return models
