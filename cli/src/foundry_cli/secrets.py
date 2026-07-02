"""`foundry secrets` — thin, safe wrappers around sops + age.

Foundry never implements cryptography itself; it standardises *where*
encrypted material lives (config/secrets/*.enc.yaml), *how* it is governed
(.sops.yaml at the repo root) and gives operators one obvious workflow.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from .config import ConfigError

KEYGEN_HELP = """\
sops + age detected. To finish setup:

  1. age-keygen -o ~/.config/sops/age/keys.txt
  2. Copy the printed public key (age1...) into .sops.yaml under `age:`
  3. foundry secrets edit config/secrets/dev.enc.yaml

CI decrypts with SOPS_AGE_KEY held in the CI secret store, or via a cloud
KMS key configured in .sops.yaml. Never commit private keys.
"""


def _require(binary: str) -> str:
    path = shutil.which(binary)
    if not path:
        raise ConfigError(
            f"'{binary}' not found on PATH — see docs/operations/secrets.md for installation"
        )
    return path


def init(root: Path) -> str:
    _require("sops")
    _require("age")
    if not (root / ".sops.yaml").is_file():
        raise ConfigError(".sops.yaml missing at the repository root")
    return KEYGEN_HELP


def _run(args: list[str], cwd: Path) -> int:
    return subprocess.run(args, cwd=cwd).returncode  # noqa: S603 - user-invoked tool


def edit(root: Path, path: str) -> int:
    return _run([_require("sops"), path], cwd=root)


def encrypt(root: Path, path: str) -> int:
    return _run([_require("sops"), "--encrypt", "--in-place", path], cwd=root)


def decrypt(root: Path, path: str) -> int:
    return _run([_require("sops"), "--decrypt", path], cwd=root)
