from __future__ import annotations

import logging

from spectralog.configuration.configuration import LoggerConfiguration
from spectralog.core.protocols import (
    JsonLoggerFormatterFactoryProtocol,
)


class JsonFileFormatterStrategy:
    """Select JSON file formatting when JSON logging is configured.

    ``JsonFileFormatterStrategy`` implements the file formatter strategy used for
    structured JSON logging.

    The strategy reports support only when the active
    :class:`LoggerConfiguration` contains a
    :class:`JsonLoggerConfiguration`. When selected, formatter creation is
    delegated to the injected :class:`JsonLoggerFormatterFactoryProtocol`.

    This keeps JSON formatter selection separate from formatter construction and
    allows :class:`FileFormatterResolver` to choose JSON formatting through the
    same strategy interface used by other file formats."""

    def __init__(
        self,
        json_formatter_factory: JsonLoggerFormatterFactoryProtocol,
    ) -> None:
        """Initialize the JSON file formatter strategy.

        Args:
            json_formatter_factory:
                Factory responsible for creating the JSON
                :class:`logging.Formatter` from a
                :class:`JsonLoggerConfiguration`."""
        self._json_formatter_factory = json_formatter_factory

    def supports(
        self,
        configuration: LoggerConfiguration,
    ) -> bool:
        """Return whether the supplied configuration enables JSON file logging.

        The strategy is considered applicable when
        ``configuration.json_logger_configuration`` is not ``None``.

        Args:
            configuration:
                Logger configuration to evaluate.

        Returns:
            bool:
                ``True`` when JSON logger configuration is present; otherwise
                ``False``."""
        is_supported = configuration.json_logger_configuration is not None

        return is_supported

    def create(
        self,
        configuration: LoggerConfiguration,
    ) -> logging.Formatter:
        """Create the formatter used for JSON file logging.

        The JSON-specific configuration is extracted from the supplied
        :class:`LoggerConfiguration` and passed to the configured JSON formatter
        factory.

        This method expects the strategy to have already been selected through
        :meth:`supports`. A missing JSON configuration therefore represents invalid
        strategy usage and results in an exception.

        Args:
            configuration:
                Logger configuration containing the required
                :class:`JsonLoggerConfiguration`.

        Raises:
            ValueError:
                If ``configuration.json_logger_configuration`` is ``None``.

        Returns:
            logging.Formatter:
                The JSON formatter created by the configured JSON formatter factory."""
        json_logger_configuration = configuration.json_logger_configuration

        if json_logger_configuration is None:
            raise ValueError(
                "JSON logger configuration is required " "for JSON file formatting.",
            )

        formatter = self._json_formatter_factory.create(
            configuration=json_logger_configuration,
        )

        created_formatter = formatter

        return created_formatter
