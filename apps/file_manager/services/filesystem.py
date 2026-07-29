from pathlib import Path


class FileSystem:

    def __init__(self):

        self.current_path = Path.home()

        self.back_history = []
        self.forward_history = []

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