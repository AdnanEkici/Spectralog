from __future__ import annotations

import logging

from spectralog.configuration.json_logger_configuration import (
    JsonLoggerConfiguration,
)
from spectralog.formatting.json_formatter import (
    JsonLoggerFormatter,
)


class JsonLoggerFormatterFactory:
    """Create JSON formatters for SpectraLog structured file logging.

    ``JsonLoggerFormatterFactory`` encapsulates construction of
    :class:`JsonLoggerFormatter` instances.

    The factory accepts a :class:`JsonLoggerConfiguration` and returns a formatter
    configured with the requested JSON metadata options. This keeps formatter
    creation separate from file-format strategy selection and allows JSON
    formatting to be consumed through
    :class:`JsonLoggerFormatterFactoryProtocol`.

    The returned formatter is exposed through the standard
    :class:`logging.Formatter` abstraction so that handler and strategy components
    do not need to depend directly on the concrete JSON formatter type."""

    def create(
        self,
        configuration: JsonLoggerConfiguration,
    ) -> logging.Formatter:
        """Create a JSON formatter from the supplied configuration.

        Constructs a :class:`JsonLoggerFormatter` using the provided
        :class:`JsonLoggerConfiguration`. The configuration determines which optional
        metadata fields are included in each structured log record.

        Args:
            configuration:
                JSON logging configuration controlling optional fields such as
                timestamps, logger names, process information, and thread information.

        Returns:
            logging.Formatter:
                A configured :class:`JsonLoggerFormatter` suitable for structured
                JSON file logging."""
        json_logger_formatter = JsonLoggerFormatter(
            configuration=configuration,
        )

        created_formatter = json_logger_formatter

        return created_formatter
