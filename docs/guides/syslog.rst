Syslog Logging
==============

SpectraLog can forward log records to a syslog server in addition to writing
to the console and, when enabled, to local log files.

Syslog support is configured with
:class:`spectralog.SyslogConfiguration`.

Basic Usage
-----------

Create a syslog configuration and pass it to
:func:`spectralog.CreateSpectraLogger`:

.. code-block:: python

   import socket

   from spectralog import CreateSpectraLogger
   from spectralog import SyslogConfiguration

   logger = CreateSpectraLogger(
       syslog_configuration=SyslogConfiguration(
           host="localhost",
           port=514,
           socket_type=socket.SOCK_DGRAM,
       ),
   )

   logger.info("Application started")

Configuration
-------------

``SyslogConfiguration`` supports the following options:

``host``
    Hostname or IP address of the target syslog server.

    Defaults to ``"localhost"``.

``port``
    Network port used by the syslog server.

    Defaults to ``514``.

``facility``
    Syslog facility passed to Python's
    :class:`logging.handlers.SysLogHandler`.

    Defaults to ``SysLogHandler.LOG_USER``.

``socket_type``
    Socket type used for communication with the syslog server.

    Common values are:

    - ``socket.SOCK_DGRAM`` for UDP
    - ``socket.SOCK_STREAM`` for TCP

    Defaults to ``socket.SOCK_DGRAM``.

UDP Example
-----------

UDP is the default transport:

.. code-block:: python

   import socket

   from spectralog import CreateSpectraLogger
   from spectralog import SyslogConfiguration

   logger = CreateSpectraLogger(
       syslog_configuration=SyslogConfiguration(
           host="127.0.0.1",
           port=514,
           socket_type=socket.SOCK_DGRAM,
       ),
   )

   logger.warning("Disk usage is high")

TCP Example
-----------

TCP can be enabled by changing the socket type:

.. code-block:: python

   import socket

   from spectralog import CreateSpectraLogger
   from spectralog import SyslogConfiguration

   logger = CreateSpectraLogger(
       syslog_configuration=SyslogConfiguration(
           host="logs.example.com",
           port=514,
           socket_type=socket.SOCK_STREAM,
       ),
   )

   logger.error("Service failed")

Combined Logging
----------------

Syslog can be used together with console and file logging.

For example:

.. code-block:: python

   import socket

   from spectralog import CreateSpectraLogger
   from spectralog import SyslogConfiguration

   logger = CreateSpectraLogger(
       logs_directory="logs",
       log_file_name="application.log",
       save_logs=True,
       syslog_configuration=SyslogConfiguration(
           host="localhost",
           port=514,
           socket_type=socket.SOCK_DGRAM,
       ),
   )

   logger.info("Application started")

In this configuration, the same log record can be emitted to:

- the console;
- the configured log file;
- the syslog server.

Formatting
----------

Syslog records use SpectraLog's plain-text formatter rather than the colored
console formatter.

This prevents terminal-specific color escape sequences from being transmitted
to the syslog server.

If source-path information is enabled, SpectraLog also applies its relative
path filter to syslog records.

For example:

.. code-block:: python

   logger = CreateSpectraLogger(
       show_folder_name=True,
       show_line=True,
       syslog_configuration=SyslogConfiguration(),
   )

Custom Formats
--------------

A custom file format also affects syslog formatting because SpectraLog uses
the plain-text file formatter for syslog output.

For example:

.. code-block:: python

   logger = CreateSpectraLogger(
       file_format="%(levelname)s | %(message)s",
       syslog_configuration=SyslogConfiguration(),
   )

Custom Log Levels
-----------------

Custom SpectraLog levels can also be sent through syslog.

.. code-block:: python

   logger.add_log_level(
       name="NOTICE",
       color="cyan",
       severity=35,
   )

   logger.notice("Deployment completed")

The configured syslog handler receives the record using the custom numeric
severity registered with SpectraLog.

Network Considerations
----------------------

SpectraLog delegates syslog transport to Python's
:class:`logging.handlers.SysLogHandler`.

The target syslog server must therefore be reachable from the application
environment and configured to accept the selected transport.

For UDP, verify that the server accepts datagrams on the configured port.

For TCP, verify that the server is listening for stream connections on the
configured port.

Firewalls, container networking, host networking rules, and remote syslog
server configuration may affect delivery.

Example Configuration
---------------------

A more complete configuration may look like:

.. code-block:: python

   import socket

   from spectralog import CreateSpectraLogger
   from spectralog import SyslogConfiguration

   logger = CreateSpectraLogger(
       debug_mode=True,
       show_datetime=True,
       show_folder_name=True,
       show_line=True,
       logs_directory="logs",
       log_file_name="application.log",
       save_logs=True,
       syslog_configuration=SyslogConfiguration(
           host="192.168.1.50",
           port=514,
           socket_type=socket.SOCK_DGRAM,
       ),
   )

   logger.info("Service initialized")

See Also
--------

See :class:`spectralog.SyslogConfiguration` for the complete configuration API.

See :func:`spectralog.CreateSpectraLogger` for the main logger creation API.
