from __future__ import annotations

import logging
import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]  # noqa
SRC_DIR = PROJECT_ROOT / "src"  # noqa
sys.path.insert(0, str(SRC_DIR))  # noqa
from spectralog.formatting.relative_path_filter import RelativePathFilter  # noqa: E402


class UnitTestRelativePathFilter(unittest.TestCase):
    def test_constructor_uses_resolved_supplied_project_root(
        self,
    ) -> None:
        """Verifies that the filter stores the resolved supplied project root."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            project_root = Path(
                temporary_directory,
            )

            relative_path_filter = RelativePathFilter(
                project_root=project_root,
            )

            self.assertEqual(
                relative_path_filter._project_root,
                project_root.resolve(),
                ("Expected the filter to store the resolved supplied " "project root."),
            )

    def test_constructor_uses_current_working_directory_when_project_root_is_none(
        self,
    ) -> None:
        """Verifies that the filter uses the resolved current working directory when no project root is supplied."""
        relative_path_filter = RelativePathFilter(
            project_root=None,
        )

        self.assertEqual(
            relative_path_filter._project_root,
            Path.cwd().resolve(),
            ("Expected the filter to use the resolved current working " "directory when project_root is None."),
        )

    def test_constructor_accepts_string_project_root(
        self,
    ) -> None:
        """Verifies that the filter accepts a string project root and stores its resolved path."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            relative_path_filter = RelativePathFilter(
                project_root=temporary_directory,
            )

            self.assertEqual(
                relative_path_filter._project_root,
                Path(temporary_directory).resolve(),
                ("Expected a string project root to be converted into " "its resolved Path representation."),
            )

    def test_filter_returns_true(
        self,
    ) -> None:
        """Verifies that filter always allows the supplied log record to be emitted."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            project_root = Path(
                temporary_directory,
            )

            source_file_path = project_root / "src" / "application.py"

            relative_path_filter = RelativePathFilter(
                project_root=project_root,
            )

            log_record = logging.LogRecord(
                name="spectralog-test",
                level=logging.INFO,
                pathname=str(source_file_path),
                lineno=100,
                msg="Application started",
                args=(),
                exc_info=None,
            )

            should_log_record = relative_path_filter.filter(
                record=log_record,
            )

            self.assertTrue(
                should_log_record,
                ("Expected filter() to return True so the supplied " "LogRecord remains eligible for logging."),
            )

    def test_filter_sets_relative_path_for_file_inside_project_root(
        self,
    ) -> None:
        """Verifies that filter stores a project-relative POSIX path for files inside the configured project root."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            project_root = Path(
                temporary_directory,
            )

            source_file_path = project_root / "src" / "spectralog" / "core" / "logger.py"

            relative_path_filter = RelativePathFilter(
                project_root=project_root,
            )

            log_record = logging.LogRecord(
                name="spectralog-test",
                level=logging.INFO,
                pathname=str(source_file_path),
                lineno=100,
                msg="Application started",
                args=(),
                exc_info=None,
            )

            relative_path_filter.filter(
                record=log_record,
            )

            relative_path = getattr(
                log_record,
                "relative_path",
            )

            self.assertEqual(
                relative_path,
                "src/spectralog/core/logger.py",
                ("Expected relative_path to contain the file path " "relative to the configured project root."),
            )

    def test_filter_sets_filename_when_file_is_outside_project_root(
        self,
    ) -> None:
        """Verifies that filter falls back to the record filename when the source path is outside the configured project root."""
        with tempfile.TemporaryDirectory() as project_directory:
            with tempfile.TemporaryDirectory() as external_directory:
                project_root = Path(
                    project_directory,
                )

                external_file_path = Path(external_directory) / "external_module.py"

                relative_path_filter = RelativePathFilter(
                    project_root=project_root,
                )

                log_record = logging.LogRecord(
                    name="spectralog-test",
                    level=logging.INFO,
                    pathname=str(external_file_path),
                    lineno=100,
                    msg="Application started",
                    args=(),
                    exc_info=None,
                )

                relative_path_filter.filter(
                    record=log_record,
                )

                relative_path = getattr(
                    log_record,
                    "relative_path",
                )

                self.assertEqual(
                    relative_path,
                    "external_module.py",
                    (
                        "Expected relative_path to fall back to the "
                        "LogRecord filename when the source path is outside "
                        "the configured project root."
                    ),
                )

    def test_filter_uses_posix_path_separators(
        self,
    ) -> None:
        """Verifies that filter stores relative paths using POSIX separators."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            project_root = Path(
                temporary_directory,
            )

            source_file_path = project_root / "src" / "spectralog" / "logger.py"

            relative_path_filter = RelativePathFilter(
                project_root=project_root,
            )

            log_record = logging.LogRecord(
                name="spectralog-test",
                level=logging.INFO,
                pathname=str(source_file_path),
                lineno=100,
                msg="Application started",
                args=(),
                exc_info=None,
            )

            relative_path_filter.filter(
                record=log_record,
            )

            relative_path = getattr(
                log_record,
                "relative_path",
            )

            self.assertEqual(
                relative_path,
                "src/spectralog/logger.py",
                ("Expected relative_path to use POSIX path separators " "independently of the host operating system."),
            )

    def test_filter_handles_file_directly_inside_project_root(
        self,
    ) -> None:
        """Verifies that filter correctly handles a source file located directly inside the project root."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            project_root = Path(
                temporary_directory,
            )

            source_file_path = project_root / "main.py"

            relative_path_filter = RelativePathFilter(
                project_root=project_root,
            )

            log_record = logging.LogRecord(
                name="spectralog-test",
                level=logging.INFO,
                pathname=str(source_file_path),
                lineno=100,
                msg="Application started",
                args=(),
                exc_info=None,
            )

            relative_path_filter.filter(
                record=log_record,
            )

            relative_path = getattr(
                log_record,
                "relative_path",
            )

            self.assertEqual(
                relative_path,
                "main.py",
                ("Expected a file directly inside the project root to " "produce only its filename as relative_path."),
            )

    def test_filter_overwrites_existing_relative_path_attribute(
        self,
    ) -> None:
        """Verifies that filter replaces any existing relative_path value with the path derived from the current record."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            project_root = Path(
                temporary_directory,
            )

            source_file_path = project_root / "src" / "worker.py"

            relative_path_filter = RelativePathFilter(
                project_root=project_root,
            )

            log_record = logging.LogRecord(
                name="spectralog-test",
                level=logging.INFO,
                pathname=str(source_file_path),
                lineno=100,
                msg="Application started",
                args=(),
                exc_info=None,
            )

            setattr(
                log_record,
                "relative_path",
                "incorrect/path.py",
            )

            relative_path_filter.filter(
                record=log_record,
            )

            relative_path = getattr(
                log_record,
                "relative_path",
            )

            self.assertEqual(
                relative_path,
                "src/worker.py",
                ("Expected filter() to replace an existing relative_path " "with the path derived from the current LogRecord."),
            )

    def test_filter_uses_record_filename_for_external_nested_path(
        self,
    ) -> None:
        """Verifies that the external-path fallback strips all parent directories and retains only the filename."""
        with tempfile.TemporaryDirectory() as project_directory:
            with tempfile.TemporaryDirectory() as external_directory:
                project_root = Path(
                    project_directory,
                )

                external_file_path = Path(external_directory) / "package" / "nested" / "module.py"

                relative_path_filter = RelativePathFilter(
                    project_root=project_root,
                )

                log_record = logging.LogRecord(
                    name="spectralog-test",
                    level=logging.INFO,
                    pathname=str(external_file_path),
                    lineno=100,
                    msg="Application started",
                    args=(),
                    exc_info=None,
                )

                relative_path_filter.filter(
                    record=log_record,
                )

                relative_path = getattr(
                    log_record,
                    "relative_path",
                )

                self.assertEqual(
                    relative_path,
                    "module.py",
                    ("Expected the external-path fallback to retain only " "the source filename."),
                )

    def test_filter_resolves_parent_directory_segments(
        self,
    ) -> None:
        """Verifies that filter resolves parent-directory segments before calculating the relative path."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            project_root = Path(
                temporary_directory,
            )

            source_file_path = project_root / "src" / "temporary" / ".." / "logger.py"

            relative_path_filter = RelativePathFilter(
                project_root=project_root,
            )

            log_record = logging.LogRecord(
                name="spectralog-test",
                level=logging.INFO,
                pathname=str(source_file_path),
                lineno=100,
                msg="Application started",
                args=(),
                exc_info=None,
            )

            relative_path_filter.filter(
                record=log_record,
            )

            relative_path = getattr(
                log_record,
                "relative_path",
            )

            self.assertEqual(
                relative_path,
                "src/logger.py",
                ("Expected filter() to resolve parent-directory segments " "before determining the project-relative path."),
            )

    def test_filter_resolves_current_directory_segments(
        self,
    ) -> None:
        """Verifies that filter resolves current-directory segments before calculating the relative path."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            project_root = Path(
                temporary_directory,
            )

            source_file_path = project_root / "src" / "." / "logger.py"

            relative_path_filter = RelativePathFilter(
                project_root=project_root,
            )

            log_record = logging.LogRecord(
                name="spectralog-test",
                level=logging.INFO,
                pathname=str(source_file_path),
                lineno=100,
                msg="Application started",
                args=(),
                exc_info=None,
            )

            relative_path_filter.filter(
                record=log_record,
            )

            relative_path = getattr(
                log_record,
                "relative_path",
            )

            self.assertEqual(
                relative_path,
                "src/logger.py",
                ("Expected filter() to normalize current-directory " "segments before determining relative_path."),
            )

    def test_filter_can_process_multiple_records(
        self,
    ) -> None:
        """Verifies that the same filter instance independently calculates relative paths for multiple log records."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            project_root = Path(
                temporary_directory,
            )

            first_file_path = project_root / "src" / "first.py"

            second_file_path = project_root / "src" / "nested" / "second.py"

            relative_path_filter = RelativePathFilter(
                project_root=project_root,
            )

            first_log_record = logging.LogRecord(
                name="spectralog-test",
                level=logging.INFO,
                pathname=str(first_file_path),
                lineno=100,
                msg="First message",
                args=(),
                exc_info=None,
            )

            second_log_record = logging.LogRecord(
                name="spectralog-test",
                level=logging.INFO,
                pathname=str(second_file_path),
                lineno=200,
                msg="Second message",
                args=(),
                exc_info=None,
            )

            first_should_log_record = relative_path_filter.filter(
                record=first_log_record,
            )

            second_should_log_record = relative_path_filter.filter(
                record=second_log_record,
            )

            first_relative_path = getattr(
                first_log_record,
                "relative_path",
            )

            second_relative_path = getattr(
                second_log_record,
                "relative_path",
            )

            self.assertTrue(
                first_should_log_record,
                ("Expected the first LogRecord to remain eligible for " "logging."),
            )

            self.assertTrue(
                second_should_log_record,
                ("Expected the second LogRecord to remain eligible for " "logging."),
            )

            self.assertEqual(
                first_relative_path,
                "src/first.py",
                ("Expected the first LogRecord to receive its own " "project-relative path."),
            )

            self.assertEqual(
                second_relative_path,
                "src/nested/second.py",
                ("Expected the second LogRecord to receive its own " "project-relative path."),
            )
