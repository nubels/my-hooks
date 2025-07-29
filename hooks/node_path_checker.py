from pathlib import Path
import os
import sys
import re

# https://chatgpt.com/share/6888dbba-f420-8000-a6e8-b1e14accee14
pattern = re.compile(r'\$(?:"([^"]+)"|([\w./]+))')


def check_node_paths(file_path: str):
    errors = []
    with open(file_path, encoding="utf-8") as f:
        for line in f:
            for grp1, grp2 in pattern.findall(line):
                node_path = grp1 or grp2
                if node_path.startswith(".."):
                    errors.append(node_path)

    return errors


def main() -> int:
    root = Path.cwd()
    invalid_node_paths = []

    for dir_path, dir_names, file_names in os.walk(root):
        dir_names[:] = [d for d in dir_names if not d.startswith(".") and d != "addons"]
        file_names[:] = [f for f in file_names if f.endswith((".gd"))]

        for filename in file_names:
            path = os.path.join(dir_path, filename)
            errors = check_node_paths(path)
            for error in errors:
                invalid_node_paths.append((path, error))

    if invalid_node_paths:
        for path, error in invalid_node_paths:
            print(f"{path}: NodePath '{error}' starts with '..'")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
