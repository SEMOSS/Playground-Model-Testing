from pydantic import BaseModel


class Model(BaseModel):
    name: str
    type: str
    id: str
    client: str


models = [
    Model(
        name="GPT-4o Chat Completions",
        type="OpenAI",
        id="4acbe913-df40-4ac0-b28a-daa5ad91b172",
        client="OpenAI - Chat Completions",
    ),
    Model(
        name="Claude Sonnet 4 Anthropic Vertex",
        type="Anthropic",
        id="b0d18f4b-ff2c-4563-8f9d-57efbff53d60",
        client="Anthropic - Vertex",
    ),
    Model(
        name="Gemini Flash 2.5 Vertex",
        type="Google GenAI",
        id="692215ed-b693-45df-a464-56a99d397d27",
        client="Google GenAI - Vertex",
    ),
    Model(
        name="GPT-4o Responses",
        type="OpenAI",
        id="714e633c-ae67-49c8-98ff-b631222b8bca",
        client="OpenAI - Responses",
    ),
    Model(
        name="GPT-4o Azure",
        type="OpenAI",
        id="c5b85067-01b0-4134-917f-2a46290832fb",
        client="OpenAI - Azure",
    ),
    Model(
        name="Claude Sonnet 3.5 Anthropic Bedrock",
        type="Anthropic",
        id="d8c58ea9-3e23-4535-a696-94465ff12711",
        client="Anthropic - Bedrock",
    ),
    Model(
        name="Claude Sonnet 3.5 Bedrock",
        type="Bedrock",
        id="b6fd16f0-18ba-4f24-baca-8e31a8189c55",
        client="Anthropic - Bedrock",
    ),
    Model(
        name="Llama3 70B",
        type="OpenAI",
        id="4801422a-5c62-421e-a00c-05c6a9e15de8",
        client="OpenAI - Chat Completions",
    ),
]


def get_models() -> list[Model]:
    return models


def get_model_by_id(model_id: str) -> Model | None:
    for model in models:
        if model.id == model_id:
            return model
    return None
