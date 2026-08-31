"""Demonstrate registering and using custom SpectraLog log levels.

Custom levels are useful when the standard DEBUG, INFO, WARNING, ERROR, and
CRITICAL levels do not express enough application-specific meaning.

This example creates SUCCESS and NOTICE levels and shows both dynamic method
usage and the generic log() API.
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIRECTORY = PROJECT_ROOT / "src"

sys.path.insert(
    0,
    str(SOURCE_DIRECTORY),
)

from spectralog import CreateSpectraLogger  # noqa: E402
from spectralog import get_logger  # noqa: E402
from spectralog.core.logger import ApplicationLogger  # noqa: E402


def main() -> None:
    """Register custom log levels and emit records using them."""
    logger: ApplicationLogger = CreateSpectraLogger(
        debug_mode=True,
        log_file_name="custom-log-levels-example.log",
    )

    logger.add_log_level(
        name="SUCCESS",
        color="bold_green",
        severity=25,
    )

    get_logger().add_log_level(
        name="NOTICE",
        color="purple",
        severity=35,
    )

    logger.success(  # type: ignore[attr-defined]
        "Application initialized successfully",
    )

    logger.notice(  # type: ignore[attr-defined]
        "Scheduled maintenance begins shortly",
    )

    logger.log(
        "SUCCESS",
        "SUCCESS emitted through logger.log()",
    )

    logger.log(
        "NOTICE",
        "NOTICE emitted through logger.log()",
    )


if __name__ == "__main__":
    main()