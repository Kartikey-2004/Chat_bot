import os

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

from config.settings import settings

MODELS = {
    "openai": settings.OPENAI_MODEL,
    "gemini": settings.GEMINI_MODEL,
}

openai_llm = ChatOpenAI(
    model=settings.OPENAI_MODEL,
    temperature=settings.TEMPERATURE,
    api_key=settings.OPENAI_API_KEY,
)

gemini_llm = ChatGoogleGenerativeAI(
    model=settings.GEMINI_MODEL,
    temperature=settings.TEMPERATURE,
    google_api_key=settings.GEMINI_API_KEY,
)

_PROVIDERS = {
    "openai": openai_llm,
    "gemini": gemini_llm,
}


def get_llm(provider: str | None = None):
    name = (provider or os.getenv("LLM_PROVIDER", "openai")).lower()
    try:
        return _PROVIDERS[name]
    except KeyError as exc:
        raise ValueError(
            f"Unknown LLM provider: {name!r}. Use one of: {', '.join(_PROVIDERS)}"
        ) from exc
