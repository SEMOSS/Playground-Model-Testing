import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field


class SEMOSSCredentials(BaseModel):
    secret_key: str = Field(..., env="SEMOSS_SECRET_KEY")
    access_key: str = Field(..., env="SEMOSS_ACCESS_KEY")
    base_url: str = Field(..., env="SEMOSS_BASE_URL")
    openai_key: str = Field(..., env="OPENAI_API_KEY")


def get_semoss_credentials() -> SEMOSSCredentials:
    load_dotenv()
    return SEMOSSCredentials(
        secret_key=os.getenv("SEMOSS_SECRET_KEY"),
        access_key=os.getenv("SEMOSS_ACCESS_KEY"),
        base_url=os.getenv("SEMOSS_BASE_URL"),
        openai_key=os.getenv("OPENAI_API_KEY"),
    )
