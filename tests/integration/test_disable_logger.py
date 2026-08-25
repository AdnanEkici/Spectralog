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
