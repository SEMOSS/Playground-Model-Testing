from typing import Optional
from src.utils.models import Model
from src.pixels.pixel_maker import PixelSelections
from src.tests.response_models import StandardResponse
from src.tests.abstract_tests import AbstractTests
from src.utils.models import DeploymentKeys


class ToolCallingWithToolChoiceTest(AbstractTests):
    """
    Tool Calling with Tool Choice Test: Tests the model's ability to call a tool with tool choice set to AUTO.
    """

    def __init__(
        self,
        models: list[Model],
        deployment_keys: DeploymentKeys,
        confirmer_model: Optional[str] = "gpt-4.1-nano",
    ):
        super().__init__(models, deployment_keys, confirmer_model)

    def test(self) -> list[StandardResponse]:
        responses = []

        for model in self.models:
            room_id = self.room_id
            model_id = model.id
            instructions = {
                "instructions": "",
                "mcp": [
                    {
                        "id": "29e9e371-9243-4293-ad3b-4be08ef95ab5",
                        "type": "PROJECT",
                        "name": "MCP",
                    }
                ],
                "temperature": 0.3,
            }

            update_room_pixel = (
                f'UpdateRoomOptions(roomId="{room_id}", roomOptions=[{instructions}]);'
            )

            try:
                update_room_response = self.semoss_client.run_pixel(update_room_pixel)
                print(update_room_response)
                if not update_room_response:
                    responses.append(
                        StandardResponse(
                            model_name=model.name,
                            model_id=model.id,
                            client=model.client,
                            response="Failed to update room options: Empty response",
                            success=False,
                            pixel=[update_room_pixel],
                        )
                    )
                    continue
            except Exception as e:
                responses.append(
                    StandardResponse(
                        model_name=model.name,
                        model_id=model.id,
                        client=model.client,
                        response=f"Failed to update room options: {e}",
                        success=False,
                        pixel=[update_room_pixel],
                    )
                )
                continue

            function_name = "get_stock_price"
            selections = PixelSelections(
                room_id=self.room_id,
                model_id=model.id,
                mcp_tool_id="29e9e371-9243-4293-ad3b-4be08ef95ab5",
                prompt="What is the price of META?",
                param_dict={"tool_choice": {"type": "AUTO"}},
            )

            ask_playground_pixel = self.pixel_maker.create_ask_playground_pixel(
                selections
            )
            print(f"Running MCP Tool Pixel: {ask_playground_pixel}")

            try:
                ask_playground_response = self.semoss_client.run_pixel(
                    ask_playground_pixel
                )
                responseMessage = ask_playground_response.get("responseMessage", None)
                tool_response = responseMessage.get("tool_responses", None)
                if tool_response:
                    tool_response = tool_response[0]
                print(f"Tool Response: {tool_response}")
            except Exception as e:
                responses.append(
                    StandardResponse(
                        model_name=model.name,
                        model_id=model.id,
                        client=model.client,
                        response=f"PHASE 1: Failed to run AskPlayground pixel: {e}",
                        success=False,
                        pixel=[update_room_pixel, ask_playground_pixel],
                    )
                )
                continue

            if tool_response:
                param_values = tool_response.get("arguments", {})
                tool_call_id = tool_response.get("id", None)
                run_mcp_tool_pixel = f'RunMCPTool(project=["29e9e371-9243-4293-ad3b-4be08ef95ab5"], function=["{function_name}"], paramValues=[{param_values}])'

                try:
                    run_mcp_tool_response = self.semoss_client.run_pixel(
                        run_mcp_tool_pixel
                    )
                    if not run_mcp_tool_response:
                        responses.append(
                            StandardResponse(
                                model_name=model.name,
                                model_id=model.id,
                                client=model.client,
                                response=f"Failed to run RunMCPTool",
                                success=False,
                                pixel=[
                                    update_room_pixel,
                                    ask_playground_pixel,
                                    run_mcp_tool_pixel,
                                ],
                            )
                        )
                        continue
                except Exception as e:
                    responses.append(
                        StandardResponse(
                            model_name=model.name,
                            model_id=model.id,
                            client=model.client,
                            response=f"Failed to run RunMCPToo: {e}",
                            success=False,
                            pixel=[
                                update_room_pixel,
                                ask_playground_pixel,
                                run_mcp_tool_pixel,
                            ],
                        )
                    )
                    continue

                add_tool_execution_pixel = f'AddToolExecution(engine=["{model_id}"], roomId=["{room_id}"], toolId=["{tool_call_id}"], toolName=["{function_name}"], tool_execution_response=[{run_mcp_tool_response}])'

                try:
                    add_tool_execution_response = self.semoss_client.run_pixel(
                        add_tool_execution_pixel
                    )
                    if not add_tool_execution_response:
                        responses.append(
                            StandardResponse(
                                model_name=model.name,
                                model_id=model.id,
                                client=model.client,
                                response=f"Failed to run RunMCPTool",
                                success=False,
                                pixel=[
                                    update_room_pixel,
                                    ask_playground_pixel,
                                    run_mcp_tool_pixel,
                                    add_tool_execution_pixel,
                                ],
                            )
                        )
                        continue

                    print(
                        "Tool execution added successfully:",
                        add_tool_execution_response,
                    )
                except Exception as e:
                    responses.append(
                        StandardResponse(
                            model_name=model.name,
                            model_id=model.id,
                            client=model.client,
                            response=f"Failed to run RunMCPTool: {e}",
                            success=False,
                            pixel=[
                                update_room_pixel,
                                ask_playground_pixel,
                                run_mcp_tool_pixel,
                                add_tool_execution_pixel,
                            ],
                        )
                    )
                    continue

            try:
                if tool_response:
                    response = self._extract_tool_response(add_tool_execution_response)
                else:
                    response = self._extract_text_response(ask_playground_response)

                confirmation = self.openai_confirmer.confirm_tool_calling_response(
                    response
                )

                standard_response_with_confirmation = StandardResponse(
                    model_name=model.name,
                    model_id=model.id,
                    client=model.client,
                    response=response,
                    success=confirmation.confirmed,
                    pixel=[
                        update_room_pixel,
                        ask_playground_pixel,
                        run_mcp_tool_pixel,
                        add_tool_execution_pixel,
                    ],
                    confirmation_response=confirmation.confirmation_response,
                )
                responses.append(standard_response_with_confirmation)

            except Exception as e:
                responses.append(
                    StandardResponse(
                        model_name=model.name,
                        model_id=model.id,
                        client=model.client,
                        response=f"Failed to run RunMCPTool: {e}",
                        success=False,
                        pixel=[
                            update_room_pixel,
                            ask_playground_pixel,
                            run_mcp_tool_pixel,
                            add_tool_execution_pixel,
                        ],
                    )
                )

        return responses
