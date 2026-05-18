from dotenv import load_dotenv
import os

load_dotenv()


class Settings:

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    OPENAI_MODEL = "gpt-4o-mini"
    GEMINI_MODEL = "gemini-2.5-flash"

    TEMPERATURE = 0.2

settings = Settings()
