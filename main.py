#!/usr/bin/env python3
"""Fridge Roast entry for make.fun.

Writes exactly one roast line about a smart fridge to /output/entry.txt.
Deterministic: every run produces byte-identical output.
"""

import hashlib
import os
import sys

ROAST = "My smart fridge pushed a firmware update at 3 a.m., then its camera flagged my milk as 'suspicious' \u2014 now the ice maker demands a password for every cube."

OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 200


def validate(line):
    """A valid entry is one non-empty line of at most 200 characters."""
    if not line:
        raise SystemExit("roast line is empty")
    if line != line.strip():
        raise SystemExit("roast line has leading or trailing whitespace")
    if "\n" in line or "\r" in line:
        raise SystemExit("roast line must be a single line")
    if len(line) > MAX_CHARS:
        raise SystemExit(
            "roast line is %d characters, over the %d limit" % (len(line), MAX_CHARS)
        )


def main():
    line = ROAST
    validate(line)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    # No trailing newline: the file holds exactly the line, so its
    # character count is exactly len(line).
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as f:
        f.write(line)
    # Round-trip check: what landed on disk must be byte-identical to
    # the validated line, so a rerun can never silently drift.
    with open(OUTPUT_PATH, "r", encoding="utf-8", newline="") as f:
        on_disk = f.read()
    if on_disk != line:
        raise SystemExit("round-trip check failed: file differs from roast line")
    if len(on_disk) != len(line) or len(on_disk) > MAX_CHARS:
        raise SystemExit("round-trip check failed: length mismatch")
    data = line.encode("utf-8")
    print("wrote %d characters to %s" % (len(line), OUTPUT_PATH))
    print("sha256: %s" % hashlib.sha256(data).hexdigest())


if __name__ == "__main__":
    main()
