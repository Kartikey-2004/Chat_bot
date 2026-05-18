from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

from config.settings import (
    OPENAI_API_KEY,
    GEMINI_API_KEY,
    OPENAI_MODEL,
    GEMINI_MODEL,
    TEMPERATURE,
)

openai_llm = ChatOpenAI(
    model=OPENAI_MODEL,
    temperature=TEMPERATURE,
    api_key=OPENAI_API_KEY,
)

gemini_llm = ChatGoogleGenerativeAI(
    model=GEMINI_MODEL,
    temperature=TEMPERATURE,
    google_api_key=GEMINI_API_KEY,
)
