from typing import Optional
from src.utils.models import Model
from src.pixels.pixel_maker import PixelSelections
from src.tests.response_models import StandardResponse
from src.tests.abstract_tests import AbstractTests


class BasicParamValuesTest(AbstractTests):
    """
    Basic Param Values Test: Tests the model's response to a prompt with basic parameter values (ie. temperature, max_tokens, top_p).
    """

    def __init__(
        self, models: list[Model], confirmer_model: Optional[str] = "gpt-4.1-nano"
    ):
        super().__init__(models, confirmer_model)

    def test(self) -> list[StandardResponse]:
        responses = []
        for model in self.models:
            selections = PixelSelections(
                room_id=self.room_id,
                model_id=model.id,
                prompt="Tell me a story about World War 2.",
                param_dict={"temperature": 0.7, "max_tokens": 2000},
            )
            pixel = self.pixel_maker.create_ask_playground_pixel(selections)

            try:
                response = self.semoss_client.run_pixel(pixel)
                response = self._extract_text_response(response)

                standard_response_with_confirmation = StandardResponse(
                    model_name=model.name,
                    model_id=model.id,
                    client=model.client,
                    response=response,
                    pixel=[pixel],
                    success=True,
                )
                responses.append(standard_response_with_confirmation)

            except Exception as e:
                standard_response = StandardResponse(
                    model_name=model.name,
                    model_id=model.id,
                    client=model.client,
                    response=str(e),
                    success=False,
                    pixel=[pixel],
                )
                responses.append(standard_response)

        return responses
