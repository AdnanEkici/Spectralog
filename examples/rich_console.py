"""Demonstrate Rich-based console logging with SpectraLog.

Rich console output improves readability by providing formatted levels, source
locations, timestamps, and enhanced tracebacks.

Use this configuration when console readability is important during development
or interactive application execution.
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
from spectralog import RichConsoleConfiguration  # noqa: E402
from spectralog.core.logger import ApplicationLogger  # noqa: E402


def main() -> None:
    """Configure and demonstrate Rich console logging."""
    rich_console_configuration = RichConsoleConfiguration(
        show_time=True,
        show_level=True,
        show_path=True,
        rich_tracebacks=True,
        markup=False,
    )

    logger: ApplicationLogger = CreateSpectraLogger(
        debug_mode=True,
        rich_console_configuration=rich_console_configuration,
        log_file_name="rich-console-example.log",
    )

    logger.debug(
        "Debug message rendered through Rich",
    )

    logger.info(
        "Application started with Rich console output",
    )

    logger.warning(
        "Something requires attention",
    )

    try:
        raise RuntimeError(
            "Example application failure",
        )
    except RuntimeError:
        logger.exception(
            "Rich traceback example",
        )


if __name__ == "__main__":
    main()