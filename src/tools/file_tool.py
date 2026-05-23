from pathlib import Path
from typing import List

from langchain.tools import tool

from config.settings import settings

_PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _agent_files_dir() -> Path:
    path = Path(settings.AGENT_FILES_DIR)
    if not path.is_absolute():
        path = _PROJECT_ROOT / path
    return path


def _ensure_agent_files_dir() -> Path:
    directory = _agent_files_dir()
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def _resolve_write_path(file_path: str) -> Path:
    """Relative paths are stored under the agent output directory."""
    path = Path(file_path)
    if path.is_absolute():
        return path
    return _ensure_agent_files_dir() / path


def _resolve_read_path(file_path: str) -> Path:
    path = Path(file_path)
    if path.exists():
        return path
    agent_path = _agent_files_dir() / path
    if agent_path.exists():
        return agent_path
    return path


def _resolve_list_dir(directory: str) -> Path:
    if directory in (".", ""):
        return _ensure_agent_files_dir()
    path = Path(directory)
    if path.is_absolute():
        return path
    return _ensure_agent_files_dir() / path


@tool
def read_file(file_path: str) -> str:
    """
    Read content from a file.
    Relative paths are looked up in the agent output folder first, then the project.
    """

    path = _resolve_read_path(file_path)

    if not path.exists():
        return f"Error: File '{file_path}' not found."

    try:
        return path.read_text(encoding="utf-8")

    except Exception as e:
        return f"Error reading file: {str(e)}"


@tool
def write_file(file_path: str, content: str) -> str:
    """
    Write content to a file.
    Relative paths are saved under the agent output folder (see AGENT_FILES_DIR).
    Automatically creates folders if they do not exist.
    """

    path = _resolve_write_path(file_path)

    try:
        path.parent.mkdir(parents=True, exist_ok=True)

        path.write_text(content, encoding="utf-8")

        return f"File written successfully: {path}"

    except Exception as e:
        return f"Error writing file: {str(e)}"


@tool
def append_file(file_path: str, content: str) -> str:
    """
    Append content to an existing file.
    Relative paths use the agent output folder (see AGENT_FILES_DIR).
    Automatically creates folders if needed.
    """

    path = _resolve_write_path(file_path)

    try:
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "a", encoding="utf-8") as f:
            f.write(content)

        return f"Content appended successfully: {path}"

    except Exception as e:
        return f"Error appending file: {str(e)}"


@tool
def list_files(directory: str = ".") -> List[str]:
    """
    List all files in a directory.
    Default lists the agent output folder where created files are stored.
    """

    path = _resolve_list_dir(directory)

    if not path.exists():
        return [f"Error: Directory '{directory}' not found."]

    return [str(file) for file in path.iterdir()]
