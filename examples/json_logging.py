"""Demonstrate structured JSON file logging with SpectraLog.

JSON logs are useful when records are consumed by log aggregation systems,
search platforms, monitoring infrastructure, or other automated tooling.

This example enables structured metadata such as timestamps, logger names,
process information, and thread information.
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
from spectralog import JsonLoggerConfiguration  # noqa: E402
from spectralog.core.logger import ApplicationLogger  # noqa: E402


def main() -> None:
    """Configure SpectraLog to write structured JSON log records."""
    json_logger_configuration = JsonLoggerConfiguration(
        include_timestamp=True,
        include_logger_name=True,
        include_process_information=True,
        include_thread_information=True,
    )

    logger: ApplicationLogger = CreateSpectraLogger(
        debug_mode=True,
        save_logs=True,
        logs_directory=LOGS_DIRECTORY,
        log_file_name="jsonl-example.jsonl",
        json_logger_configuration=json_logger_configuration,
    )

    logger.info(
        "Application started with JSON file logging",
    )

    logger.warning(
        "Structured warning message",
    )

    logger.error(
        "Structured error message",
    )

    logger.shutdown()


if __name__ == "__main__":
    main()