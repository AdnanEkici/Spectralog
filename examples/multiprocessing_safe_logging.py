"""Demonstrate multiprocessing-safe logging with SpectraLog.

Concurrent processes can write log records at the same time, which can make
direct file logging unsafe or inconsistent.

SpectraLog's multiprocessing-safe mode provides coordinated logging
infrastructure intended for applications that emit records from multiple
processes.
"""

from __future__ import annotations

import sys
from multiprocessing import Process
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIRECTORY = PROJECT_ROOT / "src"

sys.path.insert(
    0,
    str(SOURCE_DIRECTORY),
)

from spectralog import CreateSpectraLogger  # noqa: E402
from spectralog.core.logger import ApplicationLogger  # noqa: E402


def worker(
    worker_number: int,
) -> None:
    """Initialize logging and emit a message from a worker process."""
    logger: ApplicationLogger = CreateSpectraLogger(
        debug_mode=True,
        multiprocessing_safe=True,
        log_file_name="multiprocess-safe-example.log",
        
    )

    logger.info(
        "Worker %d executed",
        worker_number,
    )

    logger.shutdown()


def main() -> None:
    """Start several worker processes that use multiprocessing-safe logging."""
    processes = [
        Process(
            target=worker,
            args=(
                worker_number,
            ),
        )
        for worker_number in range(
            3,
        )
    ]

    for process in processes:
        process.start()

    for process in processes:
        process.join()


if __name__ == "__main__":
    main()