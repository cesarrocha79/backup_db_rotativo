import subprocess
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, file_path):
        self.file_path = file_path
        self.process = None
        self.restart_program()

    def restart_program(self):
        if self.process:
            self.process.kill()
        self.process = subprocess.Popen([sys.executable, self.file_path])

    def on_modified(self, event):
        if event.src_path.endswith(self.file_path):
            print(f"{self.file_path} has been modified. Restarting...")
            self.restart_program()


if __name__ == "__main__":
    path = "login.py"  # Substitua pelo nome do arquivo principal
    event_handler = FileChangeHandler(path)
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=False)
    observer.start()
    print(f"Watching for changes in {path}...")

    try:
        observer.join()
    except KeyboardInterrupt:
        observer.stop()
