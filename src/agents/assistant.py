import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

_src = Path(__file__).resolve().parents[1]
if str(_src) not in sys.path:
    sys.path.insert(0, str(_src))

from langchain.agents import create_agent
from langchain_core.callbacks.base import BaseCallbackHandler

from llms.models import get_llm
from tools.calculator_tool import calculator
from tools.file_tool import (
    append_file,
    list_files,
    read_file,
    write_file,
)
from tools.search_tool import web_search
from tools.shell_tool import run_shell_command
from config.settings import settings

SYSTEM_PROMPT = f"""
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
- Create or overwrite files (relative paths save to {settings.AGENT_FILES_DIR}/)
5. append_file
- Append content to existing files (relative paths use {settings.AGENT_FILES_DIR}/)
6. list_files
- List files/folders in a directory (default: {settings.AGENT_FILES_DIR}/)
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
- For new files the user asks you to create, use a simple filename (e.g. notes.txt).
  Do not prefix with a folder; the tool saves them under {settings.AGENT_FILES_DIR}/ automatically.
"""

tools = [
    web_search,
    calculator,
    read_file,
    write_file,
    append_file,
    list_files,
    run_shell_command,
]

agent = create_agent(
    model=get_llm(),
    tools=tools,
    system_prompt=SYSTEM_PROMPT,
)


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
        print(f"Error: {error}")
        print("================================\n")


def run_assistant(user_input: str, *, show_tools: bool = False) -> str:
    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_input,
                }
            ]
        },
        config={"callbacks": [ToolCallbackHandler()]} if show_tools else None,
    )
    last = response["messages"][-1]
    return getattr(last, "content", str(last))


if __name__ == "__main__":
    print("\n===================================")
    print("        AI Assistant Started")
    print("===================================")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        query = input("You: ").strip()

        if not query:
            continue

        if query.lower() in ("exit", "quit"):
            print("\nSession Ended.")
            break

        try:
            response = run_assistant(query, show_tools=True)
            print(f"\nAssistant: {response}\n")
        except KeyboardInterrupt:
            print("\n\nInterrupted by user.")
            break
        except Exception as e:
            print("\n========== ERROR ==========")
            print(e)
            print("===========================\n")
