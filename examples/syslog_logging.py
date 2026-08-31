"""Demonstrate forwarding SpectraLog records to a Syslog endpoint.

Syslog integration is useful when applications send logs to centralized system
logging infrastructure instead of relying only on local console or file output.

This example assumes a Syslog receiver is available on localhost using port 514.

For local testing without a dedicated Syslog server, you can temporarily change
the configured port to a non-privileged port such as ``5514`` and start a simple
UDP listener in another terminal.

For example::

    nc -u -l 5514

Then configure the example with::

    syslog_configuration = SyslogConfiguration(
        host="127.0.0.1",
        port=5514,
    )

Run this example in a second terminal. The emitted SpectraLog records should
appear in the terminal running the UDP listener.

Port ``514`` is commonly used for Syslog and may require elevated privileges on
some systems, which is why a higher port such as ``5514`` is more convenient for
local development and demonstration.

Common compatible destinations include:

- Splunk
- Elastic / Elasticsearch
- Graylog
- Grafana Loki, through a Syslog-capable collector such as Grafana Alloy
- Datadog, through the Datadog Agent
- New Relic, through a compatible log forwarder
- Fluent Bit
- Fluentd
- Vector
- rsyslog
- syslog-ng
- systemd / journald environments using an appropriate Syslog receiver
- SIEM platforms that expose Syslog ingestion
- Network appliances and centralized enterprise Syslog servers

SpectraLog
    |
    | Syslog UDP/TCP
    v
Collector / Agent / Syslog Server
    |
    v
Elastic / Splunk / Datadog / Loki / SIEM / other platform

"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIRECTORY = PROJECT_ROOT / "src"

sys.path.insert(
    0,
    str(SOURCE_DIRECTORY),
)

from spectralog import CreateSpectraLogger  # noqa: E402
from spectralog import SyslogConfiguration  # noqa: E402
from spectralog.core.logger import ApplicationLogger  # noqa: E402


def main() -> None:
    """Configure SpectraLog to forward records to a Syslog receiver."""
    syslog_configuration = SyslogConfiguration(
        host="localhost",
        port=514,
    )

    logger: ApplicationLogger = CreateSpectraLogger(
        debug_mode=True,
        syslog_configuration=syslog_configuration,
        log_file_name="syslog-example.log",
    )

    logger.info(
        "Hello from SpectraLog Syslog",
    )

    logger.warning(
        "Syslog warning example",
    )

    logger.error(
        "Syslog error example",
    )


if __name__ == "__main__":
    main()