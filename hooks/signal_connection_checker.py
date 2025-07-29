from pathlib import Path
import os
import sys
import re

signal_connection_pattern = re.compile(r"^\s*\[connection\b", re.IGNORECASE)


def has_signal_connection(tscn_path: str) -> bool:
    with open(tscn_path, "r", encoding="utf-8") as f:
        for line in f:
            if signal_connection_pattern.match(line):
                return True
    return False


def main() -> int:
    root = Path.cwd()
    scene_files_with_signal_connections = []

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith(".") and d != "addons"]
        filenames[:] = [
            f for f in filenames if not f.startswith(".") and f.endswith(".tscn")
        ]

        for file_name in filenames:
            file_path = Path(dirpath) / file_name

            if has_signal_connection(str(file_path)):
                scene_files_with_signal_connections.append(str(file_path))

    if scene_files_with_signal_connections:
        for file_path in scene_files_with_signal_connections:
            print(f"{file_path} contains one ore more signal connections.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
