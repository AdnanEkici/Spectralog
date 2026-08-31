from __future__ import annotations

import logging


SPECTRALOG_CONSOLE_ATTRIBUTE = "spectralog_console"
SPECTRALOG_FILE_ATTRIBUTE = "spectralog_file"


class ConsoleRoutingFilter(logging.Filter):
    """Filter log records according to their SpectraLog console routing flag.

    SpectraLog logging methods attach the ``spectralog_console`` attribute to
    each :class:`logging.LogRecord`. This filter allows console handlers to
    inspect that attribute and determine whether the record should be emitted.

    Records created outside SpectraLog may not contain routing metadata. Such
    records default to console output so existing Python logging behavior remains
    compatible.

    Example:
        A record emitted through::

            logger.info(
                "Console message",
                console=True,
                file=False,
            )

        contains ``spectralog_console=True`` and therefore passes this filter.
    """

    def filter(
        self,
        record: logging.LogRecord,
    ) -> bool:
        """Return whether the supplied record should reach console output.

        Args:
            record:
                Log record being considered by the console handler.

        Returns:
            bool:
                ``True`` when the record is eligible for console output,
                otherwise ``False``.
        """
        should_log_to_console = getattr(
            record,
            SPECTRALOG_CONSOLE_ATTRIBUTE,
            True,
        )

        resolved_should_log_to_console = bool(
            should_log_to_console,
        )

        return resolved_should_log_to_console


class FileRoutingFilter(logging.Filter):
    """Filter log records according to their SpectraLog file routing flag.

    SpectraLog logging methods attach the ``spectralog_file`` attribute to each
    :class:`logging.LogRecord`. File handlers use this filter to prevent records
    explicitly routed away from persistent file output from being written.

    Records without SpectraLog routing metadata default to file output. This
    preserves normal behavior for records produced directly through Python's
    standard logging API.

    Example:
        A record emitted through::

            logger.info(
                "Console-only message",
                console=True,
                file=False,
            )

        contains ``spectralog_file=False`` and is therefore rejected by this
        filter.
    """

    def filter(
        self,
        record: logging.LogRecord,
    ) -> bool:
        """Return whether the supplied record should reach file output.

        Args:
            record:
                Log record being considered by the file handler.

        Returns:
            bool:
                ``True`` when the record is eligible for file output,
                otherwise ``False``.
        """
        should_log_to_file = getattr(
            record,
            SPECTRALOG_FILE_ATTRIBUTE,
            True,
        )

        resolved_should_log_to_file = bool(
            should_log_to_file,
        )

        return resolved_should_log_to_file
