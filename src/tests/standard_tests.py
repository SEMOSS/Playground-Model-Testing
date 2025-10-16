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

    def test_tool_calling(self) -> list[StandardResponse]:
        responses = []

        engine_id = "692215ed-b693-45df-a464-56a99d397d27"
        mcpToolID = "29e9e371-9243-4293-ad3b-4be08ef95ab5"
        room_id = self.room_id

        def log_tool_error(responses, response_text):
            standard_response = StandardResponse(
                model_name="ToolCall-Test",
                model_id=mcpToolID,
                client="SEMOSS",
                response=response_text,
                success=False,
            )
            responses.append(standard_response)
            return responses

        # PHASE 1: Single tool call
        # STEP 1: AskPlayground with mcpToolID to get tool call details
        ask_playground_pixel = f'AskPlayground(roomId=["{room_id}"], engine=["{engine_id}"], mcpToolID=["{mcpToolID}"], command=["What is stock price of META?"])'

        try:
            ask_playground_response = self.semoss_client.run_pixel(ask_playground_pixel)
            tool_response = ask_playground_response.get("responseMessage", None).get(
                "tool_responses", None
            )[0]
        except Exception as e:
            response_text = f"PHASE 1: Failed to run AskPlayground pixel: {e}"
            return log_tool_error(responses, response_text)

        param_values = tool_response.get("arguments", {})
        tool_call_id = tool_response.get("id", None)

        # STEP 2: RunMCPTool with extracted parameters
        run_mcp_tool_pixel = f'RunMCPTool(project=["{mcpToolID}"], function=["get_stock_price"], paramValues=[{param_values}])'

        try:
            run_mcp_tool_response = self.semoss_client.run_pixel(run_mcp_tool_pixel)
            if not run_mcp_tool_response:
                return log_tool_error(
                    responses, "PHASE 1: Run MCP Tool response is empty"
                )
        except Exception as e:
            return log_tool_error(
                responses, f"PHASE 1: Failed to run MCP Tool pixel: {e}"
            )

        add_tool_execution_pixel = f'AddToolExecution(engine=["{engine_id}"], roomId=["{room_id}"], toolId=["{tool_call_id}"], toolName=["get_stock_price"], tool_execution_response=[{run_mcp_tool_response}])'

        try:
            add_tool_execution_response = self.semoss_client.run_pixel(
                add_tool_execution_pixel
            )
            if not add_tool_execution_response:
                return log_tool_error(
                    responses, "PHASE 1: Add Tool Execution response is empty"
                )

            standard_response = StandardResponse(
                model_name="ToolCall-Test",
                model_id=mcpToolID,
                client="SEMOSS",
                response=f"Tool execution added successfully: {add_tool_execution_response}",
                success=True,
            )
            responses.append(standard_response)
        except Exception as e:
            return log_tool_error(
                responses, f"PHASE 1: Failed to run Add Tool Execution pixel: {e}"
            )

        # PHASE 2: Multiple tool calls
        ask_playground_pixel2 = f'AskPlayground(roomId=["{room_id}"], engine=["{engine_id}"], mcpToolID=["{mcpToolID}"], command=["What about TSLA and MSFT?"])'

        try:
            ask_playground_response = self.semoss_client.run_pixel(
                ask_playground_pixel2
            )
            tool_responses = ask_playground_response.get("responseMessage", None).get(
                "tool_responses", None
            )
        except Exception as e:
            return log_tool_error(
                responses, f"PHASE 2: Failed to run AskPlayground pixel: {e}"
            )

        if not isinstance(tool_responses, list):
            return log_tool_error(
                responses,
                "PHASE 2: Tool response is not a list, expected multiple tool calls",
            )

        if len(tool_responses) < 2:
            return log_tool_error(
                responses, f"PHASE 2: Expected 2 tool calls, got {len(tool_responses)}"
            )

        tool_execution_results = []

        for i, tool_response in enumerate(tool_responses):
            tool_call_id = tool_response.get("id", None)
            param_values = tool_response.get("arguments", {})

            standard_response = StandardResponse(
                model_name="ToolCall-Test",
                model_id=mcpToolID,
                client="SEMOSS",
                response=f"Processing tool call {i+1}: ID={tool_call_id}, Params={param_values}",
                success=True,
            )

            responses.append(standard_response)

            run_mcp_tool_pixel = f'RunMCPTool(project=["{mcpToolID}"], function=["get_stock_price"], paramValues=[{param_values}])'

            try:
                run_mcp_tool_response = self.semoss_client.run_pixel(run_mcp_tool_pixel)
                if not run_mcp_tool_response:
                    return log_tool_error(
                        responses, f"PHASE 2 TOOL {i+1}: Run MCP Tool response is empty"
                    )
            except Exception as e:
                return log_tool_error(
                    responses, f"PHASE 2 TOOL {i+1}: Failed to run MCP Tool pixel: {e}"
                )

            tool_execution_results.append(
                {"tool_call_id": tool_call_id, "tool_response": run_mcp_tool_response}
            )

        for i, execution_result in enumerate(tool_execution_results):
            add_tool_execution_pixel = f'AddToolExecution(engine=["{engine_id}"], roomId=["{room_id}"], toolId=["{execution_result["tool_call_id"]}"], toolName=["get_stock_price"], tool_execution_response=[{execution_result["tool_response"]}])'

            try:
                add_tool_execution_response = self.semoss_client.run_pixel(
                    add_tool_execution_pixel
                )
                if not add_tool_execution_response:
                    return log_tool_error(
                        responses,
                        f"PHASE 2 TOOL {i+1}: Add Tool Execution response is empty",
                    )

                standard_response = StandardResponse(
                    model_name="ToolCall-Test",
                    model_id=mcpToolID,
                    client="SEMOSS",
                    response=f"Tool execution {i+1} added successfully: {add_tool_execution_response}",
                    success=True,
                )
                responses.append(standard_response)

            except Exception as e:
                return log_tool_error(
                    responses,
                    f"PHASE 2 TOOL {i+1}: Failed to run Add Tool Execution pixel: {e}",
                )

        standard_response = StandardResponse(
            model_name="ToolCall-Test",
            model_id=mcpToolID,
            client="SEMOSS",
            response="All tool executions completed successfully!",
            success=True,
        )
        responses.append(standard_response)

        # Phase 3: Summmary
        ask_playground_pixel = f'AskPlayground(roomId=["{room_id}"], engine=["{engine_id}"], command=["Can you create a summary of the stock prices we discussed?"])'
        try:
            ask_playground_response = self.semoss_client.run_pixel(ask_playground_pixel)
            text_response = ask_playground_response.get("responseMessage", None)
            if not text_response:
                return log_tool_error(
                    responses, "PHASE 3: AskPlayground response is empty"
                )
            standard_response = StandardResponse(
                model_name="ToolCall-Test",
                model_id=mcpToolID,
                client="SEMOSS",
                response=f"Summary response: {text_response}",
                success=True,
            )
            responses.append(standard_response)
        except Exception as e:
            return log_tool_error(
                responses, f"PHASE 3: Failed to run AskPlayground pixel: {e}"
            )
        return responses
