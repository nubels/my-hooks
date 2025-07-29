from pathlib import Path
import os
import re
import sys


node_pattern = re.compile(r'^\s*\[node\s+name="(?P<name>[^"]+)"', re.IGNORECASE)
pascal_pattern = re.compile(r"([A-Z][a-z0-9]*)+")


def scan_file(path: str):
    errors = []
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            match = node_pattern.match(line)
            if match:
                node_name = match.group("name")
                if not pascal_pattern.fullmatch(node_name):
                    errors.append(node_name)

    return errors


def main() -> int:
    non_pascal_cases = []

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith(".") and d != "addons"]
        filenames[:] = [
            f for f in filenames if not f.startswith(".") and f.endswith(".tscn")
        ]

        for file_name in filenames:
            file_path = Path(dirpath) / file_name

            errors = scan_file(str(file_path))

            if errors:
                non_pascal_cases.append((str(file_path), errors))

    if non_pascal_cases:
        for file_path, errors in non_pascal_cases:
            for error in errors:
                print(f"{file_path}: '{error}' is not PascalCase")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
