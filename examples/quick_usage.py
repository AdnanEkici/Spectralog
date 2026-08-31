"""Show the simplest way to initialize and use SpectraLog.

This example demonstrates the standard application workflow: create the
process-local SpectraLog logger once, then retrieve and use it throughout the
application.

Use this example as the starting point when learning the package.
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
    """Create a basic SpectraLog logger and emit standard log messages."""
    logger: ApplicationLogger = CreateSpectraLogger(
        debug_mode=True,
    )

    logger.debug(
        "Debug message",
    )

    logger.info(
        "Application started",
    )

    logger.warning(
        "Something requires attention",
    )

    logger.error(
        "An error occurred",
    )

    get_logger().critical(
        "Critical application failure",
    )


if __name__ == "__main__":
    main()