from __future__ import annotations

from spectralog.configuration.configuration import (
    LoggerConfiguration,
)


class LogFormatBuilder:
    """Build SpectraLog format strings from logger configuration.

    ``LogFormatBuilder`` constructs the plain-text format strings used by
    SpectraLog's console and file formatters.

    When an explicit ``console_format`` or ``file_format`` is supplied in the
    active :class:`LoggerConfiguration`, that value is returned unchanged.
    Otherwise, the builder composes a format from the configured timestamp,
    severity, source-location, line-number, and message fields.

    Console formats wrap the generated plain-text format with colorlog-compatible
    ``%(log_color)s`` and ``%(reset)s`` fields so that the standard SpectraLog
    console formatter can apply level-specific colors.

    File formats remain plain and do not include console color escape fields.

    The generated format components are separated with ``" | "``."""

    def build_console_format(
        self,
        configuration: LoggerConfiguration,
    ) -> str:
        """Build the format string used by the standard colored console formatter.

        If ``configuration.console_format`` is provided, that explicit format string
        is returned unchanged.

        Otherwise, a plain format is generated from the active configuration and
        wrapped with the ``%(log_color)s`` and ``%(reset)s`` fields expected by
        SpectraLog's color-aware console formatter.

        Args:
            configuration:
                Logger configuration controlling the generated console format,
                including timestamp and source-location fields and any explicit custom
                console format.

        Returns:
            str:
                The explicit console format when one is configured, otherwise the
                generated plain format wrapped with console color fields."""
        if configuration.console_format is not None:
            console_format = configuration.console_format
            return console_format

        plain_format = self._build_plain_format(
            configuration,
        )

        console_format = "%(log_color)s" f"{plain_format}" "%(reset)s"

        built_console_format = console_format
        return built_console_format

    def build_file_format(
        self,
        configuration: LoggerConfiguration,
    ) -> str:
        """Build the plain-text format string used for file logging.

        If ``configuration.file_format`` is provided, that explicit format string is
        returned unchanged.

        Otherwise, the format is generated from the active logger configuration using
        the same plain-format construction rules used by the standard console
        formatter, but without color-related fields.

        Args:
            configuration:
                Logger configuration controlling the generated file format, including
                timestamp and source-location fields and any explicit custom file
                format.

        Returns:
            str:
                The explicit file format when one is configured, otherwise the
                generated plain-text logging format."""
        if configuration.file_format is not None:
            file_format = configuration.file_format
            return file_format

        file_format = self._build_plain_format(
            configuration,
        )

        built_file_format = file_format
        return built_file_format

    def _build_plain_format(
        self,
        configuration: LoggerConfiguration,
    ) -> str:
        """Build the default plain-text format from logger display settings.

        The format is assembled in a fixed order:

        1. ``%(asctime)s`` when ``show_datetime`` is enabled.
        2. ``%(levelname)s`` in all generated formats.
        3. Source-location information when requested.
        4. ``%(message)s`` in all generated formats.

        When ``show_folder_name`` is enabled, source information is represented by
        ``%(relative_path)s``. If ``show_line`` is also enabled, the line number is
        appended to that path as ``:%(lineno)d``.

        When ``show_folder_name`` is disabled but ``show_line`` is enabled, the source
        location is represented as ``line %(lineno)d``.

        All generated components are joined with ``" | "``.

        Args:
            configuration:
                Logger configuration controlling whether timestamps, relative source
                paths, and line numbers are included.

        Returns:
            str:
                The generated plain-text logging format string."""
        format_parts: list[str] = []

        if configuration.show_datetime:
            format_parts.append("%(asctime)s")

        format_parts.append("%(levelname)s")

        if configuration.show_folder_name:
            location_format = "%(relative_path)s"

            if configuration.show_line:
                location_format = f"{location_format}:%(lineno)d"

            format_parts.append(location_format)

        elif configuration.show_line:
            format_parts.append("line %(lineno)d")

        format_parts.append("%(message)s")

        plain_format = " | ".join(format_parts)
        return plain_format
