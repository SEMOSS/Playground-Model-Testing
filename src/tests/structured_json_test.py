from typing import Optional
from src.utils.models import Model
from src.pixels.pixel_maker import PixelSelections
from src.tests.response_models import StandardResponse
from src.tests.abstract_tests import AbstractTests
from src.utils.models import DeploymentKeys


class StructuredJSONTest(AbstractTests):
    """
    Structured JSON Test: Tests the model's ability to process and respond to prompts that require structured JSON outputs.
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
            selections = PixelSelections(
                room_id=self.room_id,
                model_id=model.id,
                prompt="Name a few Manchester United players you know with their positions, countries, and skill ratings.",
                param_dict={
                    "schema": {
                        "type": "object",
                        "properties": {
                            "players": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string"},
                                        "position": {"type": "string"},
                                        "country": {"type": "string"},
                                        "skill": {"type": "integer"},
                                    },
                                    "required": [
                                        "name",
                                        "position",
                                        "country",
                                        "skill",
                                    ],
                                },
                            }
                        },
                        "required": ["players"],
                    }
                },
            )
            pixel = self.pixel_maker.create_ask_playground_pixel(selections)

            try:
                response = self.semoss_client.run_pixel(pixel)
                text_response = self._extract_text_response(response)
                confirmation = self.openai_confirmer.confirm_json_structure(
                    text_response
                )

                standard_response = StandardResponse(
                    model_name=model.name,
                    model_id=model.id,
                    client=model.client,
                    response=text_response,
                    success=confirmation.confirmed,
                    pixel=[pixel],
                    confirmation_response=confirmation.confirmation_response,
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
