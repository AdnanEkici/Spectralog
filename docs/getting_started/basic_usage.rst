Basic Usage
===========

Standard Log Levels
-------------------

SpectraLog provides the standard Python logging levels:

.. code-block:: python

   logger.debug("Debug message")
   logger.info("Informational message")
   logger.warning("Warning message")
   logger.error("Error message")
   logger.critical("Critical message")

Exception Logging
-----------------

Use ``exception`` inside an exception handler to include traceback
information:

.. code-block:: python

   try:
       result = 10 / 0
   except ZeroDivisionError:
       logger.exception("Calculation failed")

Deferred Message Formatting
---------------------------

SpectraLog supports the standard logging interpolation mechanism:

.. code-block:: python

   user_name = "Ada"

   logger.info(
       "User %s authenticated",
       user_name,
   )

Using deferred interpolation avoids formatting a message before the logging
system determines whether the record will be emitted.

Generic Log Method
------------------

A level can also be supplied explicitly:

.. code-block:: python

   logger.log(
       "WARNING",
       "Disk usage is high",
   )

Numeric severity values are also supported:

.. code-block:: python

   logger.log(
       30,
       "Disk usage is high",
   )
