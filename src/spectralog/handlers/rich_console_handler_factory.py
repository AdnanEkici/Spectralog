from __future__ import annotations

import logging
from logging import Handler
from typing import cast

from rich.logging import RichHandler
from spectralog.configuration.configuration import LoggerConfiguration
from spectralog.configuration.rich_console_configuration import (
    RichConsoleConfiguration,
)
from spectralog.core.log_routing import ConsoleRoutingFilter


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

    A :class:`ConsoleRoutingFilter` is attached to support SpectraLog's
    per-record console routing. Records emitted with ``console=False`` are
    rejected by the Rich handler, while records emitted with ``console=True``
    remain eligible for Rich console output.

    Records created outside SpectraLog that do not contain destination-routing
    metadata default to console output, preserving compatibility with ordinary
    :mod:`logging` records.

    This factory is responsible only for creating and configuring the Rich
    handler. Attaching the handler to the application logger is handled by
    :class:`ApplicationLoggerBuilder`.
    """

    def create(
        self,
        logger_configuration: LoggerConfiguration,
        rich_configuration: RichConsoleConfiguration,
    ) -> logging.Handler:
        """Create and configure a Rich console logging handler.

        Constructs a :class:`rich.logging.RichHandler` using the effective
        logging level from ``logger_configuration`` and the presentation options
        defined by ``rich_configuration``.

        A standard :class:`logging.Formatter` containing only ``%(message)s`` is
        attached to the handler. This allows Rich to render its own structural
        elements such as timestamps, levels, source paths, and tracebacks without
        duplicating fields produced by SpectraLog's plain-text formatter.

        A :class:`ConsoleRoutingFilter` is also attached. This filter inspects the
        routing metadata added by SpectraLog's logging methods and determines
        whether the current record should be emitted by the Rich console handler.

        Records emitted with ``console=False`` are suppressed for Rich output.
        Records emitted with ``console=True`` are allowed through, subject to the
        handler's configured logging level.

        Args:
            logger_configuration:
                General logger configuration providing the effective logging
                level and date format.

            rich_configuration:
                Rich-specific configuration controlling timestamp visibility,
                level visibility, source-path display, enhanced traceback
                rendering, and Rich markup handling.

        Returns:
            logging.Handler:
                A configured :class:`rich.logging.RichHandler` with message
                formatting and per-record console routing enabled.

        Example:
            A record emitted as::

                logger.info(
                    "File-only message",
                    console=False,
                    file=True,
                )

            is rejected by the Rich console handler because
            ``console=False``.

            A record emitted as::

                logger.info(
                    "Rich console message",
                    console=True,
                    file=False,
                )

            remains eligible for Rich console output.
        """
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

        rich_handler.addFilter(
            ConsoleRoutingFilter(),
        )

        configured_rich_handler = cast(
            Handler,
            rich_handler,
        )

        return configured_rich_handler
