import os
from litellm import completion
from config.settings import settings 

os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
os.environ["GEMINI_API_KEY"] = settings.GEMINI_API_KEY

def generate_response(model: str, prompt: str):
    response = completion(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
    )
    return response["choices"][0]["message"]["content"]
