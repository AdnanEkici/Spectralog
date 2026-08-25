Custom Log Levels
=================

SpectraLog allows custom logging levels to be registered at runtime.

Register a Level
----------------

.. code-block:: python

   logger.add_log_level(
       name="NOTICE",
       color="cyan",
       severity=35,
   )

Dynamic Logging Methods
-----------------------

After registration, the level becomes available as a dynamic logger method:

.. code-block:: python

   logger.notice(
       "Deployment completed",
   )

The level may also be used through ``log``:

.. code-block:: python

   logger.log(
       "NOTICE",
       "Deployment completed",
   )

Naming Rules
------------

Custom level names:

- must not be empty;
- must begin with a letter;
- may contain letters, numbers, and underscores;
- are normalized to uppercase.

For example:

.. code-block:: python

   logger.add_log_level(
       name="audit_event",
       color="cyan",
       severity=35,
   )

is registered as:

.. code-block:: text

   AUDIT_EVENT

Severity Rules
--------------

Severity values must:

- be integers;
- not be boolean values;
- be greater than zero;
- not duplicate an existing registered severity.

Colors
------

Colors must be supported by ``colorlog``.
