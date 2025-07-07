from pathlib import Path
import os
import re
import sys


node_pattern = re.compile(r'^\s*\[node\s+name="(?P<name>[^"]+)"', re.IGNORECASE)
pascal_pattern = re.compile(r"([A-Z][a-z0-9]*)+")

def check_pascal(name: str) -> bool:
    return bool(pascal_pattern.fullmatch(name))

def scan_file(path: str):
    errors = []
    with open(path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            m = node_pattern.match(line)
            if m:
                name = m.group('name')
                if not check_pascal(name):
                    errors.append((i, name))
    return errors

def main() -> int:
    root = Path.cwd()
    bad = {}

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]
        if 'addons' in Path(dirpath).parts:
            continue
        for fname in filenames:
            if not fname.lower().endswith('.tscn'):
                continue
            file_path = Path(dirpath) / fname
            errs = scan_file(str(file_path))
            if errs:
                rel = file_path.relative_to(root)
                bad[str(rel)] = errs

    if bad:
        print("the following .tscn files contain node names in the wrong format:")
        for file, errs in bad.items():
            for line, name in errs:
                print(f"  - {file}:{line} → '{name}' is not PascalCase")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
