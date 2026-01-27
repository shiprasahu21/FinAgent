from agno.models.openai import OpenAILike
from agno.agent import Agent
import uuid
import requests
from dotenv import load_dotenv
import os
from agno.os import AgentOS

# Load environment variables from .env file
load_dotenv()

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    client_app_secret: str = Field(
        ..., description="Client application secret for authentication"
    )
    experience_id: str = Field(..., description="Intuit experience ID")
    client_app_id: str = Field(..., description="Client application ID")
    profile_id: str = Field(..., description="Profile ID for authentication")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Initialize settings
settings = Settings()

_cached_token = None


def _get_auth_token() -> str:
    global _cached_token
    if _cached_token:
        return _cached_token

    """Get cached authentication token or fetch a new one if not available"""

    # Fetch new token from IAM
    url = "https://identityinternal.api.intuit.com/v1/graphql"

    IAM_MUTATION = """mutation identitySignInInternalApplicationWithPrivateAuth($input: Identity_SignInApplicationWithPrivateAuthInput!) {
        identitySignInInternalApplicationWithPrivateAuth(input: $input) {
            authorizationHeader
        }
    }"""

    headers = {
        "intuit_tid": str(uuid.uuid4()),
        "Authorization": f"Intuit_IAM_Authentication intuit_appid={settings.client_app_id}, intuit_app_secret={settings.client_app_secret}",
        "Content-Type": "application/json",
    }

    data = {
        "query": IAM_MUTATION,
        "variables": {"input": {"profileId": settings.profile_id}},
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()

        base_token = result["data"]["identitySignInInternalApplicationWithPrivateAuth"][
            "authorizationHeader"
        ]
        _cached_token = f"{base_token},intuit_appid={settings.client_app_id},intuit_app_secret={settings.client_app_secret}"
        print("✓ New auth token obtained and cached")
        return _cached_token
    except Exception as e:
        print(f"✗ Failed to get auth token: {e}")
        raise


llm = OpenAILike(
    base_url="https://llmexecution.api.intuit.com/v3/lt/amazon.nova-lite-v1-0",
    extra_headers={
        "intuit_experience_id": settings.experience_id,
        "intuit_originating_assetalias": "Intuit.coe.pecomplianceremediation",
        "Authorization": _get_auth_token(),
    },
)

gen_agent = Agent(
    name="Generalist",
    instructions="You are a generalist agent that can help with a wide range of tasks.",
    model=llm,
)

agent_os = AgentOS(
    id="my-first-os",
    description="My first AgentOS",
    agents=[gen_agent],
)

app = agent_os.get_app()

if __name__ == "__main__":
    # Default port is 7777; change with port=...
    agent_os.serve(app="test:app", reload=True, port=5111)
