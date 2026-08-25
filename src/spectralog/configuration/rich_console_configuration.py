from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RichConsoleConfiguration:
    """Configure SpectraLog's Rich-based console output.

    This immutable configuration object controls the presentation and traceback
    behavior of the Rich console handler used by SpectraLog.

    Providing an instance of this configuration when creating a SpectraLog logger
    enables Rich console rendering instead of the standard colored console
    handler. These options affect console output only and do not change file,
    JSON, or syslog formatting.

    Instances are frozen and use slots, preventing configuration values from being
    modified after construction or arbitrary attributes from being added
    dynamically.

    Attributes:
        show_time:
            Displays Rich's timestamp column for each console log record when
            ``True``. Defaults to ``True``.

        show_level:
            Displays the log level column in Rich console output when ``True``.
            Defaults to ``True``.

        show_path:
            Displays source path information in Rich console output when ``True``.
            Defaults to ``True``.

        rich_tracebacks:
            Enables Rich-formatted exception tracebacks when ``True``. When
            enabled, exceptions logged with traceback information are rendered
            using Rich's enhanced traceback presentation. Defaults to ``True``.

        markup:
            Enables Rich markup processing within log messages when ``True``.
            When ``False``, Rich markup syntax contained in application messages
            is treated as ordinary text. Defaults to ``False``.

    Example:
        Configure compact Rich console output without timestamps or source paths::

            from spectralog import RichConsoleConfiguration

            rich_configuration = RichConsoleConfiguration(
                show_time=False,
                show_level=True,
                show_path=False,
                rich_tracebacks=True,
                markup=False,
            )
    """

    show_time: bool = True
    show_level: bool = True
    show_path: bool = True
    rich_tracebacks: bool = True
    markup: bool = False
