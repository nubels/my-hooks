# https://stackoverflow.com/questions/5141437/filtering-os-walk-dirs-and-files
# https://stackoverflow.com/questions/678236 how-do-i-get-the-filename-without-the-extension-from-a-path-in-python

from pathlib import Path
import os
import re
import sys


SNAKE_CASE = r"[a-z][a-z0-9]*(_[a-z0-9]+)*"
snake_case_pattern = re.compile(f"^{SNAKE_CASE}$")


def main() -> int:
    non_snake_case_paths = []

    for dirpath, dirnames, filenames in os.walk(root_path):
        dirnames[:] = [d for d in dirnames if not d.startswith(".") and d != "addons"]
        filenames[:] = [
            f
            for f in filenames
            if not f.startswith(".") and not f.endswith((".import", ".uid"))
        ]

        for name in dirnames + filenames:
            path = os.path.join(dirpath, name)
            stem = Path(path).stem
            if not snake_case_pattern.fullmatch(stem):
                non_snake_case_paths.append(path)

    if non_snake_case_paths:
        for path in non_snake_case_paths:
            print(f"{path} is not snake_case.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
