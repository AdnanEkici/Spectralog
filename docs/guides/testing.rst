Disabling Logging in Tests
==========================

Applications often exercise code that initializes SpectraLog during unit or
integration tests. Creating console handlers, files, multiprocessing
infrastructure, or shutdown callbacks may be undesirable in those tests.

SpectraLog provides ``disable_application_logging`` for this purpose.

Basic Usage
-----------

.. code-block:: python

   import unittest

   from spectralog import CreateSpectraLogger
   from spectralog import disable_application_logging
   from spectralog import get_logger


   @disable_application_logging
   class UnitTestApplication(unittest.TestCase):
       def test_application_behavior(self) -> None:
           CreateSpectraLogger(
               log_file_name="application.log",
           )

           logger = get_logger()
           logger.info("This will not produce logging output")

           self.assertTrue(True)

Behavior
--------

While the decorated test class executes:

- SpectraLog's normal logger build operation is replaced with a disabled logger;
- no SpectraLog file handler is created;
- no Rich handler is created;
- no syslog handler is created;
- no multiprocessing logging runtime is created;
- SpectraLog ``atexit`` registration is suppressed;
- each test method receives isolated application-logger singleton state.

The application can continue to call ``CreateSpectraLogger``, ``get_logger``,
and normal logging methods without requiring test-specific changes to the
application code.
