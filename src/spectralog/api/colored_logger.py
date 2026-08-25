from __future__ import annotations

from pathlib import Path

from spectralog.configuration.configuration import LoggerConfiguration
from spectralog.configuration.json_logger_configuration import JsonLoggerConfiguration
from spectralog.configuration.rich_console_configuration import RichConsoleConfiguration
from spectralog.configuration.syslog_configuration import SyslogConfiguration
from spectralog.core.factory import ApplicationLoggerBuilderFactory
from spectralog.core.logger import ApplicationLogger
from spectralog.levels.log_level_registry import LogLevelRegistry


def CreateSpectraLogger(
    debug_mode: bool = False,
    show_datetime: bool = True,
    show_line: bool = False,
    show_folder_name: bool = False,
    logs_directory: str | Path = "logs",
    log_file_name: str | None = None,
    save_logs: bool = True,
    multiprocessing_safe: bool = False,
    syslog_configuration: SyslogConfiguration | None = None,
    rich_console_configuration: RichConsoleConfiguration | None = None,
    json_logger_configuration: JsonLoggerConfiguration | None = None,
    console_format: str | None = None,
    file_format: str | None = None,
    date_format: str = "%Y-%m-%d %H:%M:%S",
    max_bytes: int = 20 * (1024**2),
    backup_count: int = 1,
) -> ApplicationLogger:
    """Create and configure the process-wide SpectraLog application logger.

    This function is the primary entry point for initializing SpectraLog.
    It creates a :class:`LoggerConfiguration`, composes the required logger
    infrastructure, and initializes the process-local
    :class:`ApplicationLogger` singleton.

    The application logger should normally be initialized once near the
    application's entry point. After initialization, other modules should use
    :func:`get_logger` to retrieve the existing logger rather than calling
    ``CreateSpectraLogger`` again.

    Console logging is always configured. When ``save_logs`` is enabled,
    SpectraLog additionally creates a file handler using either plain-text or
    JSON Lines formatting. Rich console output, syslog output, and
    multiprocessing-safe file logging can be enabled independently through
    their corresponding configuration options.

    When ``json_logger_configuration`` is supplied, file logging uses JSON
    Lines format and the resolved log file has a ``.jsonl`` extension.
    Otherwise, standard text formatting is used.

    When ``rich_console_configuration`` is supplied, the Rich console handler
    is used instead of the standard colored console handler.

    Args:
        debug_mode:
            Enables debug-level logging when ``True``. The logger and its
            configured handlers use :data:`logging.DEBUG` as their minimum
            level. When ``False``, the minimum level is
            :data:`logging.INFO`. Defaults to ``False``.

        show_datetime:
            Includes the formatted timestamp in automatically generated
            plain-text console and file formats when ``True``. This option
            does not affect an explicitly supplied ``console_format`` or
            ``file_format``. Defaults to ``True``.

        show_line:
            Includes the source line number in automatically generated
            plain-text formats when ``True``. When
            ``show_folder_name`` is also enabled, the line number is appended
            to the relative source path. Otherwise, it is rendered as a
            standalone line component. Defaults to ``False``.

        show_folder_name:
            Includes the source file path relative to the detected project
            root in automatically generated plain-text formats when ``True``.
            The relative path is populated by SpectraLog's relative-path
            logging filter. Defaults to ``False``.

        logs_directory:
            Directory in which log files are created. A string or
            :class:`pathlib.Path` may be supplied. The directory is expanded,
            resolved, and created when file logging is enabled. Defaults to
            ``"logs"``.

        log_file_name:
            Optional custom log file name. When omitted, SpectraLog generates
            a daily file name from the current date. When JSON logging is
            enabled, the file suffix is changed to ``.jsonl`` regardless of
            the supplied suffix. Defaults to ``None``.

        save_logs:
            Enables persistent file logging when ``True``. When ``False``,
            SpectraLog does not resolve or create a log file and no file
            handler is attached. Console and optionally configured syslog
            logging remain available. Defaults to ``True``.

        multiprocessing_safe:
            Routes file log records through SpectraLog's multiprocessing
            queue and listener infrastructure when ``True``. This prevents
            the application's logger from writing directly to the file
            handler in the initializing process and ensures queued records
            are flushed during logger shutdown. Defaults to ``False``.

            This option applies to the multiprocessing runtime created by
            this logger instance. Independently initialized processes do not
            automatically share the same queue or listener.

        syslog_configuration:
            Optional :class:`SyslogConfiguration` describing the remote
            syslog host, port, facility, and socket type. When supplied, a
            syslog handler is attached in addition to the configured console
            and file handlers. Defaults to ``None``.

        rich_console_configuration:
            Optional :class:`RichConsoleConfiguration` controlling Rich
            console rendering. When supplied, SpectraLog uses a Rich console
            handler instead of its standard colored console handler. Defaults
            to ``None``.

        json_logger_configuration:
            Optional :class:`JsonLoggerConfiguration` controlling structured
            file logging. When supplied, file records are serialized as
            JSON Lines and the log file uses the ``.jsonl`` extension.
            Defaults to ``None``.

        console_format:
            Optional explicit format string for the standard colored console
            formatter. When supplied, it overrides the console format that
            would otherwise be generated from ``show_datetime``,
            ``show_line``, and ``show_folder_name``. Defaults to ``None``.

            This setting applies to the standard console formatter and is not
            used to format Rich console output.

        file_format:
            Optional explicit format string for plain-text file logging.
            When supplied, it overrides the automatically generated file
            format. JSON logging uses its JSON formatter instead of this
            format string. Defaults to ``None``.

        date_format:
            Date and time format passed to logging formatters that render an
            ``%(asctime)s`` value. Defaults to
            ``"%Y-%m-%d %H:%M:%S"``.

        max_bytes:
            Maximum size, in bytes, of a plain or JSON log file before the
            rotating file handler performs a rollover. Defaults to
            ``20 * (1024**2)``, or 20 MiB.

        backup_count:
            Number of rotated backup log files retained by the rotating file
            handler. Defaults to ``1``.

    Returns:
        ApplicationLogger:
            The initialized process-local SpectraLog application logger.
            Subsequent calls to :func:`get_logger` return this same
            :class:`ApplicationLogger` instance.

    Raises:
        SpectraApplicationLoggerReconfigurationError:
            If ``CreateSpectraLogger`` is called after the application logger
            has already been initialized. SpectraLog does not permit the
            existing process-local singleton to be reconfigured.

    Example:
        Initialize SpectraLog once at the application entry point::

            from spectralog import CreateSpectraLogger

            logger = CreateSpectraLogger(
                debug_mode=True,
                logs_directory="logs",
                log_file_name="application.log",
            )

            logger.info("Application started")

        Retrieve the same logger elsewhere in the application with
        :func:`get_logger` rather than initializing it again.
    """
    configuration = LoggerConfiguration(
        debug_mode=debug_mode,
        show_datetime=show_datetime,
        show_line=show_line,
        show_folder_name=show_folder_name,
        logs_directory=logs_directory,
        log_file_name=log_file_name,
        save_logs=save_logs,
        multiprocessing_safe=multiprocessing_safe,
        syslog_configuration=syslog_configuration,
        rich_console_configuration=rich_console_configuration,
        json_logger_configuration=json_logger_configuration,
        console_format=console_format,
        file_format=file_format,
        date_format=date_format,
        max_bytes=max_bytes,
        backup_count=backup_count,
    )

    log_level_registry = LogLevelRegistry()

    logger_builder_factory = ApplicationLoggerBuilderFactory(
        log_level_registry=log_level_registry,
    )

    logger_builder = logger_builder_factory.create(
        configuration=configuration,
    )

    application_logger = ApplicationLogger.get_instance(
        logger_builder=logger_builder,
        log_level_registry=log_level_registry,
    )

    return application_logger


def get_logger() -> ApplicationLogger:
    """Return the process-local SpectraLog application logger.

    Returns the existing :class:`ApplicationLogger` singleton when SpectraLog has
    already been initialized. This is the recommended way for application modules
    to access the logger after the initial call to :func:`CreateSpectraLogger`.

    If the application logger has not yet been initialized, a default logger is
    created using SpectraLog's default configuration.

    Returns:
        ApplicationLogger:
            The process-local SpectraLog application logger instance. Repeated
            calls return the same singleton instance for the lifetime of the
            process.

    Example:
        Initialize SpectraLog once at application startup::

            from spectralog import CreateSpectraLogger

            CreateSpectraLogger(
                debug_mode=True,
                log_file_name="application.log",
            )

        Retrieve the existing logger from another module::

            from spectralog import get_logger

            logger = get_logger()
            logger.info("Processing started")
    """
    application_logger = ApplicationLogger.get_instance()

    return application_logger
