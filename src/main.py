from dotenv import load_dotenv

load_dotenv()

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.callbacks.base import BaseCallbackHandler

# =========================
# Tools
# =========================
from tools.search_tool import web_search
from tools.calculator_tool import calculator

from tools.file_tool import (
    read_file,
    write_file,
    append_file,
    list_files,
)

from tools.shell_tool import run_shell_command


# =========================================
# Callback Handler
# =========================================
class ToolCallbackHandler(BaseCallbackHandler):

    def on_tool_start(self, serialized, input_str, **kwargs):
        print("\n========== TOOL USED ==========")
        print(f"Tool Name  : {serialized.get('name')}")
        print(f"Tool Input : {input_str}")

    def on_tool_end(self, output, **kwargs):
        print(f"Tool Output: {output}")
        print("================================\n")

    def on_tool_error(self, error, **kwargs):
        print("\n========== TOOL ERROR ==========")
        print(f"Error: {str(error)}")
        print("================================\n")


# =========================================
# LLM
# =========================================
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
)


# =========================================
# Agent
# =========================================
agent = create_agent(
    model=llm,
    tools=[
        # Search + Math
        web_search,
        calculator,
        # File Tools
        read_file,
        write_file,
        append_file,
        list_files,
        # Shell Tool
        run_shell_command,
    ],
    system_prompt="""
You are a professional AI assistant.

You have access to multiple tools.

Available Tools:
------------------------------------------------

1. calculator
- Perform mathematical calculations

2. web_search
- Search the internet for recent information

3. read_file
- Read file contents

4. write_file
- Create or overwrite files

5. append_file
- Append content to existing files

6. list_files
- List files/folders in a directory

7. run_shell_command
- Execute terminal/shell commands

Rules:
------------------------------------------------
- Use tools whenever required.
- Always choose the correct tool.
- Never hallucinate file contents.
- Never pretend shell commands executed if they did not.
- Keep answers concise and accurate.
- For coding tasks:
    - inspect files first
    - modify carefully
    - avoid unnecessary overwrites
""",
)


# =========================================
# Chat Loop
# =========================================
print("\n===================================")
print("        AI Assistant Started")
print("===================================")
print("Type 'exit' or 'quit' to stop.\n")

while True:

    user_query = input("You: ").strip()

    if not user_query:
        continue

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
            config={"callbacks": [ToolCallbackHandler()]},
        )

        ai_message = response["messages"][-1].content

        print("\nAI:")
        print(ai_message)
        print()

    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")
        break

    except Exception as e:
        print("\n========== ERROR ==========")
        print(str(e))
        print("===========================\n")
