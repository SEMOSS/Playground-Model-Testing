from ai_server import ServerClient
from openai import OpenAI
from src.utils.models import DeploymentKeys


def get_semoss_client(deployment_keys: DeploymentKeys) -> ServerClient:

    print("Creating SEMOSS client with deployment keys:", deployment_keys.model_dump())

    client = ServerClient(
        base=deployment_keys.url,
        access_key=deployment_keys.access_key,
        secret_key=deployment_keys.secret_key,
    )
    return client


def get_openai_client(deployment_key: str) -> OpenAI:
    client = OpenAI(api_key=deployment_key)
    return client
