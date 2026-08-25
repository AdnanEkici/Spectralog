from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

from spectralog.runtime.multiprocessing_logging_runtime import (
    MultiprocessingLoggingRuntime,
)


@dataclass(frozen=True, slots=True)
class LoggerBuildResult:
    """Describe the result of building a configured SpectraLog logger.

    ``LoggerBuildResult`` groups the objects and metadata produced by
    :class:`ApplicationLoggerBuilder` after logger construction has completed.

    The result allows :class:`ApplicationLogger` to receive the configured
    standard-library logger together with file-related state and the optional
    multiprocessing logging runtime without requiring the builder to expose its
    internal construction details.

    Instances are immutable and use slots so that build metadata cannot be changed
    after creation and arbitrary attributes cannot be added dynamically.

    Attributes:
        logger:
            The fully configured :class:`logging.Logger` created or prepared by
            the application logger builder.

        log_file_path:
            Resolved path of the active log file when persistent file logging is
            enabled. ``None`` when file logging is disabled.

        is_new_log_file:
            Indicates whether the resolved log file was newly created or was empty
            when the logger was built. This value is used by
            :class:`ApplicationLogger` to determine whether a new-log-file warning
            should be emitted.

        multiprocessing_logging_runtime:
            Multiprocessing logging runtime associated with the logger when
            multiprocessing-safe file logging is enabled. ``None`` when logging
            records are written directly without the multiprocessing queue and
            listener infrastructure.
    """

    logger: logging.Logger
    log_file_path: Path | None
    is_new_log_file: bool
    multiprocessing_logging_runtime: MultiprocessingLoggingRuntime | None
