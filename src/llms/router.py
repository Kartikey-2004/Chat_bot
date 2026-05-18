from llms.models import openai_llm, gemini_llm


class LLMRouter:
    @staticmethod
    def get_llm(task: str):
        routes = {
            "reasoning": openai_llm,
            "coding": openai_llm,
            "fast": gemini_llm,
            "chat": gemini_llm,
            "math": gemini_llm,
        }
        return routes.get(task, gemini_llm)
