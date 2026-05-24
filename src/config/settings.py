from dotenv import load_dotenv
import os

load_dotenv()


class Settings:

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

    TEMPERATURE = 0.2

    AGENT_FILES_DIR = os.getenv("AGENT_FILES_DIR", "agent_output")

    MAX_HISTORY_MESSAGES = int(os.getenv("MAX_HISTORY_MESSAGES", "20"))


settings = Settings()
