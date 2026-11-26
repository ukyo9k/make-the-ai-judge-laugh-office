#!/usr/bin/env python3
"""Make the AI Judge Laugh — make.fun bounty entry.

Writes one original one-line joke about office life to
/output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt when set).

The joke is written in this file, guarded (non-empty, 1-200
characters, exactly one line, no leading/trailing whitespace,
no control characters), then written out and verified by reading
it back and confirming the round-trip is byte-identical with no
trailing newline.
"""

import os
import sys

JOKE = (
    "The office coffee is so weak it apologized to me, then asked "
    "to schedule a meeting to discuss its own performance."
)

MAX_CHARS = 200


def validate(text: str) -> None:
    if not text:
        raise ValueError("entry is empty")
    if len(text) > MAX_CHARS:
        raise ValueError(f"entry is {len(text)} chars, over the {MAX_CHARS} limit")
    if text != text.strip():
        raise ValueError("entry has leading or trailing whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 32 for ch in text):
        raise ValueError("entry contains control characters")
    if "  " in text:
        raise ValueError("entry contains a double space")


def main() -> int:
    validate(JOKE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = JOKE.encode("utf-8")
    with open(path, "wb") as fh:
        fh.write(data)
    with open(path, "rb") as fh:
        if fh.read() != data:
            raise RuntimeError("round-trip verification failed")
    print(f"wrote {len(data)} bytes to {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
