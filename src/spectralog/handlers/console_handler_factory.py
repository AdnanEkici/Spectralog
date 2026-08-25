from __future__ import annotations

import logging

from spectralog.configuration.configuration import (
    LoggerConfiguration,
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
    formatter, and attaches the relative-path filter before being returned.

    This factory is responsible only for constructing and configuring the console
    handler. Attaching the handler to the application logger is handled by
    :class:`ApplicationLoggerBuilder`."""

    def __init__(
        self,
        formatter_factory: LoggerFormatterFactory,
        relative_path_filter: RelativePathFilter,
    ) -> None:
        """Initialize the console handler factory with its dependencies.

        Args:
            formatter_factory:
                Formatter factory responsible for creating the console formatter from
                the active :class:`LoggerConfiguration`.

            relative_path_filter:
                Filter that enriches log records with the ``relative_path`` attribute
                used by SpectraLog source-path formatting."""
        self._formatter_factory = formatter_factory
        self._relative_path_filter = relative_path_filter

    def create(
        self,
        configuration: LoggerConfiguration,
    ) -> logging.Handler:
        """Create and configure the standard console logging handler.

        A console formatter is first created from the supplied
        :class:`LoggerConfiguration`. A :class:`logging.StreamHandler` is then
        constructed and configured with the effective logger level, the generated
        formatter, and the shared :class:`RelativePathFilter`.

        The returned handler is ready to be attached to a
        :class:`logging.Logger`.

        Args:
            configuration:
                Logger configuration controlling the effective logging level and
                console formatting behavior.

        Returns:
            logging.Handler:
                A configured :class:`logging.StreamHandler` suitable for standard
                SpectraLog console output."""
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

        configured_console_handler = console_handler
        return configured_console_handler
