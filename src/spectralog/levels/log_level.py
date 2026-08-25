from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LogLevel:
    """Represent a registered SpectraLog log-level definition.

    ``LogLevel`` stores the normalized name, numeric severity, and console color
    associated with a single logging level.

    Instances are immutable and use slots, making each level definition stable
    after creation and preventing arbitrary attributes from being added
    dynamically.

    The registry uses this model for both SpectraLog's built-in levels and custom
    levels registered at runtime.

    Attributes:
        name:
            Normalized log-level name, typically uppercase, such as ``"INFO"`` or
            ``"NOTICE"``.

        severity:
            Integer logging severity associated with the level.

        color:
            Colorlog-compatible color name used by compatible SpectraLog console
            formatters.

    Example:
        Represent a custom level definition::

            log_level = LogLevel(
                name="NOTICE",
                severity=35,
                color="cyan",
            )"""

    name: str
    severity: int
    color: str
