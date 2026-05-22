import subprocess
from langchain.tools import tool


@tool
def run_shell_command(command: str) -> str:
    """
    Execute a shell command safely and return the output.

    Useful for:
    - Running terminal commands
    - Checking files/folders
    - Running Python scripts
    - Git commands
    - Development workflows
    """

    if not command.strip():
        return "Error: Empty command."

    blocked_commands = [
        "rm -rf",
        "shutdown",
        "reboot",
        "mkfs",
        ":(){:|:&};:",
    ]

    for blocked in blocked_commands:
        if blocked in command:
            return f"Blocked dangerous command: {blocked}"

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=20,
        )

        output = result.stdout.strip()
        error = result.stderr.strip()

        response = []

        if output:
            response.append(f"STDOUT:\n{output}")

        if error:
            response.append(f"STDERR:\n{error}")

        if not response:
            response.append("Command executed successfully with no output.")

        return "\n\n".join(response)

    except subprocess.TimeoutExpired:
        return "Error: Command timed out."

    except Exception as e:
        return f"Error executing command: {str(e)}"
