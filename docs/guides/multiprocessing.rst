Multiprocessing-Safe File Logging
=================================

SpectraLog supports queue-based file logging through
``multiprocessing_safe=True``.

.. code-block:: python

   logger = CreateSpectraLogger(
       multiprocessing_safe=True,
   )

Architecture
------------

In this mode, records flow through:

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

The application logger does not write directly to the file handler.

Runtime Lifecycle
-----------------

The multiprocessing logging runtime is started automatically when the
application logger is created.

It is stopped during ``ApplicationLogger.shutdown`` and also registered for
normal interpreter shutdown.

Independent Processes
---------------------

The multiprocessing runtime belongs to the logger instance that created it.

Independently initialized Python processes do not automatically share the same
queue or queue listener. Applications that initialize SpectraLog separately in
multiple processes should use separate log files unless they explicitly
coordinate logging through shared infrastructure.
