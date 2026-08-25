from __future__ import annotations

import logging
from logging import Handler
from typing import cast

from rich.logging import RichHandler
from spectralog.configuration.configuration import LoggerConfiguration
from spectralog.configuration.rich_console_configuration import (
    RichConsoleConfiguration,
)


class RichConsoleHandlerFactory:
    """Create Rich-based console handlers for SpectraLog.

    ``RichConsoleHandlerFactory`` constructs and configures the
    :class:`rich.logging.RichHandler` used when Rich console output is enabled.

    The handler's logging threshold is derived from the active
    :class:`LoggerConfiguration`, while presentation behavior such as timestamp,
    level, source path, traceback rendering, and Rich markup is controlled through
    :class:`RichConsoleConfiguration`.

    A message-only :class:`logging.Formatter` is attached to the Rich handler so
    that Rich remains responsible for rendering its own time, level, path, and
    traceback columns without duplicating SpectraLog's standard plain-text
    formatting.

    This factory is responsible only for creating and configuring the Rich
    handler. Attaching the handler to the application logger is handled by
    :class:`ApplicationLoggerBuilder`."""

    def create(
        self,
        logger_configuration: LoggerConfiguration,
        rich_configuration: RichConsoleConfiguration,
    ) -> logging.Handler:
        """Create and configure a Rich console logging handler.

        Constructs a :class:`rich.logging.RichHandler` using the effective logging
        level from ``logger_configuration`` and the presentation options defined by
        ``rich_configuration``.

        A standard :class:`logging.Formatter` containing only ``%(message)s`` is
        attached to the handler. This allows Rich to render its own structural
        elements such as timestamps, levels, source paths, and tracebacks without
        duplicating fields produced by SpectraLog's plain-text formatter.

        Args:
            logger_configuration:
                General logger configuration providing the effective logging level and
                date format.

            rich_configuration:
                Rich-specific configuration controlling timestamp visibility, level
                visibility, source-path display, enhanced traceback rendering, and
                Rich markup handling.

        Returns:
            logging.Handler:
                A configured :class:`rich.logging.RichHandler` suitable for SpectraLog
                console output."""
        rich_handler = RichHandler(
            level=logger_configuration.log_level,
            show_time=rich_configuration.show_time,
            show_level=rich_configuration.show_level,
            show_path=rich_configuration.show_path,
            rich_tracebacks=rich_configuration.rich_tracebacks,
            markup=rich_configuration.markup,
        )

        formatter = logging.Formatter(
            fmt="%(message)s",
            datefmt=logger_configuration.date_format,
        )

        rich_handler.setFormatter(
            formatter,
        )

        configured_rich_handler = cast(
            Handler,
            rich_handler,
        )

        return configured_rich_handler
