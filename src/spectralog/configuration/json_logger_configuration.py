from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class JsonLoggerConfiguration:
    """Configure the fields included in SpectraLog JSON log records.

    This immutable configuration object controls which optional metadata fields
    are emitted by SpectraLog's JSON formatter.

    The log level and message are always included in each JSON log record. The
    options defined here only control additional metadata such as timestamps,
    logger names, process information, and thread information.

    Instances are frozen and use slots, preventing configuration values from being
    modified after creation or arbitrary attributes from being added dynamically.

    Attributes:
        include_timestamp:
            Includes a timestamp field in each JSON log record when ``True``.
            Defaults to ``True``.

        include_logger_name:
            Includes the originating logger name in each JSON log record when
            ``True``. Defaults to ``True``.

        include_process_information:
            Includes process-related metadata, such as the process identifier and
            process name, in each JSON log record when ``True``. Defaults to
            ``True``.

        include_thread_information:
            Includes thread-related metadata, such as the thread identifier and
            thread name, in each JSON log record when ``True``. Defaults to
            ``True``.

    Example:
        Configure JSON logging with selected metadata disabled::

            from spectralog import JsonLoggerConfiguration

            json_configuration = JsonLoggerConfiguration(
                include_timestamp=True,
                include_logger_name=False,
                include_process_information=False,
                include_thread_information=False,
            )
    """

    include_timestamp: bool = True
    include_logger_name: bool = True
    include_process_information: bool = True
    include_thread_information: bool = True
