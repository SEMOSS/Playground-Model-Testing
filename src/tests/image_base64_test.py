from typing import Optional
from src.utils.models import Model
from src.pixels.pixel_maker import PixelSelections
from src.tests.response_models import StandardResponse
from src.tests.abstract_tests import AbstractTests


class ImageBase64Test(AbstractTests):
    """
    Image Base64 Test: Tests the model's ability to process and respond to prompts that include image as base64.
    """

    def __init__(
        self, models: list[Model], confirmer_model: Optional[str] = "gpt-4.1-nano"
    ):
        super().__init__(models, confirmer_model)

    def prompt_with_base64_images(self) -> list[StandardResponse]:
        import base64

        image_path = "test-images\\car.jpg"
        with open(image_path, "rb") as f:
            encoded_image = base64.b64encode(f.read()).decode("utf-8")

        responses = []
        for model in self.models:
            selections = PixelSelections(
                room_id=self.room_id,
                model_id=model.id,
                prompt="Describe this encoded image.",
                image_base64=[encoded_image],
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
                    pixel=[pixel],
                    success=confirmation.confirmed,
                    confirmation_response=confirmation.confirmation_response,
                )
                responses.append(standard_response_with_confirmation)

            except Exception as e:
                standard_response = StandardResponse(
                    model_name=model.name,
                    model_id=model.id,
                    client=model.client,
                    response=str(e),
                    pixel=[pixel],
                    success=False,
                )
                responses.append(standard_response)

        return responses
