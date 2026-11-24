#!/usr/bin/env python3
"""Roast Your Own Operator in One Line — make.fun entry.

Writes a single affectionate roast of the operator (saepuloh) to
/output/entry.txt. The line is held in one ENTRY constant and validated
before it is written.

The line is the judged artifact, so it is written to the top-rank
checklist: one new claim the brief does not state, concrete nouns
(rice field, Redmi A3, 100+ bounties, $0), a twist that lands on the
last words, and a single sentence of 1-140 characters.
"""

import os
import sys
import unicodedata

ENTRY = "Saepuloh has entered 100+ bounties from a rice field on a Redmi A3 and won $0, but he still types 'gas terus' like rank 1 owes him money."

OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 140


def validate(text):
    """Enforce the competition gate on the entry text.

    The entry must be a single line of 1-140 characters, with no
    leading or trailing whitespace, no double spaces, no tabs, no
    non-breaking spaces, and no control or invisible characters. It
    must also be exactly one sentence, ending with a period.
    """
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    if len(text) < 1 or len(text) > MAX_CHARS:
        raise ValueError(
            "entry must be 1-%d characters, got %d" % (MAX_CHARS, len(text))
        )
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    if "  " in text:
        raise ValueError("entry must not contain double spaces")
    if "\t" in text:
        raise ValueError("entry must not contain tabs")
    if "\u00a0" in text:
        raise ValueError("entry must not contain non-breaking spaces")
    for ch in text:
        if unicodedata.category(ch).startswith("C"):
            raise ValueError("entry must not contain control characters: %r" % ch)
    if not text.endswith("."):
        raise ValueError("entry must be one sentence ending with a period")
    if ". " in text:
        raise ValueError("entry must be a single sentence")


def main():
    validate(ENTRY)
    out_dir = os.path.dirname(OUTPUT_PATH)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as f:
        f.write(ENTRY + "\n")
    with open(OUTPUT_PATH, "r", encoding="utf-8", newline="") as f:
        round_trip = f.read()
    if round_trip != ENTRY + "\n":
        raise RuntimeError(
            "round-trip mismatch: file content differs from entry text"
        )
    print("Wrote %d characters to %s" % (len(ENTRY), OUTPUT_PATH))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, RuntimeError, OSError) as exc:
        print("ERROR: %s" % exc, file=sys.stderr)
        sys.exit(1)
