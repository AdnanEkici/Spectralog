from __future__ import annotations

import logging
from logging import Formatter
from typing import cast

import colorlog
from spectralog.configuration.configuration import (
    LoggerConfiguration,
)
from spectralog.formatting.format_builder import (
    LogFormatBuilder,
)
from spectralog.levels.log_level_registry import (
    LogLevelRegistry,
)


class LoggerFormatterFactory:
    """Create SpectraLog formatters for console and plain-text file output.

    ``LoggerFormatterFactory`` centralizes construction of the formatters used by
    SpectraLog's standard console and plain-text file handlers.

    Format strings are delegated to :class:`LogFormatBuilder`, while log-level
    color mappings are obtained from the shared :class:`LogLevelRegistry`. This
    keeps formatter creation separate from both format construction and log-level
    registration.

    Console formatting uses :class:`colorlog.ColoredFormatter` so that log records
    can be rendered with level-specific colors. File formatting uses the standard
    :class:`logging.Formatter` and therefore does not include terminal color
    handling.

    Both formatter types use the ``date_format`` configured in
    :class:`LoggerConfiguration`."""

    def __init__(
        self,
        format_builder: LogFormatBuilder,
        log_level_registry: LogLevelRegistry,
    ) -> None:
        """Initialize the formatter factory with its formatting dependencies.

        Args:
            format_builder:
                Builder responsible for producing console and file format strings from
                the active :class:`LoggerConfiguration`.

            log_level_registry:
                Registry containing the current SpectraLog log-level definitions and
                their associated color mappings. The registry colors are supplied to
                the colored console formatter."""
        self._format_builder = format_builder
        self._log_level_registry = log_level_registry

    def create_console_formatter(
        self,
        configuration: LoggerConfiguration,
    ) -> logging.Formatter:
        """Create the color-aware formatter used by the standard console handler.

        The console format string is obtained from
        :meth:`LogFormatBuilder.build_console_format` and used to construct a
        :class:`colorlog.ColoredFormatter`.

        The formatter receives the current color mapping from
        :class:`LogLevelRegistry`, allowing both built-in and registered custom log
        levels to be rendered with their configured colors.

        The configured ``date_format`` is passed through to the formatter, and color
        reset behavior is enabled so that terminal styling does not leak into
        subsequent output.

        Args:
            configuration:
                Logger configuration used to determine the console format and date
                format.

        Returns:
            logging.Formatter:
                A configured :class:`colorlog.ColoredFormatter` suitable for standard
                SpectraLog console output."""
        console_format = self._format_builder.build_console_format(
            configuration,
        )

        console_formatter = colorlog.ColoredFormatter(
            fmt=console_format,
            datefmt=configuration.date_format,
            log_colors=self._log_level_registry.colors,
            reset=True,
        )

        configured_console_formatter = cast(
            Formatter,
            console_formatter,
        )

        return configured_console_formatter

    def create_file_formatter(
        self,
        configuration: LoggerConfiguration,
    ) -> logging.Formatter:
        """Create the formatter used for plain-text file logging.

        The file format string is obtained from
        :meth:`LogFormatBuilder.build_file_format` and used to construct a standard
        :class:`logging.Formatter`.

        Unlike the console formatter, the file formatter does not apply terminal
        colors. The configured ``date_format`` is passed directly to the standard
        logging formatter.

        Args:
            configuration:
                Logger configuration used to determine the plain-text file format and
                date format.

        Returns:
            logging.Formatter:
                A configured standard-library formatter suitable for plain-text file
                logging."""
        file_format = self._format_builder.build_file_format(
            configuration,
        )

        file_formatter = logging.Formatter(
            fmt=file_format,
            datefmt=configuration.date_format,
        )

        configured_file_formatter = file_formatter
        return configured_file_formatter
