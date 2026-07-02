"""Small shared helpers for the Foundry CLI."""

from __future__ import annotations

import sys


def eprint(message: str) -> None:
    print(message, file=sys.stderr)


def parse_var_flags(pairs: list[str]) -> dict[str, str]:
    values: dict[str, str] = {}
    for pair in pairs:
        if "=" not in pair:
            raise ValueError(f"--var expects name=value, got '{pair}'")
        key, _, value = pair.partition("=")
        values[key.strip()] = value
    return values
