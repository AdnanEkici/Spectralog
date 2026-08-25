JSON Logging
============

SpectraLog can write structured JSON Lines log files.

Enable JSON Logging
-------------------

.. code-block:: python

   from spectralog import CreateSpectraLogger
   from spectralog import JsonLoggerConfiguration

   logger = CreateSpectraLogger(
       log_file_name="application.log",
       json_logger_configuration=JsonLoggerConfiguration(),
   )

When JSON logging is enabled, the resulting file uses the ``.jsonl``
extension.

Example Record
--------------

A record may resemble:

.. code-block:: json

   {
     "level": "INFO",
     "message": "Application started",
     "timestamp": "2026-08-25T12:30:00+00:00",
     "logger": "ApplicationLogger",
     "process_id": 12345,
     "process_name": "MainProcess",
     "thread_id": 123456789,
     "thread_name": "MainThread"
   }

Optional Metadata
-----------------

Metadata fields can be disabled individually:

.. code-block:: python

   json_configuration = JsonLoggerConfiguration(
       include_timestamp=True,
       include_logger_name=False,
       include_process_information=False,
       include_thread_information=False,
   )

Level and message fields are always included.
