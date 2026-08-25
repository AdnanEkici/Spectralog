Exceptions
==========

SpectraLog provides package-specific exceptions for logger lifecycle errors,
custom log-level validation, and registry operations.

All SpectraLog-specific exceptions inherit from
:class:`spectralog.exceptions.exceptions.SpectraLogError`.

Base Exception
--------------

.. autoexception:: spectralog.exceptions.exceptions.SpectraLogError

Application Logger Exceptions
-----------------------------

.. autoexception:: spectralog.exceptions.exceptions.SpectraApplicationLoggerAlreadyInitializedError

.. autoexception:: spectralog.exceptions.exceptions.SpectraApplicationLoggerReconfigurationError

Log-Level Registry Exceptions
-----------------------------

.. autoexception:: spectralog.exceptions.exceptions.SpectraLogLevelAlreadyExistsError

.. autoexception:: spectralog.exceptions.exceptions.SpectraLogLevelNotFoundError

Validation Exceptions
---------------------

.. autoexception:: spectralog.exceptions.exceptions.InvalidSpectraLogLevelNameError

.. autoexception:: spectralog.exceptions.exceptions.InvalidSpectraLogLevelSeverityError

.. autoexception:: spectralog.exceptions.exceptions.InvalidSpectraLogColorError

Handling SpectraLog Errors
--------------------------

Applications may catch a specific exception when different failure conditions
require different behavior.

For example:

.. code-block:: python

   from spectralog import CreateSpectraLogger
   from spectralog.exceptions.exceptions import (
       SpectraApplicationLoggerReconfigurationError,
   )

   try:
       CreateSpectraLogger()
       CreateSpectraLogger()
   except SpectraApplicationLoggerReconfigurationError:
       print("SpectraLog has already been configured.")

Catching All SpectraLog Errors
------------------------------

All package-specific exceptions inherit from ``SpectraLogError``.

This allows applications to handle any SpectraLog-specific failure through one
base exception when individual error types do not need separate handling.

.. code-block:: python

   from spectralog.exceptions.exceptions import SpectraLogError

   try:
       ...
   except SpectraLogError as exception:
       print(f"SpectraLog error: {exception}")

Application Logger Lifecycle
----------------------------

``SpectraApplicationLoggerAlreadyInitializedError``
    Raised when ``ApplicationLogger`` is instantiated outside SpectraLog's
    managed singleton lifecycle.

``SpectraApplicationLoggerReconfigurationError``
    Raised when configuration dependencies are supplied after the
    process-local application logger has already been initialized.

Custom Log Levels
-----------------

``SpectraLogLevelAlreadyExistsError``
    Raised when a custom log-level name is already registered or its numeric
    severity is already assigned to another level.

``SpectraLogLevelNotFoundError``
    Raised when SpectraLog cannot find a requested log-level name in the
    active registry.

``InvalidSpectraLogLevelNameError``
    Raised when a custom log-level name does not satisfy SpectraLog's naming
    requirements.

``InvalidSpectraLogLevelSeverityError``
    Raised when a custom severity is not a positive integer or is otherwise
    invalid.

``InvalidSpectraLogColorError``
    Raised when a custom log-level color is not supported by the configured
    color backend.

See Also
--------

See :doc:`../guides/custom_levels` for custom log-level registration and
validation behavior.

See :doc:`public_api` for the main SpectraLog public API.
