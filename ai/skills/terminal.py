import subprocess
from ai.skills.base import Skill, string_parameters, SkillError
from ai.providers import Tool


SAFE_COMMANDS = {
    'ls', 'dir', 'pwd', 'cd', 'echo', 'date', 'time', 'whoami',
    'hostname', 'uname', 'ver', 'help', 'cls', 'clear'
}


def execute_command(kernel, command: str) -> str:
    """Execute a safe system command."""
    try:
        base_command = command.split()[0].lower() if command.split() else ""
        if base_command not in SAFE_COMMANDS:
            raise SkillError(
                f"Command '{base_command}' is not allowed for security reasons"
            )
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode != 0:
            return f"Command failed: {result.stderr}"
        return result.stdout or "Command executed successfully"
    except subprocess.TimeoutExpired:
        raise SkillError("Command timed out")
    except SkillError:
        raise
    except Exception as e:
        raise SkillError(f"Could not execute command: {e}")


def list_directory(kernel, path: str = ".") -> str:
    """List files in a directory."""
    try:
        result = subprocess.run(
            ['dir' if subprocess.os.name == 'nt' else 'ls', path],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout or "Directory is empty"
    except Exception as e:
        raise SkillError(f"Could not list directory: {e}")


SKILLS = (
    Skill(
        tool=Tool(
            name="execute_command",
            description="Execute a safe system command (limited to basic commands)",
            parameters=string_parameters(command="The command to execute"),
        ),
        run=execute_command
    ),
    Skill(
        tool=Tool(
            name="list_directory",
            description="List files in a directory",
            parameters=string_parameters(path="Directory path (default: current directory)"),
        ),
        run=list_directory
    ),
)