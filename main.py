"""Write the out-of-office entry line to entry.txt.

Deterministic: no network, no randomness, no time dependence.
The entry is a single line of at most 140 characters.
"""

import os
import sys

# The entry: one line, nothing else.
ENTRY = "I'm out of office until Monday. My inbox is being watched by my cat, who has already ignored your email twice."


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("error: MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1

    # Self-check: exactly one non-blank line, 1-140 characters.
    lines = ENTRY.splitlines()
    if len(lines) != 1:
        print("error: entry must be exactly one line", file=sys.stderr)
        return 1
    if not ENTRY.strip():
        print("error: entry must not be blank", file=sys.stderr)
        return 1
    if ENTRY != ENTRY.strip():
        print("error: entry must not have leading or trailing whitespace",
              file=sys.stderr)
        return 1
    if not 1 <= len(ENTRY) <= 140:
        print(f"error: entry is {len(ENTRY)} characters, must be 1-140",
              file=sys.stderr)
        return 1
    if "http://" in ENTRY or "https://" in ENTRY:
        print("error: entry must not contain a link", file=sys.stderr)
        return 1

    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(ENTRY + "\n")

    # Re-read what was written and verify it matches the checked entry.
    with open(path, "r", encoding="utf-8", newline="\n") as f:
        written = f.read()
    if written != ENTRY + "\n":
        print("error: written entry does not match the checked entry",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
