from __future__ import annotations

import logging

from spectralog.configuration.configuration import (
    LoggerConfiguration,
)
from spectralog.core.log_routing import (
    ConsoleRoutingFilter,
)
from spectralog.formatting.formatter_factory import (
    LoggerFormatterFactory,
)
from spectralog.formatting.relative_path_filter import (
    RelativePathFilter,
)


class ConsoleHandlerFactory:
    """Create the standard SpectraLog console logging handler.

    ``ConsoleHandlerFactory`` constructs and configures the standard
    :class:`logging.StreamHandler` used for console output when Rich console
    logging is not enabled.

    Formatter creation is delegated to :class:`LoggerFormatterFactory`, while
    source-path enrichment is provided through a shared
    :class:`RelativePathFilter`.

    The created handler uses the effective logging level from
    :class:`LoggerConfiguration`, applies the configured color-aware console
    formatter, enriches records with relative source-path information, and
    applies per-record console destination routing.

    A :class:`ConsoleRoutingFilter` is attached so callers can suppress console
    output for an individual record by passing ``console=False`` to SpectraLog
    logging methods.

    This factory is responsible only for constructing and configuring the
    console handler. Attaching the handler to the application logger is handled
    by :class:`ApplicationLoggerBuilder`.
    """

    def __init__(
        self,
        formatter_factory: LoggerFormatterFactory,
        relative_path_filter: RelativePathFilter,
    ) -> None:
        """Initialize the console handler factory with its dependencies.

        Args:
            formatter_factory:
                Formatter factory responsible for creating the console formatter
                from the active :class:`LoggerConfiguration`.

            relative_path_filter:
                Filter that enriches log records with the ``relative_path``
                attribute used by SpectraLog source-path formatting.
        """
        self._formatter_factory = formatter_factory
        self._relative_path_filter = relative_path_filter

    def create(
        self,
        configuration: LoggerConfiguration,
    ) -> logging.Handler:
        """Create and configure the standard console logging handler.

        A console formatter is first created from the supplied
        :class:`LoggerConfiguration`. A :class:`logging.StreamHandler` is then
        constructed and configured with the effective logging level, generated
        formatter, source-path enrichment, and console destination routing.

        Two filters are attached before the handler is returned:

        - :class:`RelativePathFilter` enriches records with the ``relative_path``
          attribute required by SpectraLog's source-path formatting.
        - :class:`ConsoleRoutingFilter` determines whether a record is eligible
          for standard console output.

        Records emitted through SpectraLog with ``console=False`` are rejected
        by :class:`ConsoleRoutingFilter` and therefore do not appear on the
        standard console handler.

        Records emitted with ``console=True`` remain eligible for console output.

        Records created outside SpectraLog that do not contain destination
        routing metadata default to console output, preserving compatibility with
        ordinary :mod:`logging` records.

        Args:
            configuration:
                Logger configuration controlling the effective logging level and
                console formatting behavior.

        Returns:
            logging.Handler:
                A configured :class:`logging.StreamHandler` with formatting,
                relative-path enrichment, and per-record console routing enabled.

        Example:
            A record emitted as::

                logger.info(
                    "File-only message",
                    console=False,
                    file=True,
                )

            reaches the console handler but is rejected by
            :class:`ConsoleRoutingFilter` before being written to the console.
        """
        formatter = self._formatter_factory.create_console_formatter(
            configuration,
        )

        console_handler = logging.StreamHandler()

        console_handler.setLevel(
            configuration.log_level,
        )

        console_handler.setFormatter(
            formatter,
        )

        console_handler.addFilter(
            self._relative_path_filter,
        )

        console_handler.addFilter(
            ConsoleRoutingFilter(),
        )

        configured_console_handler = console_handler

        return configured_console_handler
