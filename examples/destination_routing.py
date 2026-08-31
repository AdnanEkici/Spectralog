"""Demonstrate per-record console and file destination routing.

SpectraLog can decide where an individual log record should be emitted without
changing the logger's global configuration.

This is useful when some messages should appear only on the console, only in a
log file, in both places, or in neither destination.
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
from spectralog.core.logger import ApplicationLogger  # noqa: E402


def main() -> None:
    """Emit records using different console and file routing combinations."""
    logger: ApplicationLogger = CreateSpectraLogger(
        debug_mode=True,
        save_logs=True,
        logs_directory=LOGS_DIRECTORY,
        log_file_name="routing-example.log",
    )

    logger.info(
        "This message is written to both console and file",
    )

    logger.info(
        "This message appears only in the console",
        console=True,
        file=False,
    )

    logger.info(
        "This message appears only in the log file",
        console=False,
        file=True,
    )

    logger.info(
        "This message is discarded by console and file routing",
        console=False,
        file=False,
    )

    logger.add_log_level(
        name="NOTICE",
        color="purple",
        severity=35,
    )

    logger.notice(  # type: ignore[attr-defined]
        "Custom level written only to the console",
        console=True,
        file=False,
    )

    logger.notice(  # type: ignore[attr-defined]
        "Custom level written only to the file",
        console=False,
        file=True,
    )

    logger.shutdown()


if __name__ == "__main__":
    main()