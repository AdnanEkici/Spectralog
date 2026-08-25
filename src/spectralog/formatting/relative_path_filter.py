from __future__ import annotations

import logging
from pathlib import Path


class RelativePathFilter(logging.Filter):
    """Enrich log records with a source path relative to a project root.

    ``RelativePathFilter`` adds a ``relative_path`` attribute to each
    :class:`logging.LogRecord` processed by the filter. SpectraLog formatters can
    then reference this value through ``%(relative_path)s`` when source-path
    display is enabled.

    The project root may be supplied explicitly. When omitted, the current working
    directory is resolved and used as the root.

    If the log record's absolute source path is located beneath the configured
    project root, ``relative_path`` contains the path relative to that root. If the
    source file lies outside the project root, the filter falls back to the
    record's file name.

    The resulting path is normalized to POSIX-style separators so that formatted
    log output remains consistent across operating systems.

    This filter never rejects a log record; its purpose is to enrich the record
    with additional path metadata before formatting."""

    def __init__(
        self,
        project_root: str | Path | None = None,
    ) -> None:
        """Initialize the relative-path filter.

        The supplied project root is converted to a :class:`pathlib.Path` and resolved
        to an absolute path. When no project root is provided, the resolved current
        working directory is used.

        Args:
            project_root:
                Optional directory used as the base for relative source-path
                calculation. Strings and :class:`pathlib.Path` instances are accepted.
                When ``None``, :func:`pathlib.Path.cwd` is used. Defaults to ``None``."""
        super().__init__()

        resolved_project_root = Path(project_root).resolve() if project_root is not None else Path.cwd().resolve()

        self._project_root = resolved_project_root

    def filter(
        self,
        record: logging.LogRecord,
    ) -> bool:
        """Add normalized relative source-path information to a log record.

        The record's absolute ``pathname`` is resolved and compared with the
        configured project root. When the source path is contained within that root,
        the relative path is stored on the record as ``relative_path``.

        If the source path cannot be expressed relative to the configured project
        root, the record's ``filename`` is used instead.

        The stored value uses POSIX-style path separators regardless of the host
        operating system.

        The method always returns ``True``, so records are enriched but never filtered
        out.

        Args:
            record:
                Log record whose source-path metadata should be enriched.

        Returns:
            bool:
                Always ``True``, allowing the log record to continue through the
                logging pipeline."""
        absolute_path = Path(record.pathname).resolve()

        try:
            relative_path = absolute_path.relative_to(
                self._project_root,
            )
        except ValueError:
            relative_path = Path(record.filename)

        record.relative_path = relative_path.as_posix()

        should_log_record = True
        return should_log_record
