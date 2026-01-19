from langchain_anthropic import ChatAnthropic
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI

from config.settings import get_settings


def get_llm(
    provider: str | None = None,
    model: str | None = None,
    temperature: float | None = None,
) -> BaseChatModel:
    """Get LLM instance based on provider configuration.

    Args:
        provider: LLM provider ('openai' or 'anthropic'). Defaults to settings.
        model: Model name. Defaults to settings based on provider.
        temperature: Temperature for generation. Defaults to settings.

    Returns:
        Configured LLM instance.
    """
    settings = get_settings()

    provider = provider or settings.default_llm_provider
    temperature = temperature if temperature is not None else settings.temperature

    if provider == "openai":
        return ChatOpenAI(
            api_key=settings.openai_api_key,
            model=model or settings.openai_model,
            temperature=temperature,
            max_tokens=settings.max_tokens,
        )
    elif provider == "anthropic":
        return ChatAnthropic(
            api_key=settings.anthropic_api_key,
            model=model or settings.anthropic_model,
            temperature=temperature,
            max_tokens=settings.max_tokens,
        )
    else:
        raise ValueError(f"Unknown LLM provider: {provider}")
