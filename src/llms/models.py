import os

from langchain_litellm import ChatLiteLLM

from config.settings import settings

_llm_cache: dict[str, ChatLiteLLM] = {}


def configured_providers() -> list[str]:
    providers = []
    if settings.OPENAI_API_KEY:
        providers.append("openai")
    if settings.GEMINI_API_KEY:
        providers.append("gemini")
    return providers


def provider_label(name: str) -> str:
    model = settings.OPENAI_MODEL if name == "openai" else settings.GEMINI_MODEL
    return f"{name.title()} · {model}"


def _litellm_model(name: str) -> str:
    if name == "openai":
        return f"openai/{settings.OPENAI_MODEL}"
    return f"gemini/{settings.GEMINI_MODEL}"


def get_llm(provider: str | None = None) -> ChatLiteLLM:
    name = (provider or os.getenv("LLM_PROVIDER", "openai")).lower()
    if name not in ("openai", "gemini"):
        raise ValueError(f"Unknown provider: {name!r}")

    if name == "openai" and not settings.OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is missing in .env")
    if name == "gemini" and not settings.GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is missing in .env")

    if name in _llm_cache:
        return _llm_cache[name]

    if settings.OPENAI_API_KEY:
        os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
    if settings.GEMINI_API_KEY:
        os.environ["GEMINI_API_KEY"] = settings.GEMINI_API_KEY
        os.environ["GOOGLE_API_KEY"] = settings.GEMINI_API_KEY

    llm = ChatLiteLLM(model=_litellm_model(name), temperature=settings.TEMPERATURE)
    _llm_cache[name] = llm
    return llm


def format_llm_error(exc: Exception) -> str:
    message = str(exc)
    if "429" in message or "RESOURCE_EXHAUSTED" in message.upper():
        return "Rate limit exceeded."
    return f"Request failed: {message[:400]}"
