from __future__ import annotations

import sys
from pathlib import Path

from spectralog import CreateSpectraLogger  # noqa: E402
from spectralog import get_logger  # noqa: E402
from spectralog import JsonLoggerConfiguration  # noqa: E402
from spectralog import RichConsoleConfiguration  # noqa: E402
from spectralog import SyslogConfiguration  # noqa: E402
from spectralog.core.logger import ApplicationLogger  # noqa: E402


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIRECTORY = PROJECT_ROOT / "src"

sys.path.insert(0, str(SOURCE_DIRECTORY))


if __name__ == "__main__":
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
        syslog_configuration=syslog_configuration,
        rich_console_configuration=rich_console_configuration,
        json_logger_configuration=json_logger_configuration,
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

    logger.debug(
        "Debug message",
    )

    logger.info(
        "Application started",
    )

    logger.success(  # type: ignore[attr-defined]
        "Application initialized successfully",
    )

    logger.warning(
        "Warning message",
    )

    logger.notice(  # type: ignore[attr-defined]
        "Notice message",
    )

    logger.error(
        "Error message",
    )

    get_logger().critical(
        "Critical message",
    )

    get_logger().debug(
        "Debug message",
    )

    get_logger().info(
        "Application started",
    )

    get_logger().success(  # type: ignore[attr-defined]
        "Application initialized successfully",
    )

    get_logger().warning(
        "Warning message",
    )

    get_logger().notice(  # type: ignore[attr-defined]
        "Notice message",
    )

    get_logger().error(
        "Error message",
    )

    get_logger().critical(
        "Critical message",
    )

    logger.info(
        "Hello from SpectraLog syslog.",
    )

    logger.info(
        "Application started with Rich console output.",
    )

    logger.warning(
        "Something requires attention.",
    )

    logger.info(
        "Application started with JSON file logging.",
    )
