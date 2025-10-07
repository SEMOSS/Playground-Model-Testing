from src.runners.runners import run_selected_tests, TestSelections
from src.utils.models import models
from pprint import pprint

if __name__ == "__main__":
    selections = TestSelections(standard_text_test=True, prompt_with_image_urls=True)
    results = run_selected_tests(models, selections)
    pprint(results)
