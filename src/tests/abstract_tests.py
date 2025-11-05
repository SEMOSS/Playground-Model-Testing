from typing import Optional
from src.clients.clients import get_openai_client, get_semoss_client
from src.utils.models import Model
from src.utils.constants import CREATE_ROOM_PIXEL
from src.pixels.pixel_maker import PixelMaker
from src.confirmations.openai_confirmations import OpenAIConfirmations


class AbstractTests:
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

    def _extract_tool_response(self, response: dict) -> str:
        response_message = response.get("response", None)
        if not response_message:
            raise ValueError("Response message not found")

        return response_message
