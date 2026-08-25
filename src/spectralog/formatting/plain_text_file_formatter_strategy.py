from __future__ import annotations

import logging

from spectralog.configuration.configuration import LoggerConfiguration
from spectralog.core.protocols import LoggerFormatterFactoryProtocol


class PlainTextFileFormatterStrategy:
    """Select plain-text file formatting when JSON logging is not configured.

    ``PlainTextFileFormatterStrategy`` implements the file formatter strategy used
    for standard plain-text log files.

    The strategy reports support when the active
    :class:`LoggerConfiguration` does not contain a
    :class:`JsonLoggerConfiguration`. When selected, formatter creation is
    delegated to the injected :class:`LoggerFormatterFactoryProtocol`.

    This strategy typically acts as the plain-text fallback in
    :class:`FileFormatterResolver` after more specialized strategies, such as JSON
    formatting, have been evaluated."""

    def __init__(
        self,
        formatter_factory: LoggerFormatterFactoryProtocol,
    ) -> None:
        """Initialize the plain-text file formatter strategy.

        Args:
            formatter_factory:
                Factory responsible for creating the standard plain-text
                :class:`logging.Formatter` from a
                :class:`LoggerConfiguration`."""
        self._formatter_factory = formatter_factory

    def supports(
        self,
        configuration: LoggerConfiguration,
    ) -> bool:
        """Return whether the supplied configuration uses plain-text file logging.

        The strategy is applicable when
        ``configuration.json_logger_configuration`` is ``None``. A present JSON
        configuration indicates that JSON file formatting should be selected instead.

        Args:
            configuration:
                Logger configuration to evaluate.

        Returns:
            bool:
                ``True`` when JSON logging is not configured; otherwise ``False``."""
        is_supported = configuration.json_logger_configuration is None

        return is_supported

    def create(
        self,
        configuration: LoggerConfiguration,
    ) -> logging.Formatter:
        """Create the formatter used for plain-text file logging.

        Formatter creation is delegated to
        :meth:`LoggerFormatterFactoryProtocol.create_file_formatter` using the
        supplied :class:`LoggerConfiguration`.

        Args:
            configuration:
                Logger configuration used to construct the plain-text file formatter.

        Returns:
            logging.Formatter:
                The configured formatter returned by the injected formatter factory."""
        formatter = self._formatter_factory.create_file_formatter(
            configuration,
        )

        created_formatter = formatter

        return created_formatter
