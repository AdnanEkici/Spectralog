Internal API
============

This section documents SpectraLog's internal implementation components.

These classes support logger construction, formatting, handler creation,
log-level management, file-path resolution, and multiprocessing runtime
management.

They are primarily intended for contributors and advanced users. They should
not be considered part of the stable public API unless explicitly documented
elsewhere.

Application Logger
------------------

.. autoclass:: spectralog.core.logger.ApplicationLogger
   :members:
   :show-inheritance:

Logger Construction
-------------------

.. autoclass:: spectralog.core.builder.ApplicationLoggerBuilder
   :members:

.. autoclass:: spectralog.core.factory.ApplicationLoggerBuilderFactory
   :members:

Models
------

.. autoclass:: spectralog.core.models.LoggerBuildResult
   :members:

Formatting
----------

.. autoclass:: spectralog.formatting.format_builder.LogFormatBuilder
   :members:

.. autoclass:: spectralog.formatting.formatter_factory.LoggerFormatterFactory
   :members:

.. autoclass:: spectralog.formatting.file_formatter_resolver.FileFormatterResolver
   :members:

.. autoclass:: spectralog.formatting.json_file_formatter_strategy.JsonFileFormatterStrategy
   :members:

.. autoclass:: spectralog.formatting.plain_text_file_formatter_strategy.PlainTextFileFormatterStrategy
   :members:

.. autoclass:: spectralog.formatting.json_formatter.JsonLoggerFormatter
   :members:

.. autoclass:: spectralog.formatting.json_logger_formatter_factory.JsonLoggerFormatterFactory
   :members:

.. autoclass:: spectralog.formatting.relative_path_filter.RelativePathFilter
   :members:

Handlers
--------

.. autoclass:: spectralog.handlers.console_handler_factory.ConsoleHandlerFactory
   :members:

.. autoclass:: spectralog.handlers.file_handler_factory.FileHandlerFactory
   :members:

.. autoclass:: spectralog.handlers.rich_console_handler_factory.RichConsoleHandlerFactory
   :members:

.. autoclass:: spectralog.handlers.syslog_handler_factory.SyslogHandlerFactory
   :members:

.. autoclass:: spectralog.handlers.queue_file_handler_factory.QueueFileHandlerFactory
   :members:

.. autoclass:: spectralog.handlers.multiprocessing_handler_factory.MultiprocessingHandlerFactory
   :members:

File Resolution
---------------

.. autoclass:: spectralog.files.log_file_path_resolver.LogFilePathResolver
   :members:

Log Levels
----------

.. autoclass:: spectralog.levels.log_level.LogLevel
   :members:

.. autoclass:: spectralog.levels.log_level_registry.LogLevelRegistry
   :members:

Multiprocessing Runtime
-----------------------

.. autoclass:: spectralog.runtime.multiprocessing_logging_runtime.MultiprocessingLoggingRuntime
   :members:

Protocols
---------

The following protocols define internal dependency boundaries used throughout
SpectraLog.

.. autoclass:: spectralog.core.protocols.LoggerBuilder
   :members:

.. autoclass:: spectralog.core.protocols.LoggerFormatterFactoryProtocol
   :members:

.. autoclass:: spectralog.core.protocols.JsonLoggerFormatterFactoryProtocol
   :members:

.. autoclass:: spectralog.core.protocols.FileFormatterStrategyProtocol
   :members:

.. autoclass:: spectralog.core.protocols.FileFormatterResolverProtocol
   :members:

.. autoclass:: spectralog.core.protocols.LogFilePathResolverProtocol
   :members:

.. autoclass:: spectralog.core.protocols.ConsoleHandlerFactoryProtocol
   :members:

.. autoclass:: spectralog.core.protocols.RichConsoleHandlerFactoryProtocol
   :members:

.. autoclass:: spectralog.core.protocols.FileHandlerFactoryProtocol
   :members:

.. autoclass:: spectralog.core.protocols.MultiprocessingHandlerFactoryProtocol
   :members:

.. autoclass:: spectralog.core.protocols.SyslogHandlerFactoryProtocol
   :members:
