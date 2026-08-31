"""Demonstrate ordinary file logging from multiple independent processes.

Without SpectraLog's multiprocessing-safe mode, each process manages its own
logging infrastructure independently.

This example deliberately gives every worker a separate log file. Doing so
avoids concurrent writes to the same file and demonstrates that process-local
SpectraLog instances can operate independently without multiprocessing-safe
coordination.

Three worker processes are started, producing three separate log files.
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
    """Initialize an independent logger and write to a worker-specific file."""
    logger: ApplicationLogger = CreateSpectraLogger(
        debug_mode=True,
        multiprocessing_safe=False,
        log_file_name=f"worker-{worker_number}-example.log",
    )

    logger.info(
        "Worker %d executed",
        worker_number,
    )

    logger.shutdown()


def main() -> None:
    """Start three processes that each write to an independent log file."""
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