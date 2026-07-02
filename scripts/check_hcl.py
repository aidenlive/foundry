#!/usr/bin/env python3
"""Parse every .tf file in the repository with python-hcl2.

A cheap, registry-free syntax gate for CI environments that cannot reach
provider registries. `tofu validate` remains the authoritative check and runs
in the stack pipeline (see .github/workflows/terraform-reusable.yml).
"""

from __future__ import annotations

import sys
from pathlib import Path

try:
    import hcl2
except ImportError:
    print("python-hcl2 is not installed: pip install python-hcl2", file=sys.stderr)
    sys.exit(2)

SKIP_PARTS = {".terraform", ".foundry", ".venv", "node_modules", "site"}


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    failures = 0
    files = sorted(
        p for p in root.rglob("*.tf") if not (set(p.parts) & SKIP_PARTS)
    )
    for path in files:
        try:
            with path.open() as handle:
                hcl2.load(handle)
        except Exception as exc:  # noqa: BLE001 - report every parse failure
            failures += 1
            print(f"FAIL {path.relative_to(root)}: {exc}", file=sys.stderr)
    print(f"checked {len(files)} .tf files, {failures} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
