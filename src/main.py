import os

from dotenv import load_dotenv

load_dotenv()

from agents.assistant import get_agent
from config.settings import settings
from guardrails import check_input, check_output
from llms.models import format_llm_error
from tools.file_tool import new_files_since, snapshot_files

from langchain_core.callbacks.base import BaseCallbackHandler


class ToolCallbackHandler(BaseCallbackHandler):
    def on_tool_start(self, serialized, input_str, **kwargs):
        print(f"\n[tool] {serialized.get('name')}: {input_str}")

    def on_tool_end(self, output, **kwargs):
        print(f"[tool] -> {output}\n")


def run_assistant(
    user_input: str,
    *,
    provider: str | None = None,
    show_tools: bool = False,
    history: list[dict] | None = None,
) -> tuple[str, list]:
    check = check_input(user_input)
    if not check.allowed:
        return check.message, []

    resolved = (provider or os.getenv("LLM_PROVIDER", "openai")).lower()
    before = snapshot_files()

    messages = [
        {"role": m["role"], "content": m["content"]}
        for m in (history or [])
        if m.get("role") in ("user", "assistant") and m.get("content")
    ]
    messages.append({"role": "user", "content": user_input})
    if len(messages) > settings.MAX_HISTORY_MESSAGES:
        messages = messages[-settings.MAX_HISTORY_MESSAGES :]

    try:
        response = get_agent(resolved).invoke(
            {"messages": messages},
            config={"callbacks": [ToolCallbackHandler()]} if show_tools else None,
        )
    except ValueError as exc:
        return str(exc), []
    except Exception as exc:
        return format_llm_error(exc), []

    content = getattr(response["messages"][-1], "content", "")
    check = check_output(content)
    if not check.allowed:
        return check.message, []

    return check.message, new_files_since(before, snapshot_files())


def main() -> None:
    print("AI Assistant — type 'quit' to exit, /openai or /gemini to switch\n")
    provider = None
    history: list[dict] = []

    while True:
        try:
            query = input("You: ").strip()
        except KeyboardInterrupt:
            break
        if not query or query.lower() in ("exit", "quit"):
            break
        if query.lower().startswith("/openai"):
            provider = "openai"
            query = query[7:].strip()
            if not query:
                continue
        elif query.lower().startswith("/gemini"):
            provider = "gemini"
            query = query[7:].strip()
            if not query:
                continue

        reply, files = run_assistant(
            query, provider=provider, show_tools=True, history=history
        )
        history.append({"role": "user", "content": query})
        history.append({"role": "assistant", "content": reply})
        print(f"\nAI: {reply}")
        for path in files:
            print(f"  file: {path.name}")
        print()


if __name__ == "__main__":
    main()
