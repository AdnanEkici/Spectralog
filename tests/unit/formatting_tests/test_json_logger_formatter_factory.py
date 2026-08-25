from __future__ import annotations

import logging
import sys
import unittest
from pathlib import Path
from typing import cast
from unittest.mock import MagicMock
from unittest.mock import patch

PROJECT_ROOT = Path(__file__).resolve().parents[3]  # noqa
SRC_DIR = PROJECT_ROOT / "src"  # noqa
sys.path.insert(0, str(SRC_DIR))  # noqa


from spectralog.configuration.json_logger_configuration import JsonLoggerConfiguration  # noqa: E402
from spectralog.formatting.json_formatter import JsonLoggerFormatter  # noqa: E402
from spectralog.formatting.json_logger_formatter_factory import JsonLoggerFormatterFactory  # noqa: E402


class UnitTestJsonLoggerFormatterFactory(unittest.TestCase):
    def setUp(self) -> None:
        self.json_logger_formatter_factory = JsonLoggerFormatterFactory()

    @patch(
        "spectralog.formatting.json_logger_formatter_factory.JsonLoggerFormatter",
    )
    def test_create_constructs_json_logger_formatter_with_configuration(
        self,
        json_logger_formatter_class_mock: MagicMock,
    ) -> None:
        """Verifies that create constructs JsonLoggerFormatter using the supplied JSON logger configuration."""
        configuration = JsonLoggerConfiguration(
            include_timestamp=False,
            include_logger_name=False,
            include_process_information=False,
            include_thread_information=False,
        )

        json_logger_formatter_class_mock.return_value = MagicMock()

        self.json_logger_formatter_factory.create(
            configuration=configuration,
        )

        json_logger_formatter_class_mock.assert_called_once_with(
            configuration=configuration,
        )

    @patch(
        "spectralog.formatting.json_logger_formatter_factory.JsonLoggerFormatter",
    )
    def test_create_returns_created_json_logger_formatter(
        self,
        json_logger_formatter_class_mock: MagicMock,
    ) -> None:
        """Verifies that create returns the exact JsonLoggerFormatter instance produced by the constructor."""
        configuration = JsonLoggerConfiguration()

        json_logger_formatter = MagicMock()

        json_logger_formatter_class_mock.return_value = json_logger_formatter

        created_formatter = self.json_logger_formatter_factory.create(
            configuration=configuration,
        )

        self.assertIs(
            created_formatter,
            json_logger_formatter,
            ("Expected create() to return the exact JsonLoggerFormatter " "instance produced by the constructor."),
        )

    @patch(
        "spectralog.formatting.json_logger_formatter_factory.JsonLoggerFormatter",
    )
    def test_create_passes_same_configuration_instance(
        self,
        json_logger_formatter_class_mock: MagicMock,
    ) -> None:
        """Verifies that create passes the exact JsonLoggerConfiguration instance supplied by the caller."""
        configuration = JsonLoggerConfiguration(
            include_timestamp=True,
            include_logger_name=False,
            include_process_information=True,
            include_thread_information=False,
        )

        json_logger_formatter_class_mock.return_value = MagicMock()

        self.json_logger_formatter_factory.create(
            configuration=configuration,
        )

        supplied_configuration = json_logger_formatter_class_mock.call_args.kwargs["configuration"]

        self.assertIs(
            supplied_configuration,
            configuration,
            ("Expected JsonLoggerFormatter to receive the exact " "JsonLoggerConfiguration instance supplied to create()."),
        )

    @patch(
        "spectralog.formatting.json_logger_formatter_factory.JsonLoggerFormatter",
    )
    def test_create_preserves_custom_configuration_values(
        self,
        json_logger_formatter_class_mock: MagicMock,
    ) -> None:
        """Verifies that create preserves all custom JSON logger configuration values."""
        configuration = JsonLoggerConfiguration(
            include_timestamp=False,
            include_logger_name=True,
            include_process_information=False,
            include_thread_information=True,
        )

        json_logger_formatter_class_mock.return_value = MagicMock()

        self.json_logger_formatter_factory.create(
            configuration=configuration,
        )

        supplied_configuration = json_logger_formatter_class_mock.call_args.kwargs["configuration"]

        self.assertFalse(
            supplied_configuration.include_timestamp,
            ("Expected include_timestamp to remain False when passed " "to JsonLoggerFormatter."),
        )

        self.assertTrue(
            supplied_configuration.include_logger_name,
            ("Expected include_logger_name to remain True when passed " "to JsonLoggerFormatter."),
        )

        self.assertFalse(
            supplied_configuration.include_process_information,
            ("Expected include_process_information to remain False when " "passed to JsonLoggerFormatter."),
        )

        self.assertTrue(
            supplied_configuration.include_thread_information,
            ("Expected include_thread_information to remain True when " "passed to JsonLoggerFormatter."),
        )

    @patch(
        "spectralog.formatting.json_logger_formatter_factory.JsonLoggerFormatter",
    )
    def test_create_constructs_new_formatter_for_each_call(
        self,
        json_logger_formatter_class_mock: MagicMock,
    ) -> None:
        """Verifies that create constructs a new JsonLoggerFormatter for each invocation."""
        first_configuration = JsonLoggerConfiguration(
            include_timestamp=True,
        )

        second_configuration = JsonLoggerConfiguration(
            include_timestamp=False,
        )

        first_formatter = MagicMock()
        second_formatter = MagicMock()

        json_logger_formatter_class_mock.side_effect = [
            first_formatter,
            second_formatter,
        ]

        first_created_formatter = self.json_logger_formatter_factory.create(
            configuration=first_configuration,
        )

        second_created_formatter = self.json_logger_formatter_factory.create(
            configuration=second_configuration,
        )

        self.assertIs(
            first_created_formatter,
            first_formatter,
            ("Expected the first create() call to return the first " "JsonLoggerFormatter instance."),
        )

        self.assertIs(
            second_created_formatter,
            second_formatter,
            ("Expected the second create() call to return the second " "JsonLoggerFormatter instance."),
        )

        self.assertEqual(
            json_logger_formatter_class_mock.call_count,
            2,
            ("Expected JsonLoggerFormatter to be constructed once for " "each create() invocation."),
        )

    def test_create_returns_real_json_logger_formatter(
        self,
    ) -> None:
        """Verifies that create returns a real JsonLoggerFormatter when the constructor is not mocked."""
        configuration = JsonLoggerConfiguration()

        created_formatter = self.json_logger_formatter_factory.create(
            configuration=configuration,
        )

        self.assertIsInstance(
            created_formatter,
            JsonLoggerFormatter,
            ("Expected create() to return a real JsonLoggerFormatter " "instance when the constructor is not mocked."),
        )

    def test_create_returns_logging_formatter_compatible_instance(
        self,
    ) -> None:
        """Verifies that the created JSON logger formatter satisfies the logging.Formatter contract."""
        configuration = JsonLoggerConfiguration()

        created_formatter = self.json_logger_formatter_factory.create(
            configuration=configuration,
        )

        self.assertIsInstance(
            created_formatter,
            logging.Formatter,
            ("Expected JsonLoggerFormatterFactory to create an object " "compatible with logging.Formatter."),
        )

    def test_real_formatter_retains_supplied_configuration(
        self,
    ) -> None:
        """Verifies that the real JsonLoggerFormatter retains the exact supplied configuration instance."""
        configuration = JsonLoggerConfiguration(
            include_timestamp=False,
            include_logger_name=True,
            include_process_information=False,
            include_thread_information=True,
        )

        created_formatter = self.json_logger_formatter_factory.create(
            configuration=configuration,
        )

        self.assertIsInstance(
            created_formatter,
            JsonLoggerFormatter,
            ("Expected create() to return a JsonLoggerFormatter before " "checking its stored configuration."),
        )

        json_logger_formatter = cast(
            JsonLoggerFormatter,
            created_formatter,
        )

        self.assertIs(
            json_logger_formatter._configuration,
            configuration,
            ("Expected the real JsonLoggerFormatter to retain the exact " "JsonLoggerConfiguration instance supplied to the factory."),
        )

    def test_real_formatter_can_format_log_record(
        self,
    ) -> None:
        """Verifies that a formatter created by the factory can successfully format a logging LogRecord."""
        configuration = JsonLoggerConfiguration(
            include_timestamp=False,
            include_logger_name=False,
            include_process_information=False,
            include_thread_information=False,
        )

        created_formatter = self.json_logger_formatter_factory.create(
            configuration=configuration,
        )

        log_record = logging.LogRecord(
            name="spectralog-test",
            level=logging.INFO,
            pathname=__file__,
            lineno=100,
            msg="Application started",
            args=(),
            exc_info=None,
        )

        formatted_log_entry = created_formatter.format(
            log_record,
        )

        self.assertIsInstance(
            formatted_log_entry,
            str,
            ("Expected the formatter created by the factory to produce " "a string when formatting a LogRecord."),
        )

        self.assertIn(
            '"level": "INFO"',
            formatted_log_entry,
            ("Expected the formatted JSON output to contain the " "LogRecord level."),
        )

        self.assertIn(
            '"message": "Application started"',
            formatted_log_entry,
            ("Expected the formatted JSON output to contain the " "LogRecord message."),
        )
