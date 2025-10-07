from typing import Optional
from src.clients.clients import get_openai_client, get_semoss_client
from src.utils.models import Model
from src.utils.constants import CREATE_ROOM_PIXEL
from src.pixels.pixel_maker import PixelMaker, PixelSelections
from src.tests.response_models import StandardResponse
from src.confirmations.openai_confirmations import OpenAIConfirmations


class StandardTests:
    def __init__(
        self, models: list[Model], confirmer_model: Optional[str] = "gpt-4.1-nano"
    ):
        self.models = models
        self.openai_confirmer = OpenAIConfirmations(model=confirmer_model)
        self.semoss_client = get_semoss_client()
        self.openai_client = get_openai_client()
        self.pixel_maker = PixelMaker()
        self.room_id = self.create_room()

    def create_room(self) -> str:
        room_id = self.semoss_client.run_pixel(CREATE_ROOM_PIXEL).get("roomId", None)
        if not room_id:
            raise ValueError("Failed to create room")
        return room_id

    def _extract_text_response(self, response: dict) -> str:
        response_block = response.get("responseMessage", None)
        if not response_block:
            raise ValueError("Response message not found")
        response_message = response_block.get("content", None)
        if not response_message:
            raise ValueError("Response content not found")

        return response_message

    def standard_text_test(self) -> list[StandardResponse]:
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
                )
                responses.append(standard_response)

        return responses

    def prompt_with_image_urls(self) -> list[StandardResponse]:
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
                )
                responses.append(standard_response)

        return responses
