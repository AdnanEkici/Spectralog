from __future__ import annotations

from logging import LogRecord
from logging.handlers import QueueHandler
from multiprocessing.queues import Queue


class QueueFileHandlerFactory:
    """Create queue handlers for SpectraLog multiprocessing file logging.

    ``QueueFileHandlerFactory`` constructs the
    :class:`logging.handlers.QueueHandler` used by SpectraLog's
    multiprocessing-safe logging pipeline.

    The queue handler does not write log records to a file directly. Instead, it
    places eligible records onto the supplied multiprocessing queue so that a
    separate :class:`logging.handlers.QueueListener` can forward them to the
    configured file handler.

    This separation allows application logging calls to avoid performing the file
    write directly while preserving the downstream file handler's formatting,
    rotation, and filtering behavior.

    The factory configures the queue handler with the supplied logging threshold
    before returning it."""

    def create(
        self,
        log_record_queue: Queue[LogRecord],
        log_level: int,
    ) -> QueueHandler:
        """Create and configure a queue handler for log-record transport.

        Constructs a :class:`logging.handlers.QueueHandler` backed by the supplied
        multiprocessing queue and configures it with the requested logging level.

        Records accepted by this handler are placed onto ``log_record_queue`` for
        later processing by SpectraLog's queue listener and downstream file handler.

        Args:
            log_record_queue:
                Multiprocessing queue used to transport log records from the
                application logger to the queue listener.

            log_level:
                Minimum integer logging severity accepted by the queue handler.

        Returns:
            QueueHandler:
                A configured :class:`logging.handlers.QueueHandler` ready to be
                attached to the application logger."""
        queue_handler = QueueHandler(
            log_record_queue,
        )

        queue_handler.setLevel(
            log_level,
        )

        configured_queue_handler = queue_handler

        return configured_queue_handler
