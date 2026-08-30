import shutil
from pathlib import Path


class FileSystem:

    def __init__(self):

        self.current_path = Path.home()

        self.back_history = []
        self.forward_history = []
        self._clipboard = None  # (path, mode: 'copy'|'cut')

    # =====================================================

    def get_current_path(self):

        return self.current_path

    # =====================================================

    def list_directory(self):

        items = []

        try:

            for item in sorted(
                self.current_path.iterdir(),
                key=lambda x: (x.is_file(), x.name.lower())
            ):
                items.append(item)

        except Exception as e:

            print(e)

        return items

    # =====================================================

    def open_folder(self, folder):

        folder = Path(folder)

        if folder.exists() and folder.is_dir():

            self.back_history.append(self.current_path)

            self.current_path = folder

            self.forward_history.clear()

            return True

        return False

    # =====================================================

    def go_up(self):

        parent = self.current_path.parent

        if parent != self.current_path:

            self.open_folder(parent)

    # =====================================================

    def can_go_back(self):

        return len(self.back_history) > 0

    # =====================================================

    def can_go_forward(self):

        return len(self.forward_history) > 0

    # =====================================================

    def go_back(self):

        if not self.can_go_back():
            return

        self.forward_history.append(self.current_path)

        self.current_path = self.back_history.pop()

    # =====================================================

    def go_forward(self):

        if not self.can_go_forward():
            return

        self.back_history.append(self.current_path)

        self.current_path = self.forward_history.pop()

    # =====================================================
    # File Operations
    # =====================================================

    def copy_file(self, path):
        """Copy a file/folder to clipboard."""
        self._clipboard = (Path(path), 'copy')

    def cut_file(self, path):
        """Cut a file/folder to clipboard."""
        self._clipboard = (Path(path), 'cut')

    def paste_file(self):
        """Paste from clipboard into current directory."""
        if not self._clipboard:
            return False, "Nothing to paste"
        src, mode = self._clipboard
        if not src.exists():
            return False, f"Source no longer exists: {src.name}"
        dest = self.current_path / src.name
        # Handle name conflict
        if dest.exists():
            base = src.stem
            suffix = src.suffix
            counter = 1
            while dest.exists():
                dest = self.current_path / f"{base} ({counter}){suffix}"
                counter += 1
        try:
            if mode == 'cut':
                shutil.move(str(src), str(dest))
                self._clipboard = None
            else:
                if src.is_dir():
                    shutil.copytree(str(src), str(dest))
                else:
                    shutil.copy2(str(src), str(dest))
            return True, f"Pasted {src.name}"
        except Exception as e:
            return False, str(e)

    def has_clipboard(self):
        """Check if clipboard has a file."""
        return self._clipboard is not None

    def delete_file(self, path):
        """Delete a file or directory."""
        p = Path(path)
        if not p.exists():
            return False, f"File not found: {p.name}"
        try:
            if p.is_dir():
                shutil.rmtree(str(p))
            else:
                p.unlink()
            return True, f"Deleted {p.name}"
        except Exception as e:
            return False, str(e)

    def rename_file(self, path, new_name):
        """Rename a file or directory."""
        p = Path(path)
        if not p.exists():
            return False, f"File not found"
        new_path = p.parent / new_name
        if new_path.exists():
            return False, f"Name already taken: {new_name}"
        try:
            p.rename(new_path)
            return True, f"Renamed to {new_name}"
        except Exception as e:
            return False, str(e)

    def create_folder(self, name):
        """Create a new folder in the current directory."""
        try:
            new_dir = self.current_path / name
            new_dir.mkdir(exist_ok=True)
            return True, f"Created folder: {name}"
        except Exception as e:
            return False, str(e)

    def create_file(self, name):
        """Create a new file in the current directory."""
        try:
            new_file = self.current_path / name
            new_file.touch(exist_ok=True)
            return True, f"Created file: {name}"
        except Exception as e:
            return False, str(e)