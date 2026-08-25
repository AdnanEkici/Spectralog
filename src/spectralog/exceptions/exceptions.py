from __future__ import annotations


class SpectraLogError(Exception):
    """Base exception for errors raised by SpectraLog's application logger.

    All SpectraLog-specific logger lifecycle, configuration, and log-level
    validation exceptions inherit from this class.

    Catching this exception allows callers to handle any SpectraLog application
    logger error through a single common base type."""

    pass


class SpectraApplicationLoggerAlreadyInitializedError(
    SpectraLogError,
):
    """Raised when :class:`ApplicationLogger` is instantiated outside its managed lifecycle.

    ``ApplicationLogger`` is designed to be created only through SpectraLog's
    singleton initialization path. Direct construction without the internal
    construction token raises this exception.

    Applications should initialize logging through :func:`CreateSpectraLogger` or
    retrieve the existing logger through :func:`get_logger`."""

    pass


class SpectraApplicationLoggerReconfigurationError(
    SpectraLogError,
):
    """Raised when an initialized application logger is configured again.

    SpectraLog uses a process-local :class:`ApplicationLogger` singleton. Once the
    singleton has been initialized, supplying a new logger builder or log-level
    registry is treated as an attempt to reconfigure the active logger and raises
    this exception.

    Applications should configure SpectraLog once during startup and use
    :func:`get_logger` for subsequent access."""

    pass


class SpectraLogLevelAlreadyExistsError(
    SpectraLogError,
):
    """Raised when attempting to register a log level that already exists.

    A log-level name must uniquely identify a single registered level within
    SpectraLog's log-level registry. Registering another level with an existing
    name raises this exception."""

    pass


class SpectraLogLevelNotFoundError(
    SpectraLogError,
):
    """Raised when a requested log level is not registered.

    This exception indicates that SpectraLog could not resolve the requested
    log-level name from its active log-level registry.

    The level must be one of SpectraLog's predefined levels or a custom level
    previously registered with :meth:`ApplicationLogger.add_log_level`."""

    pass


class InvalidSpectraLogLevelNameError(
    SpectraLogError,
):
    """Raised when a log-level name fails SpectraLog's validation requirements.

    This exception indicates that the supplied name cannot be used as a valid
    SpectraLog log-level identifier.

    The exact accepted naming rules are defined by the log-level registry's
    validation logic."""

    pass


class InvalidSpectraLogLevelSeverityError(
    SpectraLogError,
):
    """Raised when a log-level severity fails SpectraLog's validation requirements.

    Custom log levels must use a valid integer severity accepted by the log-level
    registry. This exception is raised when the supplied severity violates those
    requirements.

    The exact accepted severity constraints are defined by the log-level
    registry's validation logic."""

    pass


class InvalidSpectraLogColorError(
    SpectraLogError,
):
    """Raised when a log-level color fails SpectraLog's validation requirements.

    Custom log levels may define a color used by compatible colored console
    formatters. This exception is raised when the supplied color is not accepted
    by SpectraLog's log-level registry.

    The exact supported color values are defined by the registry's color
    validation logic."""

    pass
