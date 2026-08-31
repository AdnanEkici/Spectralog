"""Demonstrate several SpectraLog features in one complete configuration.

This example combines console formatting, JSON logging, Syslog forwarding,
multiprocessing-safe logging, custom levels, logger retrieval, and per-record
destination routing.

Use the smaller feature-specific examples when learning individual features and
this file when reviewing how those features can be configured together.
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
from spectralog import JsonLoggerConfiguration  # noqa: E402
from spectralog import RichConsoleConfiguration  # noqa: E402
from spectralog import SyslogConfiguration  # noqa: E402
from spectralog.core.logger import ApplicationLogger  # noqa: E402


def main() -> None:
    """Configure and exercise several SpectraLog features together."""
    syslog_configuration = SyslogConfiguration(
        host="localhost",
        port=514,
    )

    rich_console_configuration = RichConsoleConfiguration(
        show_time=True,
        show_level=True,
        show_path=True,
        rich_tracebacks=True,
        markup=False,
    )

    json_logger_configuration = JsonLoggerConfiguration(
        include_timestamp=True,
        include_logger_name=True,
        include_process_information=True,
        include_thread_information=True,
    )

    logger: ApplicationLogger = CreateSpectraLogger(
        debug_mode=True,
        show_datetime=True,
        show_folder_name=True,
        show_line=True,
        multiprocessing_safe=True,
        log_file_name="fully-configured-example.log",
        syslog_configuration=syslog_configuration,
        rich_console_configuration=rich_console_configuration,
        json_logger_configuration=json_logger_configuration,
    )

    logger.add_log_level(
        name="SUCCESS",
        color="bold_green",
        severity=25,
    )

    logger.add_log_level(
        name="NOTICE",
        color="purple",
        severity=35,
    )

    logger.debug(
        "Debug message",
    )

    logger.info(
        "Application started",
    )

    logger.success(  # type: ignore[attr-defined]
        "Application initialized successfully",
    )

    logger.notice(  # type: ignore[attr-defined]
        "Notice message",
    )

    logger.warning(
        "Warning message",
    )

    logger.error(
        "Error message",
    )

    logger.critical(
        "Critical message",
    )

    get_logger().info(
        "Retrieved the current process-local ApplicationLogger",
    )

    logger.notice(  # type: ignore[attr-defined]
        "Console-only custom message",
        console=True,
        file=False,
    )

    logger.notice(  # type: ignore[attr-defined]
        "File-only custom message",
        console=False,
        file=True,
    )

    logger.shutdown()


if __name__ == "__main__":
    main()