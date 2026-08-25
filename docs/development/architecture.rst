Architecture
============

Overview
--------

SpectraLog is designed around a small public API and a set of internal
components with clearly separated responsibilities.

The main construction flow is:

.. code-block:: text

   CreateSpectraLogger
          |
          v
   LoggerConfiguration
          |
          v
   ApplicationLoggerBuilderFactory
          |
          v
   ApplicationLoggerBuilder
          |
          +--> Console Handler
          |
          +--> File Handler
          |
          +--> Multiprocessing Runtime
          |
          +--> Syslog Handler
          |
          v
   ApplicationLogger

Public API
----------

Applications normally interact with SpectraLog through:

- ``CreateSpectraLogger``
- ``get_logger``
- ``disable_application_logging``

The public API intentionally hides most formatter, handler, and runtime
construction details.

Application Logger
------------------

``ApplicationLogger`` is the process-local logging facade.

It is responsible for:

- exposing standard logging methods;
- supporting dynamically registered custom log levels;
- managing the process-local singleton;
- starting the optional multiprocessing runtime;
- shutting down logging resources;
- forwarding log calls to the underlying standard-library logger.

Logger Configuration
--------------------

``LoggerConfiguration`` contains the complete configuration used to build the
logger.

It defines behavior such as:

- effective logging level;
- console formatting;
- file formatting;
- log directory and file name;
- log rotation;
- JSON logging;
- Rich console output;
- syslog output;
- multiprocessing-safe file logging.

Builder Factory
---------------

``ApplicationLoggerBuilderFactory`` composes the concrete dependencies required
to build an application logger.

It creates and connects:

- format builders;
- formatter factories;
- formatter strategies;
- handler factories;
- relative-path filtering;
- file-path resolution;
- multiprocessing logging infrastructure;
- syslog infrastructure.

This keeps object construction centralized rather than spreading dependency
creation throughout the package.

Application Logger Builder
--------------------------

``ApplicationLoggerBuilder`` orchestrates construction of the underlying
``logging.Logger``.

Its responsibilities include:

- retrieving the named logger;
- removing and closing existing handlers;
- setting the configured logging level;
- selecting the standard or Rich console handler;
- configuring file logging;
- configuring multiprocessing logging;
- configuring syslog logging;
- disabling logger propagation;
- returning the completed ``LoggerBuildResult``.

Formatting
----------

Formatting responsibilities are separated from handler creation.

``LogFormatBuilder``
    Builds plain-text console and file format strings.

``LoggerFormatterFactory``
    Creates standard colored console and plain-text file formatters.

``JsonLoggerFormatter``
    Serializes log records into structured JSON.

``JsonLoggerFormatterFactory``
    Creates JSON formatter instances.

``FileFormatterResolver``
    Chooses the appropriate file formatter strategy.

``JsonFileFormatterStrategy``
    Selects JSON formatting when JSON logging is configured.

``PlainTextFileFormatterStrategy``
    Selects plain-text formatting when JSON logging is not configured.

File Formatter Strategy
-----------------------

File formatting uses a strategy-based design.

The resolution flow is:

.. code-block:: text

   LoggerConfiguration
          |
          v
   FileFormatterResolver
          |
          +--> JsonFileFormatterStrategy
          |
          +--> PlainTextFileFormatterStrategy
          |
          v
   logging.Formatter

Strategies are evaluated in order.

JSON formatting is evaluated before plain-text formatting so that JSON
configuration takes precedence when enabled.

Handlers
--------

SpectraLog uses dedicated factories for each logging destination.

``ConsoleHandlerFactory``
    Creates the standard color-aware console handler.

``RichConsoleHandlerFactory``
    Creates the Rich-based console handler.

``FileHandlerFactory``
    Creates rotating persistent file handlers.

``QueueFileHandlerFactory``
    Creates queue handlers for multiprocessing file logging.

``MultiprocessingHandlerFactory``
    Assembles the multiprocessing queue, queue handler, file handler, listener,
    and runtime.

``SyslogHandlerFactory``
    Creates network syslog handlers.

Relative Path Filtering
-----------------------

``RelativePathFilter`` enriches log records with a ``relative_path`` attribute.

When a log record originates inside the configured project root, the absolute
source path is converted to a relative path.

When the source file lies outside the project root, the file name is used as a
fallback.

The filter always allows the record to continue through the logging pipeline.

Log File Resolution
-------------------

``LogFilePathResolver`` determines the final persistent log file path.

It supports:

- custom log file names;
- automatically generated daily file names;
- plain-text ``.log`` files;
- JSON Lines ``.jsonl`` files;
- automatic creation of the configured logs directory.

Log Levels
----------

``LogLevelRegistry`` owns SpectraLog's log-level definitions.

The registry contains the standard levels:

- DEBUG
- INFO
- WARNING
- ERROR
- CRITICAL

Custom levels can also be registered dynamically.

Each level is represented by a ``LogLevel`` containing:

- name;
- severity;
- color.

The registry validates custom names, severities, and color values before
registration.

Multiprocessing Logging
-----------------------

When ``multiprocessing_safe=True`` is enabled, file logging uses a queue-based
pipeline.

The flow is:

.. code-block:: text

   ApplicationLogger
          |
          v
      QueueHandler
          |
          v
   Multiprocessing Queue
          |
          v
      QueueListener
          |
          v
   RotatingFileHandler

``MultiprocessingLoggingRuntime`` owns the lifecycle of this pipeline.

It starts the queue listener when the application logger is initialized and
stops it during logger shutdown.

The runtime also closes the queue handler and multiprocessing queue and joins
the queue feeder thread during cleanup.

Singleton Lifecycle
-------------------

``ApplicationLogger`` is a process-local singleton.

The intended application flow is:

.. code-block:: python

   from spectralog import CreateSpectraLogger

   logger = CreateSpectraLogger()

and then, from other modules:

.. code-block:: python

   from spectralog import get_logger

   logger = get_logger()

Once the application logger has been explicitly initialized, attempts to
reconfigure it are rejected.

Different Python processes have independent singleton instances because each
process has its own memory space.

Testing Support
---------------

``disable_application_logging`` allows application code to continue using the
normal SpectraLog API during tests without creating logging side effects.

The decorator disables the logger build infrastructure for the decorated
``unittest.TestCase`` class and isolates the ``ApplicationLogger`` singleton
for each test method.

This allows tests to execute code that calls ``CreateSpectraLogger`` and
``get_logger`` without creating log files, Rich handlers, syslog handlers, or
multiprocessing logging infrastructure.

Dependency Boundaries
---------------------

SpectraLog uses protocols to define internal dependency contracts.

Examples include:

- ``LoggerBuilder``
- ``LoggerFormatterFactoryProtocol``
- ``FileFormatterStrategyProtocol``
- ``FileFormatterResolverProtocol``
- ``ConsoleHandlerFactoryProtocol``
- ``FileHandlerFactoryProtocol``
- ``MultiprocessingHandlerFactoryProtocol``
- ``SyslogHandlerFactoryProtocol``

This allows higher-level components to depend on behavior rather than concrete
implementations.

Design Goals
------------

The architecture is intended to preserve the following properties:

- small public API;
- clear separation of responsibilities;
- testable components;
- explicit dependency composition;
- interchangeable formatter strategies;
- isolated handler construction;
- predictable singleton lifecycle;
- deterministic logging shutdown;
- compatibility with Python's standard logging system.

See Also
--------

See :doc:`../api/internals` for the generated internal API reference.

See :doc:`../api/public_api` for the public API reference.
