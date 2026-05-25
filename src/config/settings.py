import logging
import os
import warnings

from dotenv import load_dotenv

load_dotenv()


def _configure_runtime_noise() -> None:
    # LangChain + LiteLLM attach `reasoning` metadata that Pydantic v2 flags when
    # serializing (e.g. for LangSmith). Harmless; suppress so the CLI stays readable.
    warnings.filterwarnings("ignore", category=UserWarning, module="pydantic.main")
    for name in ("LiteLLM", "litellm"):
        logging.getLogger(name).setLevel(logging.ERROR)


_configure_runtime_noise()


def _configure_langsmith_tracing() -> None:
    key = os.getenv("LANGSMITH_API_KEY", "").strip()
    enabled = os.getenv("LANGSMITH_TRACING", "false").lower() in ("1", "true", "yes")
    tracing = bool(key) and enabled
    value = "true" if tracing else "false"
    os.environ["LANGCHAIN_TRACING_V2"] = value
    os.environ["LANGSMITH_TRACING"] = value
    for name in ("langsmith", "langsmith.client"):
        logging.getLogger(name).setLevel(logging.ERROR)


_configure_langsmith_tracing()


class Settings:

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    TEMPERATURE = 0.2

    AGENT_FILES_DIR = os.getenv("AGENT_FILES_DIR", "agent_output")

    MAX_HISTORY_MESSAGES = int(os.getenv("MAX_HISTORY_MESSAGES", "20"))


settings = Settings()
