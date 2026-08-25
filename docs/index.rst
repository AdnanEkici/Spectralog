SpectraLog
==========

SpectraLog is a configurable Python logging package providing colored console
logging, rotating file logging, structured JSON logging, Rich console output,
syslog integration, custom log levels, and multiprocessing-safe file logging.

It provides a small public API while keeping formatter, handler, and runtime
composition internally separated.

Quick Example
-------------

.. code-block:: python

   from spectralog import CreateSpectraLogger

   logger = CreateSpectraLogger(
       debug_mode=True,
       log_file_name="application.log",
   )

   logger.info("Application started")
   logger.warning("Configuration requires attention")

Features
--------

- Colored console logging
- Rotating file logging
- JSON Lines logging
- Rich console integration
- Syslog output
- Custom log levels
- Multiprocessing-safe file logging
- Process-local application logger
- Test-time logging suppression

Documentation
-------------

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   getting_started/installation
   getting_started/quickstart
   getting_started/basic_usage

.. toctree::
   :maxdepth: 2
   :caption: Guides

   guides/configuration
   guides/json_logging
   guides/rich_console
   guides/syslog
   guides/multiprocessing
   guides/custom_levels
   guides/testing

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/index

.. toctree::
   :maxdepth: 2
   :caption: Development

   development/architecture
   development/contributing

Indices
-------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
