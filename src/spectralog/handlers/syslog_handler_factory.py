from __future__ import annotations

import logging
from logging.handlers import SysLogHandler

from spectralog.configuration.configuration import LoggerConfiguration
from spectralog.configuration.syslog_configuration import SyslogConfiguration
from spectralog.core.protocols import LoggerFormatterFactoryProtocol
from spectralog.formatting.relative_path_filter import RelativePathFilter


class SyslogHandlerFactory:
    """Create syslog handlers for SpectraLog network logging.

    ``SyslogHandlerFactory`` constructs and configures the
    :class:`logging.handlers.SysLogHandler` used when syslog output is enabled.

    The factory combines SpectraLog's general :class:`LoggerConfiguration` with a
    :class:`SyslogConfiguration`. General logger configuration determines the
    effective logging level and plain-text formatting behavior, while the syslog
    configuration defines the destination host, port, facility, and socket type.

    Syslog records use SpectraLog's standard file formatter rather than the
    color-aware console formatter so that terminal-specific color escape sequences
    are not transmitted to the syslog server.

    A shared :class:`RelativePathFilter` is attached to the handler so that format
    strings containing ``%(relative_path)s`` can be used safely for syslog output.

    This factory is responsible only for constructing and configuring the syslog
    handler. Attaching the handler to the application logger is handled by
    :class:`ApplicationLoggerBuilder`."""

    def __init__(
        self,
        formatter_factory: LoggerFormatterFactoryProtocol,
        relative_path_filter: RelativePathFilter,
    ) -> None:
        """Initialize the syslog handler factory with its dependencies.

        Args:
            formatter_factory:
                Formatter factory used to create the plain-text formatter applied to
                outgoing syslog records.

            relative_path_filter:
                Filter that enriches log records with the ``relative_path`` attribute
                used by SpectraLog source-path formatting."""
        self._formatter_factory = formatter_factory
        self._relative_path_filter = relative_path_filter

    def create(
        self,
        logger_configuration: LoggerConfiguration,
        syslog_configuration: SyslogConfiguration,
    ) -> logging.Handler:
        """Create and configure a syslog logging handler.

        A plain-text formatter is created from ``logger_configuration`` and attached
        to a :class:`logging.handlers.SysLogHandler`.

        The syslog destination address, facility, and socket type are obtained from
        ``syslog_configuration``. The handler's minimum logging level is set from the
        effective SpectraLog logger level, and the shared
        :class:`RelativePathFilter` is attached before the handler is returned.

        The configured socket type determines the transport used by
        :class:`logging.handlers.SysLogHandler`, such as UDP with
        :data:`socket.SOCK_DGRAM` or TCP with :data:`socket.SOCK_STREAM`.

        Args:
            logger_configuration:
                General SpectraLog configuration controlling the effective logging
                level and formatter behavior.

            syslog_configuration:
                Syslog-specific configuration defining the destination host, port,
                facility, and socket type.

        Returns:
            logging.Handler:
                A configured :class:`logging.handlers.SysLogHandler` ready to be
                attached to the application logger."""
        formatter = self._formatter_factory.create_file_formatter(
            logger_configuration,
        )

        syslog_handler = SysLogHandler(
            address=(
                syslog_configuration.host,
                syslog_configuration.port,
            ),
            facility=syslog_configuration.facility,
            socktype=syslog_configuration.socket_type,
        )

        syslog_handler.setLevel(
            logger_configuration.log_level,
        )

        syslog_handler.setFormatter(
            formatter,
        )

        syslog_handler.addFilter(
            self._relative_path_filter,
        )

        configured_syslog_handler = syslog_handler

        return configured_syslog_handler
