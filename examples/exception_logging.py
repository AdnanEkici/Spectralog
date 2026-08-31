"""Demonstrate logging exceptions and tracebacks with SpectraLog.

Exception logging records both a descriptive application message and information
about the active exception.

Use logger.exception() inside an exception handler when diagnostic traceback
information should be included automatically.
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
from spectralog.core.logger import ApplicationLogger  # noqa: E402


def main() -> None:
    """Raise and log an example exception with traceback information."""
    logger: ApplicationLogger = CreateSpectraLogger(
        debug_mode=True,
        log_file_name="exception-logging-example.log",
    )

    try:
        result = 10 / 0

        logger.info(
            "Result: %s",
            result,
        )
    except ZeroDivisionError:
        logger.exception(
            "Calculation failed",
        )


if __name__ == "__main__":
    main()