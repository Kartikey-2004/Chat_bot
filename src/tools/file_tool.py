from pathlib import Path
from typing import List

from langchain.tools import tool

from config.settings import settings

_ROOT = Path(__file__).resolve().parents[2]


def agent_output_dir() -> Path:
    path = Path(settings.AGENT_FILES_DIR)
    if not path.is_absolute():
        path = _ROOT / path
    path.mkdir(parents=True, exist_ok=True)
    return path


def snapshot_files() -> dict[str, float]:
    root = agent_output_dir()
    return {
        str(f.relative_to(root)): f.stat().st_mtime
        for f in root.rglob("*")
        if f.is_file()
    }


def new_files_since(before: dict[str, float], after: dict[str, float]) -> list[Path]:
    root = agent_output_dir()
    return [
        root / rel
        for rel, mtime in after.items()
        if rel not in before or before[rel] < mtime
    ]


def _write_path(file_path: str) -> Path:
    path = Path(file_path)
    return path if path.is_absolute() else agent_output_dir() / path


def _read_path(file_path: str) -> Path:
    path = Path(file_path)
    if path.exists():
        return path
    agent_path = agent_output_dir() / path
    return agent_path if agent_path.exists() else path


@tool
def read_file(file_path: str) -> str:
    """Read a file. Relative paths use the agent output folder."""
    path = _read_path(file_path)
    if not path.exists():
        return f"Error: File '{file_path}' not found."
    try:
        return path.read_text(encoding="utf-8")
    except Exception as e:
        return f"Error reading file: {e}"


@tool
def write_file(file_path: str, content: str) -> str:
    """Write a file. Relative paths save under the agent output folder."""
    path = _write_path(file_path)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return f"File written: {path.name}"
    except Exception as e:
        return f"Error writing file: {e}"


@tool
def append_file(file_path: str, content: str) -> str:
    """Append to a file. Relative paths use the agent output folder."""
    path = _write_path(file_path)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "a", encoding="utf-8") as f:
            f.write(content)
        return f"Content appended: {path.name}"
    except Exception as e:
        return f"Error appending file: {e}"


@tool
def list_files(directory: str = ".") -> List[str]:
    """List files in a directory. Default is the agent output folder."""
    if directory in (".", ""):
        path = agent_output_dir()
    else:
        p = Path(directory)
        path = p if p.is_absolute() else agent_output_dir() / p
    if not path.exists():
        return [f"Error: Directory '{directory}' not found."]
    return [f.name for f in path.iterdir()]
