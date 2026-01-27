"""
LLM configuration and authentication for FinAgent.
"""

import uuid
import requests
from agno.models.openai import OpenAILike
from settings import get_settings

_cached_token: str | None = None


def _get_auth_token() -> str:
    """Get cached authentication token or fetch a new one if not available."""
    global _cached_token
    if _cached_token:
        return _cached_token

    settings = get_settings()

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


def get_llm(model: str = "amazon.nova-pro-v1-0") -> OpenAILike:
    """
    Get configured LLM instance.

    Args:
        model: Model name to use (default: amazon.nova-lite-v1-0)
               Options: amazon.nova-lite-v1-0, anthropic.claude-sonnet-4-20250514-v1-0,
               gpt-5-nano-2025-08-07-oai, gpt-5-chat-2025-08-07-oai

    Returns:
        Configured OpenAILike instance
    """
    settings = get_settings()

    return OpenAILike(
        base_url=f"https://llmexecution.api.intuit.com/v3/lt/{model}",
        extra_headers={
            "intuit_experience_id": settings.experience_id,
            "intuit_originating_assetalias": "Intuit.coe.pecomplianceremediation",
            "Authorization": _get_auth_token(),
        },
    )
