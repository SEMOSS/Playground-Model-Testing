from pydantic import BaseModel
from typing import Optional


class PixelSelections(BaseModel):
    room_id: str
    model_id: str
    prompt: str
    context: Optional[str] = None
    image_urls: Optional[list[str]] = None
    image_base64: Optional[list[str]] = None
    mcp_tool_id: str = None
    param_dict: Optional[dict] = (
        None  # TODO Make a model for the commonly used params so we can test them individually
    )


class PixelMaker:

    def create_ask_playground_pixel(self, selections: PixelSelections) -> str:

        pixel = f'AskPlayground(roomId=["{selections.room_id}"], engine=["{selections.model_id}"], command=["<encode>{selections.prompt}</encode>"]'
        if selections.context:
            pixel = self._with_context(pixel, selections.context)
        if selections.image_urls:
            pixel = self._with_image_urls(pixel, selections.image_urls)
        if selections.image_base64:
            pixel = self._with_image_base64(pixel, selections.image_base64)
        if selections.mcp_tool_id:
            pixel = self._with_mcp_tool_id(pixel, selections.mcp_tool_id)
        if selections.param_dict:
            params = ",".join(
                [
                    f'"{key}": {repr(value)}'
                    for key, value in selections.param_dict.items()
                ]
            )
            pixel += f", paramValues=[{{{params}}}]"

        pixel += ")"
        return pixel

    def _with_context(self, pixel: str, context: str) -> str:
        return pixel + f', context=["<encode>{context}</encode>"]'

    def _with_image_urls(self, pixel: str, image_urls: list[str]) -> str:
        urls = '","'.join(image_urls)
        return pixel + f', url=["{urls}"]'

    def _with_image_base64(self, pixel: str, image_base64: list[str]) -> str:
        base64s = '","'.join(image_base64)
        return pixel + f', image=["{base64s}"]'
    
    def _with_mcp_tool_id(self, pixel: str, mcp_tool_id: str) -> str:
        return pixel + f', mcpToolID=["{mcp_tool_id}"]'
