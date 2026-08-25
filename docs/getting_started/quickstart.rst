Quick Start
===========

Create the Application Logger
-----------------------------

SpectraLog should normally be initialized once near the application's entry
point.

.. code-block:: python

   from spectralog import CreateSpectraLogger

   logger = CreateSpectraLogger()

   logger.info("Application started")

By default, SpectraLog:

- logs INFO and higher messages;
- displays log messages in the console;
- includes timestamps;
- writes logs to the ``logs`` directory;
- creates a daily ``.log`` file.

Debug Logging
-------------

Enable DEBUG-level logging with:

.. code-block:: python

   logger = CreateSpectraLogger(
       debug_mode=True,
   )

   logger.debug("Debug information")

Access the Logger from Other Modules
------------------------------------

Initialize SpectraLog once:

.. code-block:: python

   from spectralog import CreateSpectraLogger

   CreateSpectraLogger()

Then retrieve the same application logger elsewhere:

.. code-block:: python

   from spectralog import get_logger

   logger = get_logger()
   logger.info("Processing request")

SpectraLog uses a process-local application logger singleton. Repeated calls to
``get_logger`` return the same logger instance.
