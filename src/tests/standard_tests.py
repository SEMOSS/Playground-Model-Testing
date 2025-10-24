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
    
    def _extract_tool_response(self, response: dict) -> str:
        response_message = response.get("response", None)
        if not response_message:
            raise ValueError("Response message not found")

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

    def basic_param_values(self) -> list[StandardResponse]:
        responses = []
        for model in self.models:
            selections = PixelSelections(
                room_id=self.room_id,
                model_id=model.id,
                prompt="Tell me a story about World War 2.",
                param_dict={"temperature": 0.7, "max_tokens": 2000, "top_p": 0.9},
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
    
    def tool_calling_with_tool_choice(self) -> list[StandardResponse]:
        responses = []
            
        for model in self.models:
            room_id=self.room_id
            model_id=model.id
            function_name = "get_stock_price"
            selections = PixelSelections(
                room_id=self.room_id,
                model_id=model.id,
                mcp_tool_id="29e9e371-9243-4293-ad3b-4be08ef95ab5",
                prompt="What is the price of META?",
                param_dict={"tool_choice": {"type":"AUTO"}},
            )

            pixel = self.pixel_maker.create_ask_playground_pixel(selections)
            print(f"Running MCP Tool Pixel: {pixel}")

            try:
                ask_playground_response = self.semoss_client.run_pixel(pixel)
                responseMessage = ask_playground_response.get("responseMessage", None)
                tool_response = responseMessage.get("tool_responses", None)
                if tool_response:
                    tool_response = tool_response[0]
                print(f"Tool Response: {tool_response}")
            except Exception as e:
                raise RuntimeError(f"PHASE 1: Failed to run AskPlayground pixel: {e}")

            if tool_response:
                param_values = tool_response.get("arguments", {})
                tool_call_id = tool_response.get("id", None)
                run_mcp_tool_pixel = f'RunMCPTool(project=["29e9e371-9243-4293-ad3b-4be08ef95ab5"], function=["{function_name}"], paramValues=[{param_values}])'

                try:
                    run_mcp_tool_response = self.semoss_client.run_pixel(run_mcp_tool_pixel)
                    if not run_mcp_tool_response:
                        raise ValueError("PHASE 1: Run MCP Tool response is empty")
                except Exception as e:
                    raise RuntimeError(f"PHASE 1: Failed to run MCP Tool pixel: {e}")

                add_tool_execution_pixel = f'AddToolExecution(engine=["{model_id}"], roomId=["{room_id}"], toolId=["{tool_call_id}"], toolName=["{function_name}"], tool_execution_response=[{run_mcp_tool_response}])'

                try:
                    add_tool_execution_response = self.semoss_client.run_pixel(add_tool_execution_pixel)
                    if not add_tool_execution_response:
                        raise ValueError("PHASE 1: Add Tool Execution response is empty")

                    print("Tool execution added successfully:", add_tool_execution_response)
                except Exception as e:
                    raise RuntimeError(f"PHASE 1: Failed to run Add Tool Execution pixel: {e}")

            try:
                if tool_response:
                    response = self._extract_tool_response(add_tool_execution_response)
                else:
                    response = self._extract_text_response(ask_playground_response)

                standard_response_with_confirmation = StandardResponse(
                    model_name=model.name,
                    model_id=model.id,
                    client=model.client,
                    response=response,
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
                )
                responses.append(standard_response)

        return responses
