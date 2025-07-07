from pathlib import Path
import os
import sys

PASS = 0
FAIL = 1


def separate_compound_words(s: str) -> str:
    if not s:
        return s

    length = len(s)
    start = 0
    words = []

    def is_upper(c):
        return c.isupper()

    def is_lower(c):
        return c.islower()

    def is_digit(c):
        return c.isdigit()

    prev_upper = is_upper(s[0])
    prev_lower = is_lower(s[0])
    prev_digit = is_digit(s[0])

    for i in range(1, length):
        curr = s[i]
        curr_upper = is_upper(curr)
        curr_lower = is_lower(curr)
        curr_digit = is_digit(curr)

        next_lower = False
        if i + 1 < length:
            next_lower = is_lower(s[i + 1])

        cond_a = prev_lower and curr_upper
        cond_b = (prev_upper or prev_digit) and curr_upper and next_lower
        cond_c = prev_digit and curr_lower and next_lower
        cond_d = (prev_upper or prev_lower) and curr_digit

        if cond_a or cond_b or cond_c or cond_d:
            words.append(s[start:i])
            start = i

        prev_upper = curr_upper
        prev_lower = curr_lower
        prev_digit = curr_digit

    words.append(s[start:])

    result = " ".join(words)
    chars = []
    for ch in result:
        if ch.isspace() or ch == "_" or ch == "-":
            chars.append(" ")
        else:
            chars.append(ch)
    return "".join(chars).lower()


def to_snake_case(s: str) -> str:
    return separate_compound_words(s).replace(" ", "_")


def main() -> int:
    root = os.getcwd()
    bad = []

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]
        filenames = [f for f in filenames if not f.startswith('.')]

        parts = dirpath.split(os.sep)

        if 'addons' in parts:
            continue
        
        if 'LICENSE' in parts:
            continue
        
        if 'README' in parts:
            continue

        for name in filenames + dirnames:
            rel = os.path.relpath(os.path.join(dirpath, name), root)

            p = Path(name)
            suffixes = "".join(p.suffixes)
            stem = p.name[: len(p.name) - len(suffixes)]

            snake_stem = to_snake_case(stem)
            expected = snake_stem + suffixes

            if name != expected:
                bad.append((rel, expected))

    if bad:
        for rel, expected in bad:
            print(f"  - {rel} is not snake_case. should be: {expected}")
        return FAIL

    return PASS


if __name__ == "__main__":
    sys.exit(main())
