import os

from langchain.agents import create_agent

from config.settings import settings
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

SYSTEM_PROMPT = f"""
You are a professional AI assistant.
You have access to multiple tools.

Available Tools (4 categories):
------------------------------------------------
1. calculator — math expressions
2. web_search — internet search
3. file tools — read_file, write_file, append_file, list_files
   (relative paths save to {settings.AGENT_FILES_DIR}/)
4. run_shell_command — terminal commands (dangerous commands blocked)

Rules:
------------------------------------------------
- Use tools whenever required.
- Always choose the correct tool.
- Never hallucinate file contents.
- Never pretend shell commands executed if they did not.
- Keep answers concise and accurate.
- Refuse harmful, illegal, or unethical requests.
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

_agents: dict = {}


def get_agent(provider: str | None = None):
    name = (provider or os.getenv("LLM_PROVIDER", "openai")).lower()
    if name not in _agents:
        _agents[name] = create_agent(
            model=get_llm(name),
            tools=tools,
            system_prompt=SYSTEM_PROMPT,
        )
    return _agents[name]
