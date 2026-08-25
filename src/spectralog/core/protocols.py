from __future__ import annotations

import logging
from pathlib import Path
from typing import Protocol

from spectralog.configuration.configuration import LoggerConfiguration
from spectralog.configuration.json_logger_configuration import (
    JsonLoggerConfiguration,
)
from spectralog.configuration.rich_console_configuration import (
    RichConsoleConfiguration,
)
from spectralog.configuration.syslog_configuration import (
    SyslogConfiguration,
)
from spectralog.core.models import LoggerBuildResult
from spectralog.runtime.multiprocessing_logging_runtime import (
    MultiprocessingLoggingRuntime,
)


class LoggerBuilder(Protocol):
    """Define the interface for objects that build configured application loggers.

    Implementations are responsible for constructing or preparing a named
    :class:`logging.Logger` and returning the resulting logger together with any
    associated file and multiprocessing runtime metadata.

    The protocol allows :class:`ApplicationLogger` to depend on logger-building
    behavior without depending on a concrete builder implementation."""

    def build(
        self,
        name: str,
    ) -> LoggerBuildResult:
        ...


class LoggerFormatterFactoryProtocol(Protocol):
    """Define the interface for creating SpectraLog console and file formatters.

    Implementations produce formatters from a :class:`LoggerConfiguration` while
    encapsulating the concrete formatting strategy used for each output type.

    Console and file formatting are exposed separately because they may require
    different format strings, color handling, or formatter implementations."""

    def create_console_formatter(
        self,
        configuration: LoggerConfiguration,
    ) -> logging.Formatter:
        ...

    def create_file_formatter(
        self,
        configuration: LoggerConfiguration,
    ) -> logging.Formatter:
        ...


class JsonLoggerFormatterFactoryProtocol(Protocol):
    """Define the interface for creating JSON log formatters.

    Implementations create a :class:`logging.Formatter` from a
    :class:`JsonLoggerConfiguration`, allowing JSON formatter construction to be
    used through an abstraction rather than a concrete formatter factory."""

    def create(
        self,
        configuration: JsonLoggerConfiguration,
    ) -> logging.Formatter:
        ...


class FileFormatterStrategyProtocol(Protocol):
    """Define the strategy interface for selecting and creating file formatters.

    A file formatter strategy determines whether it supports a given
    :class:`LoggerConfiguration` and, when selected, creates the corresponding
    :class:`logging.Formatter`.

    This protocol allows file formatting behavior to be resolved through ordered
    strategies such as JSON and plain-text formatting."""

    def supports(
        self,
        configuration: LoggerConfiguration,
    ) -> bool:
        ...

    def create(
        self,
        configuration: LoggerConfiguration,
    ) -> logging.Formatter:
        ...


class FileFormatterResolverProtocol(Protocol):
    """Define the interface for resolving the appropriate file formatter.

    Implementations inspect the supplied :class:`LoggerConfiguration`, select an
    applicable file formatter strategy, and return the resulting
    :class:`logging.Formatter`.

    The resolver hides strategy-selection details from handler factories that only
    need the final formatter."""

    def resolve(
        self,
        configuration: LoggerConfiguration,
    ) -> logging.Formatter:
        ...


class LogFilePathResolverProtocol(Protocol):
    """Define the interface for resolving the effective log file path.

    Implementations derive the final :class:`pathlib.Path` used for persistent
    logging from a :class:`LoggerConfiguration`.

    Path resolution may include directory creation, automatic file naming, custom
    file names, and extension normalization depending on the active logging
    configuration."""

    def resolve(
        self,
        configuration: LoggerConfiguration,
    ) -> Path:
        ...


class ConsoleHandlerFactoryProtocol(Protocol):
    """Define the interface for creating the standard console logging handler.

    Implementations create and configure a :class:`logging.Handler` suitable for
    console output using the supplied :class:`LoggerConfiguration`.

    The returned handler is expected to contain any formatter, level, and filter
    configuration required for standard SpectraLog console logging."""

    def create(
        self,
        configuration: LoggerConfiguration,
    ) -> logging.Handler:
        ...


class RichConsoleHandlerFactoryProtocol(Protocol):
    """Define the interface for creating Rich-based console logging handlers.

    Implementations create a :class:`logging.Handler` using both the general
    :class:`LoggerConfiguration` and the Rich-specific
    :class:`RichConsoleConfiguration`.

    This abstraction allows the logger builder to select Rich console output
    without depending directly on the concrete Rich handler implementation."""

    def create(
        self,
        logger_configuration: LoggerConfiguration,
        rich_configuration: RichConsoleConfiguration,
    ) -> logging.Handler:
        ...


class FileHandlerFactoryProtocol(Protocol):
    """Define the interface for creating persistent file logging handlers.

    Implementations create and configure a :class:`logging.Handler` for the
    resolved log file path using the supplied :class:`LoggerConfiguration`.

    The concrete handler may provide behavior such as file rotation, formatter
    selection, filtering, and encoding while remaining hidden behind this
    protocol."""

    def create(
        self,
        configuration: LoggerConfiguration,
        log_file_path: Path,
    ) -> logging.Handler:
        ...


class MultiprocessingHandlerFactoryProtocol(Protocol):
    """Define the interface for creating multiprocessing-safe logging infrastructure.

    Implementations construct a :class:`MultiprocessingLoggingRuntime` for the
    resolved log file path and active :class:`LoggerConfiguration`.

    The resulting runtime is responsible for coordinating queue-based logging
    components used when SpectraLog's multiprocessing-safe file logging mode is
    enabled."""

    def create(
        self,
        configuration: LoggerConfiguration,
        log_file_path: Path,
    ) -> MultiprocessingLoggingRuntime:
        ...


class SyslogHandlerFactoryProtocol(Protocol):
    """Define the interface for creating syslog logging handlers.

    Implementations create and configure a :class:`logging.Handler` using the
    general :class:`LoggerConfiguration` together with a
    :class:`SyslogConfiguration`.

    This abstraction isolates syslog transport and handler construction from the
    application logger builder."""

    def create(
        self,
        logger_configuration: LoggerConfiguration,
        syslog_configuration: SyslogConfiguration,
    ) -> logging.Handler:
        ...
