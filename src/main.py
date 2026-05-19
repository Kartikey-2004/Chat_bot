from dotenv import load_dotenv
load_dotenv()

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.callbacks.base import BaseCallbackHandler

from tools.search_tool import web_search
from tools.calculator import calculator


# Callback Handler
class ToolCallbackHandler(BaseCallbackHandler):

    def on_tool_start(self, serialized, input_str, **kwargs):
        print("\n========== TOOL USED ==========")
        print(f"Tool Name  : {serialized.get('name')}")
        print(f"Tool Input : {input_str}")

    def on_tool_end(self, output, **kwargs):
        print(f"Tool Output: {output}")
        print("================================\n")


# LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
)


# Agent
agent = create_agent(
    model=llm,
    tools=[web_search, calculator],
    system_prompt="""
    You are a helpful AI assistant.

    Use:
    - calculator tool for math
    - web_search tool for internet queries
    """,
)


# Chat Loop
print("\n===== AI Assistant Started =====")
print("Type 'exit' to quit.\n")

while True:

    user_query = input("You: ")

    if user_query.lower() in ["exit", "quit"]:
        print("\nSession Ended.")
        break

    try:
        response = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": user_query,
                    }
                ]
            },
            config={
                "callbacks": [ToolCallbackHandler()]
            }
        )

        print("\nAI:", response["messages"][-1].content)
        print()

    except Exception as e:
        print("\nError:", str(e))