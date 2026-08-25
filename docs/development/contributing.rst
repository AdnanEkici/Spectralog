Contributing
============

Contributions to SpectraLog are welcome. This document describes the expected
development workflow, code-quality requirements, testing strategy, and
documentation standards for changes to the project.

Development Setup
-----------------

Clone the repository and install SpectraLog in editable mode:

.. code-block:: bash

   git clone <repository-url>
   cd <repository-directory>
   python -m pip install -e .

Install development and documentation dependencies as required by the project:

.. code-block:: bash

   python -m pip install -e ".[docs]"

If the project defines a separate development dependency group, install that
group as well.

Project Structure
-----------------

The source code follows a ``src`` layout:

.. code-block:: text

   src/
   └── spectralog/
       ├── api/
       ├── configuration/
       ├── core/
       ├── exceptions/
       ├── files/
       ├── formatting/
       ├── handlers/
       ├── levels/
       └── runtime/

Tests are organized separately from the package source:

.. code-block:: text

   tests/
   ├── unit/
   └── integration/

Documentation is maintained under:

.. code-block:: text

   docs/

Architecture
------------

Before making structural changes, review :doc:`architecture`.

SpectraLog separates responsibilities across configuration models, builders,
factories, formatter strategies, handler factories, log-level management, and
runtime lifecycle components.

Contributions should preserve these boundaries unless a deliberate
architectural change is being introduced.

Code Style
----------

New production code should follow the conventions already used throughout the
project.

In particular:

- use explicit type annotations;
- prefer descriptive variable names;
- avoid abbreviated variable names;
- keep classes focused on a single responsibility;
- inject collaborators where appropriate rather than constructing unrelated
  dependencies inside domain components;
- prefer protocol-based dependencies where an abstraction is useful;
- keep public interfaces small and intentional;
- avoid unnecessary comments when the implementation can be expressed clearly
  through naming and structure;
- preserve existing return-value style and project formatting conventions.

Type Checking
-------------

All new and modified code should remain compatible with the project's static
type-checking configuration.

Run the configured type checker before submitting changes.

For example:

.. code-block:: bash

   mypy src tests

Do not suppress type errors unless there is a specific and documented reason.
Prefer accurate typing, explicit casts, or interface improvements over broad
``# type: ignore`` directives.

Unit Tests
----------

Unit tests should exercise classes and functions in isolation.

The project uses :mod:`unittest`.

Test classes should follow the project's naming convention, for example:

.. code-block:: python

   class UnitTestLogFilePathResolver(unittest.TestCase):
       ...

Each test method should include a concise one-sentence docstring describing the
behavior being verified.

Assertions should include meaningful failure messages where supported by the
``unittest`` assertion API.

For example:

.. code-block:: python

   self.assertEqual(
       actual_value,
       expected_value,
       "Expected the resolved log level to match the registered severity.",
   )

Mocks should be used for external side effects or collaborator boundaries when
the purpose of the test is to verify local behavior.

Avoid mocking the behavior that the test is specifically intended to verify.

Integration Tests
-----------------

Integration tests should exercise SpectraLog through realistic package usage
and should avoid mocking internal package components.

Fresh Python subprocesses are preferred when a scenario requires complete
isolation of process-local singleton state, ``atexit`` registration, logging
handlers, or multiprocessing runtime state.

Integration tests should verify observable behavior such as:

- console output;
- log file creation;
- plain-text file contents;
- JSON Lines output;
- custom log-level behavior;
- Rich console integration;
- syslog transmission;
- multiprocessing logging shutdown;
- public API imports;
- logging suppression in tests.

Singleton Behavior
------------------

``ApplicationLogger`` is a process-local singleton.

Tests should not depend on arbitrary execution order or reuse singleton state
between logically independent scenarios.

When full process isolation is required, use a subprocess rather than directly
modifying internal singleton state in an integration test.

Logging Tests
-------------

Tests involving persistent logging should use temporary directories whenever
possible.

For example:

.. code-block:: python

   import tempfile
   from pathlib import Path

   with tempfile.TemporaryDirectory() as temporary_directory:
       logs_directory = Path(temporary_directory) / "logs"

This prevents test runs from leaving log files in the repository.

Tests that should execute application code without producing SpectraLog output
may use :func:`spectralog.disable_application_logging`.

Documentation
-------------

Public APIs should include complete docstrings suitable for Sphinx-generated
documentation.

SpectraLog uses Google-style docstrings rendered through
``sphinx.ext.napoleon``.

Public docstrings should document, where applicable:

- the purpose of the object;
- important lifecycle behavior;
- arguments;
- return values;
- raised exceptions;
- relevant side effects;
- examples;
- important limitations or operational notes.

Do not document behavior that is not guaranteed by the implementation.

If public behavior changes, update the corresponding guide and API reference
documentation in the same contribution.

Building the Documentation
--------------------------

Build the HTML documentation with:

.. code-block:: bash

   sphinx-build -b html docs docs/_build/html

Before submitting documentation changes, run Sphinx with warnings treated as
errors:

.. code-block:: bash

   sphinx-build -W --keep-going -b html docs docs/_build/html

The documentation build should complete without warnings.

Public API Changes
------------------

Changes to the public package API require additional care.

Examples of public API changes include:

- adding or removing package-root exports;
- changing function parameters or defaults;
- changing configuration fields;
- changing exception types;
- changing file naming behavior;
- changing logging output semantics;
- changing singleton lifecycle behavior.

When modifying public behavior:

1. update implementation tests;
2. update integration tests;
3. update public docstrings;
4. update the relevant user guide;
5. update the API reference if necessary;
6. consider backward compatibility.

Package-root imports should remain intentional. Internal implementation classes
should not be exported from ``spectralog`` unless they are intended to become
part of the supported public API.

Exceptions
----------

SpectraLog-specific exceptions should inherit from
:class:`spectralog.SpectraLogError`.

Use specific exception types where callers may reasonably need to distinguish
different failure conditions.

Avoid replacing meaningful package-specific exceptions with generic exceptions
unless the error genuinely represents a standard Python contract violation.

Adding Log Levels
-----------------

Changes to custom log-level behavior should preserve the registry's validation
rules and uniqueness guarantees.

Custom level names are normalized before registration. Names and numeric
severities must remain unique within a registry.

Changes to supported colors should remain compatible with the formatter
backend used by SpectraLog.

Dependency Changes
------------------

Avoid introducing new runtime dependencies unless they provide a clear benefit
to package users.

A dependency required only for testing, documentation, linting, or release
automation should be placed in the appropriate optional development dependency
group rather than the package's runtime dependency set.

Submitting Changes
------------------

Before submitting a contribution, verify that:

- unit tests pass;
- integration tests pass;
- static type checking passes;
- documentation builds without warnings;
- new public behavior is documented;
- no generated log files or build artifacts are included unintentionally.

A typical validation sequence may look like:

.. code-block:: bash

   python -m unittest discover -s tests
   mypy src tests
   sphinx-build -W --keep-going -b html docs docs/_build/html

Commit changes in focused units that describe one logical modification at a
time.

Pull Requests
-------------

A pull request should clearly describe:

- what behavior was changed;
- why the change is needed;
- whether the public API is affected;
- what tests were added or updated;
- whether documentation was updated;
- any compatibility considerations or known limitations.

Changes that alter logging semantics, multiprocessing behavior, file handling,
or public API contracts should include corresponding integration coverage.
