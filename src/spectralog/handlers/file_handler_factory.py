from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from spectralog.configuration.configuration import LoggerConfiguration
from spectralog.core.log_routing import FileRoutingFilter
from spectralog.core.protocols import FileFormatterResolverProtocol
from spectralog.formatting.relative_path_filter import RelativePathFilter


class FileHandlerFactory:
    """Create rotating file handlers for SpectraLog persistent logging.

    ``FileHandlerFactory`` constructs and configures the
    :class:`logging.handlers.RotatingFileHandler` used for persistent SpectraLog
    output.

    Formatter selection is delegated to the configured
    :class:`FileFormatterResolverProtocol`, allowing the handler to support
    multiple file formats such as plain text and JSON without depending directly
    on a concrete formatter implementation.

    The created handler uses UTF-8 encoding, applies the effective logging level
    from :class:`LoggerConfiguration`, and configures file rotation through the
    ``max_bytes`` and ``backup_count`` settings.

    A shared :class:`RelativePathFilter` is attached to enrich log records with
    SpectraLog's ``relative_path`` source metadata.

    A :class:`FileRoutingFilter` is also attached so individual log records can
    opt out of persistent file output by using ``file=False`` on SpectraLog
    logging methods.

    This factory is responsible only for constructing and configuring the file
    handler. Attaching the handler to a logger, or placing it behind a
    multiprocessing queue, is handled by higher-level SpectraLog components.
    """

    def __init__(
        self,
        file_formatter_resolver: FileFormatterResolverProtocol,
        relative_path_filter: RelativePathFilter,
    ) -> None:
        """Initialize the file handler factory with its dependencies.

        Args:
            file_formatter_resolver:
                Resolver responsible for selecting and creating the appropriate
                file formatter for the active
                :class:`LoggerConfiguration`.

            relative_path_filter:
                Filter that enriches log records with the ``relative_path``
                attribute used by SpectraLog source-path formatting.
        """
        self._file_formatter_resolver = file_formatter_resolver
        self._relative_path_filter = relative_path_filter

    def create(
        self,
        configuration: LoggerConfiguration,
        log_file_path: Path,
    ) -> logging.Handler:
        """Create and configure a rotating file logging handler.

        The appropriate file formatter is first resolved from the supplied
        :class:`LoggerConfiguration`. A
        :class:`logging.handlers.RotatingFileHandler` is then created for
        ``log_file_path`` using UTF-8 encoding.

        The handler's rotation policy is configured from ``max_bytes`` and
        ``backup_count``. Its logging threshold is set to the effective
        configuration level and the resolved formatter is attached.

        Two filters are installed before the handler is returned:

        - :class:`RelativePathFilter` enriches records with SpectraLog source-path
          metadata.
        - :class:`FileRoutingFilter` determines whether the record is eligible
          for file output.

        Records emitted through SpectraLog with ``file=False`` are rejected by
        the routing filter and are therefore not written to the log file. Records
        emitted with ``file=True`` remain eligible for file output.

        Records that do not contain SpectraLog routing metadata default to file
        output, preserving compatibility with ordinary
        :mod:`logging` records.

        Args:
            configuration:
                Logger configuration controlling the effective logging level,
                formatter selection, maximum file size, and retained backup
                count.

            log_file_path:
                Resolved path of the log file to which accepted records should
                be written.

        Returns:
            logging.Handler:
                A configured
                :class:`logging.handlers.RotatingFileHandler` with formatting,
                path enrichment, rotation, and per-record file routing enabled.

        Example:
            A record emitted as::

                logger.info(
                    "Console-only message",
                    console=True,
                    file=False,
                )

            reaches the file handler but is rejected by
            :class:`FileRoutingFilter` before it is written.
        """
        formatter = self._file_formatter_resolver.resolve(
            configuration,
        )

        file_handler = RotatingFileHandler(
            filename=log_file_path,
            maxBytes=configuration.max_bytes,
            backupCount=configuration.backup_count,
            encoding="utf-8",
        )

        file_handler.setLevel(
            configuration.log_level,
        )

        file_handler.setFormatter(
            formatter,
        )

        file_handler.addFilter(
            self._relative_path_filter,
        )

        file_handler.addFilter(
            FileRoutingFilter(),
        )

        configured_file_handler = file_handler

        return configured_file_handler
