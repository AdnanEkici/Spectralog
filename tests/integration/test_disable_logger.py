from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]  # noqa
SRC_DIR = PROJECT_ROOT / "src"  # noqa
sys.path.insert(0, str(SRC_DIR))  # noqa

from spectralog import CreateSpectraLogger  # noqa: E402
from spectralog import disable_application_logging  # noqa: E402
from spectralog import get_logger  # noqa: E402
from spectralog import silence_application_logging  # noqa: E402


class DummyLoggedApplication:
    def __init__(
        self,
        logs_directory: Path,
    ) -> None:
        self._logs_directory = logs_directory

    def initialize_logger(
        self,
    ) -> None:
        CreateSpectraLogger(
            logs_directory=self._logs_directory,
            log_file_name="dummy-application.log",
            save_logs=True,
        )

    def execute(
        self,
    ) -> None:
        logger = get_logger()

        logger.info(
            "Dummy application started",
        )

        logger.warning(
            "Dummy application warning",
        )

        logger.error(
            "Dummy application error",
        )


class IntegrationTestApplicationLoggingEnabled(unittest.TestCase):
    def test_dummy_application_creates_and_writes_log_file(
        self,
    ) -> None:
        """Verifies that the dummy application creates and writes its log file during normal package usage."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            logs_directory = (
                Path(
                    temporary_directory,
                )
                / "logs"
            )

            dummy_application = DummyLoggedApplication(
                logs_directory=logs_directory,
            )

            dummy_application.initialize_logger()

            try:
                dummy_application.execute()
            finally:
                logger = get_logger()
                logger.shutdown()

            log_file_path = logs_directory / "dummy-application.log"

            self.assertTrue(
                log_file_path.exists(),
                ("Expected normal SpectraLog usage to create the " "dummy application log file."),
            )

            log_file_contents = log_file_path.read_text(
                encoding="utf-8",
            )

            self.assertIn(
                "Dummy application started",
                log_file_contents,
                ("Expected the dummy application's INFO message to " "be written to the log file."),
            )

            self.assertIn(
                "Dummy application warning",
                log_file_contents,
                ("Expected the dummy application's WARNING message to " "be written to the log file."),
            )

            self.assertIn(
                "Dummy application error",
                log_file_contents,
                ("Expected the dummy application's ERROR message to " "be written to the log file."),
            )


@disable_application_logging
class IntegrationTestApplicationLoggingDisabled(unittest.TestCase):
    def test_dummy_application_does_not_create_log_file(
        self,
    ) -> None:
        """Verifies that the logging disable decorator prevents the dummy application from creating logging infrastructure."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            logs_directory = (
                Path(
                    temporary_directory,
                )
                / "logs"
            )

            dummy_application = DummyLoggedApplication(
                logs_directory=logs_directory,
            )

            dummy_application.initialize_logger()
            dummy_application.execute()

            self.assertFalse(
                logs_directory.exists(),
                ("Expected disable_application_logging to prevent the " "dummy application from creating its logs directory."),
            )

    def test_dummy_application_can_still_use_logger_api(
        self,
    ) -> None:
        """Verifies that application code can continue calling the SpectraLog API while logging output is disabled."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            logs_directory = (
                Path(
                    temporary_directory,
                )
                / "logs"
            )

            dummy_application = DummyLoggedApplication(
                logs_directory=logs_directory,
            )

            dummy_application.initialize_logger()

            try:
                dummy_application.execute()
            except Exception as exception:
                self.fail(
                    (
                        "Expected the dummy application to use the logger "
                        "normally while logging is disabled, but an "
                        f"exception was raised: {exception!r}"
                    ),
                )

            self.assertFalse(
                logs_directory.exists(),
                ("Expected disabled logging to avoid creating the logs " "directory even though application logging methods were called."),
            )



    def test_dummy_application_can_use_get_logger_without_explicit_initialization(
            self,
        ) -> None:
            """Verifies that get_logger returns a disabled fallback logger before explicit initialization."""
            with tempfile.TemporaryDirectory() as temporary_directory:
                logs_directory = (
                    Path(
                        temporary_directory,
                    )
                    / "logs"
                )

                dummy_application = DummyLoggedApplication(
                    logs_directory=logs_directory,
                )

                try:
                    dummy_application.execute()
                except Exception as exception:
                    self.fail(
                        (
                            "Expected get_logger() to return a disabled fallback "
                            "logger before explicit initialization, but an "
                            f"exception was raised: {exception!r}"
                        ),
                    )

                self.assertFalse(
                    logs_directory.exists(),
                    (
                        "Expected fallback logging to avoid creating the logs "
                        "directory when CreateSpectraLogger was not called."
                    ),
        )            
                
    def test_dummy_application_can_initialize_after_fallback_logger_was_created(
        self,
    ) -> None:
        """Verifies that explicit initialization succeeds after a disabled fallback logger was created."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            logs_directory = (
                Path(
                    temporary_directory,
                )
                / "logs"
            )

            dummy_application = DummyLoggedApplication(
                logs_directory=logs_directory,
            )

            fallback_logger = get_logger()

            try:
                dummy_application.initialize_logger()
                dummy_application.execute()
            except Exception as exception:
                self.fail(
                    (
                        "Expected explicit initialization to replace the "
                        "disabled fallback logger, but an exception was "
                        f"raised: {exception!r}"
                    ),
                )

            configured_logger = get_logger()

            self.assertIsNot(
                configured_logger,
                fallback_logger,
                (
                    "Expected CreateSpectraLogger to replace the temporary "
                    "fallback logger with a newly initialized logger."
                ),
            )

            self.assertFalse(
                logs_directory.exists(),
                (
                    "Expected disable_application_logging to continue "
                    "preventing log file creation after explicit initialization."
                ),
        )
            
            
class IntegrationTestSilenceApplicationLogging(unittest.TestCase):
    def test_silenced_function_does_not_create_log_file(
        self,
    ) -> None:
        """Verifies that silence_application_logging prevents log file creation inside a decorated function."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            logs_directory = (
                Path(
                    temporary_directory,
                )
                / "logs"
            )

            dummy_application = DummyLoggedApplication(
                logs_directory=logs_directory,
            )

            @silence_application_logging
            def execute_dummy_application() -> None:
                dummy_application.initialize_logger()
                dummy_application.execute()

            execute_dummy_application()

            self.assertFalse(
                logs_directory.exists(),
                (
                    "Expected silence_application_logging to prevent the "
                    "dummy application from creating its logs directory."
                ),
            )

    def test_silenced_function_can_use_get_logger_without_initialization(
        self,
    ) -> None:
        """Verifies that get_logger works without explicit initialization inside a silenced function."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            logs_directory = (
                Path(
                    temporary_directory,
                )
                / "logs"
            )

            dummy_application = DummyLoggedApplication(
                logs_directory=logs_directory,
            )

            @silence_application_logging
            def execute_dummy_application() -> None:
                dummy_application.execute()

            try:
                execute_dummy_application()
            except Exception as exception:
                self.fail(
                    (
                        "Expected get_logger() to return a disabled fallback "
                        "logger inside silence_application_logging, but an "
                        f"exception was raised: {exception!r}"
                    ),
                )

            self.assertFalse(
                logs_directory.exists(),
                (
                    "Expected fallback logging inside "
                    "silence_application_logging not to create the logs directory."
                ),
            )

    def test_silenced_function_can_initialize_after_fallback_logger_was_created(
        self,
    ) -> None:
        """Verifies that explicit initialization succeeds after fallback logger creation inside a silenced function."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            logs_directory = (
                Path(
                    temporary_directory,
                )
                / "logs"
            )

            dummy_application = DummyLoggedApplication(
                logs_directory=logs_directory,
            )

            fallback_logger = None
            configured_logger = None

            @silence_application_logging
            def execute_dummy_application() -> None:
                nonlocal fallback_logger
                nonlocal configured_logger

                fallback_logger = get_logger()

                dummy_application.initialize_logger()

                configured_logger = get_logger()

                dummy_application.execute()

            try:
                execute_dummy_application()
            except Exception as exception:
                self.fail(
                    (
                        "Expected explicit initialization to replace the "
                        "disabled fallback logger inside "
                        "silence_application_logging, but an exception was "
                        f"raised: {exception!r}"
                    ),
                )

            self.assertIsNot(
                configured_logger,
                fallback_logger,
                (
                    "Expected CreateSpectraLogger to replace the temporary "
                    "fallback logger inside silence_application_logging."
                ),
            )

            self.assertFalse(
                logs_directory.exists(),
                (
                    "Expected silence_application_logging to prevent "
                    "log file creation after explicit initialization."
                ),
            )

    def test_silenced_function_preserves_return_value(
        self,
    ) -> None:
        """Verifies that silence_application_logging preserves the decorated function return value."""

        @silence_application_logging
        def calculate_value() -> int:
            return 42

        returned_value = calculate_value()

        self.assertEqual(
            returned_value,
            42,
            (
                "Expected silence_application_logging to preserve the "
                "decorated function return value."
            ),
        )

    def test_silenced_function_propagates_application_exception(
        self,
    ) -> None:
        """Verifies that silence_application_logging does not suppress exceptions raised by application code."""

        @silence_application_logging
        def execute_failing_application() -> None:
            raise RuntimeError(
                "Dummy application failure",
            )

        with self.assertRaisesRegex(
            RuntimeError,
            "Dummy application failure",
            msg=(
                "Expected silence_application_logging to propagate "
                "exceptions raised by the decorated function."
            ),
        ):
            execute_failing_application()