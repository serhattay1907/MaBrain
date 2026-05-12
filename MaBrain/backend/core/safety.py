"""
MabrAIn — Whitelist Safety Guard (Conscience Agent)
Blocks any file-system operation on paths outside the user-approved folders.
Also hard-blocks dangerous system directories regardless of whitelist.

This is NOT a security system — it's protection against LLM mistakes.
"""

import os
from pathlib import Path

from core.config import settings
from core.logger import logger

# Hard-blocked prefixes — never allow, ever
BLOCKED_PREFIXES = [
    "/etc", "/usr", "/bin", "/sbin", "/boot", "/sys", "/proc", "/dev",
    "C:\\Windows", "C:\\Program Files", "C:\\Program Files (x86)",
    "C:\\ProgramData",
]


class SafetyError(Exception):
    """Raised when a file operation is refused by the safety guard."""


def _normalize(path: str) -> Path:
    return Path(os.path.expandvars(os.path.expanduser(path))).resolve()


def check_path(path: str) -> Path:
    """
    Validates that `path` is inside an allowed folder and not in a blocked prefix.
    Returns the resolved Path on success, raises SafetyError on refusal.
    """
    resolved = _normalize(path)

    # Hard-block check
    for blocked in BLOCKED_PREFIXES:
        if str(resolved).startswith(blocked):
            logger.warning(f"Safety guard BLOCKED: {resolved} (system path)")
            raise SafetyError(f"Access to '{resolved}' is not allowed (system directory).")

    # Whitelist check
    allowed = settings.get_allowed_folders()
    if not allowed:
        raise SafetyError(
            "No folders are whitelisted. "
            "Please configure ALLOWED_FOLDERS in .env or via onboarding."
        )

    for folder in allowed:
        if str(resolved).startswith(str(_normalize(folder))):
            return resolved

    logger.warning(f"Safety guard BLOCKED: {resolved} (not in whitelist)")
    raise SafetyError(
        f"'{resolved}' is outside the allowed folders. "
        f"Allowed: {allowed}"
    )
