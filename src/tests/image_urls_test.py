from typing import List, Optional
from src.utils.models import Model
from src.pixels.pixel_maker import PixelSelections
from src.tests.response_models import StandardResponse
from src.tests.abstract_tests import AbstractTests


class ImageURLsTest(AbstractTests):
    """
    Image URLs Test: Tests the model's ability to process and respond to prompts that include image URLs.
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
                prompt="Describe the image.",
                image_urls=[
                    "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/transformers/tasks/car.jpg?download=true",
                ],
            )
            pixel = self.pixel_maker.create_ask_playground_pixel(selections)

            try:
                response = self.semoss_client.run_pixel(pixel)
                response = self._extract_text_response(response)

                confirmation = self.openai_confirmer.confirm_image_response(response)
                standard_response_with_confirmation = StandardResponse(
                    model_name=model.name,
                    model_id=model.id,
                    client=model.client,
                    response=response,
                    success=confirmation.confirmed,
                    pixel=[pixel],
                    confirmation_response=confirmation.confirmation_response,
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

    def get_example_pixels(self) -> List[str]:
        return [
            'AskPlayground(roomId=["6ad2ebd6-4f4f-4e09-a509-f9acec404afe"], engine=["b0d18f4b-ff2c-4563-8f9d-57efbff53d60"], command=["<encode>Describe the image.</encode>"], url=["https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/transformers/tasks/car.jpg?download=true"])'
        ]
