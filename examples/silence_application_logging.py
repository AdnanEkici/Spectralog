"""Demonstrate temporarily silencing SpectraLog for a function or method.

The silence_application_logging decorator is useful when a specific operation
should run without producing console output, log files, or other SpectraLog
side effects.

Unlike disable_application_logging, this decorator is not tied to unittest
classes and can be applied directly to ordinary functions and methods.
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIRECTORY = PROJECT_ROOT / "src"
LOGS_DIRECTORY = PROJECT_ROOT / "logs"

sys.path.insert(
    0,
    str(SOURCE_DIRECTORY),
)

from spectralog import CreateSpectraLogger  # noqa: E402
from spectralog import get_logger  # noqa: E402
from spectralog import silence_application_logging  # noqa: E402


@silence_application_logging
def execute_without_logging() -> None:
    """Use SpectraLog normally while suppressing logging output."""
    logger = get_logger()

    logger.info(
        "This message is suppressed",
    )

    logger.warning(
        "This warning is suppressed",
    )

    logger.error(
        "This error is suppressed",
    )


@silence_application_logging
def initialize_without_logging() -> None:
    """Initialize SpectraLog while preventing real logging infrastructure."""
    logger = CreateSpectraLogger(
        save_logs=True,
        logs_directory=LOGS_DIRECTORY,
        log_file_name="silenced-example.log",
    )

    logger.info(
        "This message does not create the configured log file",
    )


def main() -> None:
    """Run examples of function-level SpectraLog suppression."""
    execute_without_logging()
    initialize_without_logging()


if __name__ == "__main__":
    main()