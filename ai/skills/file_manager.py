import os
from ai.skills.base import Skill, string_parameters
from ai.skills.base import SkillError


def list_files(kernel, path: str = ".") -> str:
    """List files in a directory."""
    try:
        if not os.path.exists(path):
            raise SkillError(f"Path does not exist: {path}")
        
        if not os.path.isdir(path):
            raise SkillError(f"Path is not a directory: {path}")
        
        files = os.listdir(path)
        if not files:
            return f"Directory '{path}' is empty"
        
        return f"Files in {path}: " + ", ".join(files[:20])  # Limit to 20 files
        
    except PermissionError:
        raise SkillError(f"Permission denied: {path}")
    except Exception as e:
        raise SkillError(f"Could not list files: {e}")


def open_file_manager(kernel, path: str = ".") -> str:
    """Open file manager at specified path."""
    try:
        # This would integrate with the window manager to open the file manager app
        window_manager = kernel.get_service("window_manager")
        if window_manager:
            return f"Opening file manager at {path}"
        raise SkillError("Window manager not available")
    except Exception as e:
        raise SkillError(f"Could not open file manager: {e}")


def get_file_info(kernel, path: str) -> str:
    """Get information about a file."""
    try:
        if not os.path.exists(path):
            raise SkillError(f"File does not exist: {path}")
        
        stat = os.stat(path)
        size = stat.st_size
        is_dir = os.path.isdir(path)
        
        file_type = "directory" if is_dir else "file"
        return f"{path}: {file_type}, {size} bytes"
        
    except Exception as e:
        raise SkillError(f"Could not get file info: {e}")


SKILLS = [
    Skill(
        tool=string_parameters(
            name="list_files",
            description="List files in a directory",
            path="Directory path (default: current directory)"
        ),
        run=list_files
    ),
    Skill(
        tool=string_parameters(
            name="open_file_manager",
            description="Open file manager at specified path",
            path="Directory path to open (default: current directory)"
        ),
        run=open_file_manager
    ),
    Skill(
        tool=string_parameters(
            name="get_file_info",
            description="Get information about a file",
            path="File or directory path"
        ),
        run=get_file_info
    ),
]