from __future__ import annotations

import socket
from dataclasses import dataclass
from logging.handlers import SysLogHandler


@dataclass(frozen=True, slots=True)
class SyslogConfiguration:
    """Configure SpectraLog's syslog handler.

    This immutable configuration object defines the network destination and
    transport settings used when SpectraLog forwards log records to a syslog
    server.

    Providing an instance of this configuration when creating a SpectraLog logger
    enables syslog output in addition to any configured console and file handlers.

    Instances are frozen and use slots, preventing configuration values from being
    modified after construction or arbitrary attributes from being added
    dynamically.

    Attributes:
        host:
            Hostname or IP address of the target syslog server. Defaults to
            ``"localhost"``.

        port:
            Network port used by the syslog server. The conventional syslog port
            is ``514``. Defaults to ``514``.

        facility:
            Syslog facility value passed to
            :class:`logging.handlers.SysLogHandler`. Defaults to
            :data:`logging.handlers.SysLogHandler.LOG_USER`.

        socket_type:
            Socket type used to communicate with the syslog server. Common values
            are :data:`socket.SOCK_DGRAM` for UDP and
            :data:`socket.SOCK_STREAM` for TCP. Defaults to
            :data:`socket.SOCK_DGRAM`.

    Example:
        Configure UDP syslog forwarding to a remote server::

            import socket

            from spectralog import SyslogConfiguration

            syslog_configuration = SyslogConfiguration(
                host="192.168.1.50",
                port=514,
                socket_type=socket.SOCK_DGRAM,
            )

        Configure TCP syslog forwarding::

            import socket

            from spectralog import SyslogConfiguration

            syslog_configuration = SyslogConfiguration(
                host="logs.example.com",
                port=514,
                socket_type=socket.SOCK_STREAM,
            )
    """

    host: str = "localhost"
    port: int = 514
    facility: int = SysLogHandler.LOG_USER
    socket_type: socket.SocketKind = socket.SOCK_DGRAM
