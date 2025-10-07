from ai_server import ServerClient
from src.utils.credentials import get_semoss_credentials
from openai import OpenAI


def get_semoss_client() -> ServerClient:
    creds = get_semoss_credentials()
    client = ServerClient(
        base=creds.base_url,
        access_key=creds.access_key,
        secret_key=creds.secret_key,
    )
    return client


def get_openai_client() -> OpenAI:
    creds = get_semoss_credentials()
    client = OpenAI(api_key=creds.openai_key)
    return client
