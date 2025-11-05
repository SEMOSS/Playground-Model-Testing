from typing import Optional
from src.utils.models import Model
from src.pixels.pixel_maker import PixelSelections
from src.tests.response_models import StandardResponse
from src.tests.abstract_tests import AbstractTests


class StandardTextTest(AbstractTests):
    """
    Standard Text Test: Most basic test to check if the model can respond to a simple text prompt.
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
                prompt="What is the capital of France?",
            )
            pixel = self.pixel_maker.create_ask_playground_pixel(selections)

            try:
                response = self.semoss_client.run_pixel(pixel)
                standard_response = StandardResponse(
                    model_name=model.name,
                    model_id=model.id,
                    client=model.client,
                    response=self._extract_text_response(response),
                    pixel=[pixel],
                    success=True,
                )
                responses.append(standard_response)
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
