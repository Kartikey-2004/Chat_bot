from pathlib import Path
from typing import List

from langchain.tools import tool


@tool
def read_file(file_path: str) -> str:
    """
    Read content from a file.
    """

    path = Path(file_path)

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
    Automatically creates folders if they do not exist.
    """

    path = Path(file_path)

    try:
        path.parent.mkdir(parents=True, exist_ok=True)

        path.write_text(content, encoding="utf-8")

        return f"File written successfully: {file_path}"

    except Exception as e:
        return f"Error writing file: {str(e)}"


@tool
def append_file(file_path: str, content: str) -> str:
    """
    Append content to an existing file.
    Automatically creates folders if needed.
    """

    path = Path(file_path)

    try:
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "a", encoding="utf-8") as f:
            f.write(content)

        return f"Content appended successfully: {file_path}"

    except Exception as e:
        return f"Error appending file: {str(e)}"


@tool
def list_files(directory: str = ".") -> List[str]:
    """
    List all files in a directory.
    """

    path = Path(directory)

    if not path.exists():
        return [f"Error: Directory '{directory}' not found."]

    return [str(file) for file in path.iterdir()]
