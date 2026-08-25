Rich Console Logging
====================

SpectraLog integrates with Rich for enhanced terminal output.

Enable Rich Output
------------------

.. code-block:: python

   from spectralog import CreateSpectraLogger
   from spectralog import RichConsoleConfiguration

   logger = CreateSpectraLogger(
       rich_console_configuration=RichConsoleConfiguration(),
   )

Configuration
-------------

.. code-block:: python

   rich_configuration = RichConsoleConfiguration(
       show_time=True,
       show_level=True,
       show_path=True,
       rich_tracebacks=True,
       markup=False,
   )

Rich Tracebacks
---------------

With ``rich_tracebacks=True``, exceptions logged through ``logger.exception``
use Rich's enhanced traceback rendering.

Markup
------

Rich markup is disabled by default.

Enable it only when log messages intentionally contain Rich markup syntax:

.. code-block:: python

   RichConsoleConfiguration(
       markup=True,
   )
