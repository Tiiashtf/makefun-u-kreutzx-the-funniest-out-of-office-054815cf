#!/usr/bin/env python3
"""Out-of-office entry for make.fun's "The Funniest Out-of-Office" bounty.

Writes a single funny one-line out-of-office auto-reply to
/output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt). Deterministic,
stdlib only, no network, no secrets.

The line: one idea, told straight. The sender is not on holiday at all —
they are hiding from their inbox, and the auto-reply itself is the cover
story. The punch lands on the last word, "alibi", which reframes the
whole reply as a small conspiracy between the sender and the reader.
"""

import os
import shutil
import sys

LINE = (
    "Out of office until Friday. I'm not on holiday, I'm hiding from my "
    "inbox, and this auto-reply is my alibi."
)


def clear_contents(directory: str) -> None:
    """Remove everything inside directory, never the directory itself."""
    for name in os.listdir(directory):
        path = os.path.join(directory, name)
        if os.path.islink(path):
            # Unlink the link itself; never follow it.
            os.unlink(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)
        else:
            # Regular files, fifos, sockets: unlink.
            os.unlink(path)


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    clear_contents(out_dir)

    target = os.path.join(out_dir, "entry.txt")
    with open(target, "w", encoding="utf-8", newline="") as handle:
        handle.write(LINE)

    # Verify what we wrote, byte for byte.
    with open(target, "rb") as handle:
        data = handle.read()
    encoded = LINE.encode("utf-8")
    if data != encoded:
        raise SystemExit("entry.txt does not match the line")
    if not 1 <= len(LINE) <= 140:
        raise SystemExit("line must be 1-140 characters")
    if LINE != LINE.strip():
        raise SystemExit("line must not start or end with whitespace")
    if not LINE.strip():
        raise SystemExit("line must not be only whitespace")
    if "\n" in LINE or "\r" in LINE:
        raise SystemExit("line must be a single line")
    if len(data) != len(LINE):
        raise SystemExit("line must be plain ASCII so bytes equal characters")
    return 0


if __name__ == "__main__":
    sys.exit(main())
