from __future__ import annotations

import logging
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock

PROJECT_ROOT = Path(__file__).resolve().parents[3]  # noqa
SRC_DIR = PROJECT_ROOT / "src"  # noqa
sys.path.insert(0, str(SRC_DIR))  # noqa

from spectralog.configuration.configuration import LoggerConfiguration  # noqa: E402
from spectralog.configuration.json_logger_configuration import JsonLoggerConfiguration  # noqa: E402
from spectralog.core.protocols import JsonLoggerFormatterFactoryProtocol  # noqa: E402
from spectralog.formatting.json_file_formatter_strategy import JsonFileFormatterStrategy  # noqa: E402


class UnitTestJsonFileFormatterStrategy(unittest.TestCase):
    def setUp(self) -> None:
        self.json_formatter_factory = MagicMock(
            spec=JsonLoggerFormatterFactoryProtocol,
        )

        self.json_file_formatter_strategy = JsonFileFormatterStrategy(
            json_formatter_factory=self.json_formatter_factory,
        )

    def test_supports_returns_true_when_json_logger_configuration_is_present(
        self,
    ) -> None:
        """Verifies that supports returns True when JSON logger configuration is present."""
        configuration = LoggerConfiguration(
            json_logger_configuration=JsonLoggerConfiguration(),
        )

        is_supported = self.json_file_formatter_strategy.supports(
            configuration=configuration,
        )

        self.assertTrue(
            is_supported,
            ("Expected supports() to return True when " "json_logger_configuration is configured."),
        )

    def test_supports_returns_false_when_json_logger_configuration_is_absent(
        self,
    ) -> None:
        """Verifies that supports returns False when JSON logger configuration is absent."""
        configuration = LoggerConfiguration(
            json_logger_configuration=None,
        )

        is_supported = self.json_file_formatter_strategy.supports(
            configuration=configuration,
        )

        self.assertFalse(
            is_supported,
            ("Expected supports() to return False when " "json_logger_configuration is not configured."),
        )

    def test_supports_does_not_call_json_formatter_factory(
        self,
    ) -> None:
        """Verifies that supports only inspects configuration and does not invoke the JSON formatter factory."""
        configuration = LoggerConfiguration(
            json_logger_configuration=JsonLoggerConfiguration(),
        )

        self.json_file_formatter_strategy.supports(
            configuration=configuration,
        )

        self.json_formatter_factory.create.assert_not_called()

    def test_create_passes_json_logger_configuration_to_factory(
        self,
    ) -> None:
        """Verifies that create passes the configured JsonLoggerConfiguration to the JSON formatter factory."""
        json_logger_configuration = JsonLoggerConfiguration(
            include_timestamp=False,
            include_logger_name=False,
            include_process_information=False,
            include_thread_information=False,
        )

        configuration = LoggerConfiguration(
            json_logger_configuration=json_logger_configuration,
        )

        formatter = MagicMock(
            spec=logging.Formatter,
        )

        self.json_formatter_factory.create.return_value = formatter

        self.json_file_formatter_strategy.create(
            configuration=configuration,
        )

        self.json_formatter_factory.create.assert_called_once_with(
            configuration=json_logger_configuration,
        )

    def test_create_returns_formatter_created_by_json_formatter_factory(
        self,
    ) -> None:
        """Verifies that create returns the formatter produced by the JSON formatter factory."""
        configuration = LoggerConfiguration(
            json_logger_configuration=JsonLoggerConfiguration(),
        )

        formatter = MagicMock(
            spec=logging.Formatter,
        )

        self.json_formatter_factory.create.return_value = formatter

        created_formatter = self.json_file_formatter_strategy.create(
            configuration=configuration,
        )

        self.assertIs(
            created_formatter,
            formatter,
            ("Expected create() to return the exact formatter instance " "produced by the JSON formatter factory."),
        )

    def test_create_raises_value_error_when_json_logger_configuration_is_absent(
        self,
    ) -> None:
        """Verifies that create raises ValueError when JSON logger configuration is not available."""
        configuration = LoggerConfiguration(
            json_logger_configuration=None,
        )

        with self.assertRaisesRegex(
            ValueError,
            ("JSON logger configuration is required " "for JSON file formatting."),
            msg=("Expected create() to raise ValueError when " "json_logger_configuration is missing."),
        ):
            self.json_file_formatter_strategy.create(
                configuration=configuration,
            )

    def test_create_does_not_call_factory_when_json_logger_configuration_is_absent(
        self,
    ) -> None:
        """Verifies that create does not invoke the JSON formatter factory when required configuration is missing."""
        configuration = LoggerConfiguration(
            json_logger_configuration=None,
        )

        with self.assertRaises(
            ValueError,
            msg=("Expected create() to raise ValueError when JSON logger " "configuration is missing."),
        ):
            self.json_file_formatter_strategy.create(
                configuration=configuration,
            )

        self.json_formatter_factory.create.assert_not_called()

    def test_create_passes_same_json_logger_configuration_instance(
        self,
    ) -> None:
        """Verifies that create passes the exact JsonLoggerConfiguration instance stored in LoggerConfiguration."""
        json_logger_configuration = JsonLoggerConfiguration()

        configuration = LoggerConfiguration(
            json_logger_configuration=json_logger_configuration,
        )

        formatter = MagicMock(
            spec=logging.Formatter,
        )

        self.json_formatter_factory.create.return_value = formatter

        self.json_file_formatter_strategy.create(
            configuration=configuration,
        )

        supplied_configuration = self.json_formatter_factory.create.call_args.kwargs["configuration"]

        self.assertIs(
            supplied_configuration,
            json_logger_configuration,
            ("Expected the JSON formatter factory to receive the exact " "JsonLoggerConfiguration instance stored in LoggerConfiguration."),
        )

    def test_create_supports_custom_json_configuration_values(
        self,
    ) -> None:
        """Verifies that create preserves all custom JSON logger configuration values passed to the formatter factory."""
        json_logger_configuration = JsonLoggerConfiguration(
            include_timestamp=False,
            include_logger_name=True,
            include_process_information=False,
            include_thread_information=True,
        )

        configuration = LoggerConfiguration(
            json_logger_configuration=json_logger_configuration,
        )

        formatter = MagicMock(
            spec=logging.Formatter,
        )

        self.json_formatter_factory.create.return_value = formatter

        self.json_file_formatter_strategy.create(
            configuration=configuration,
        )

        supplied_configuration = self.json_formatter_factory.create.call_args.kwargs["configuration"]

        self.assertEqual(
            supplied_configuration.include_timestamp,
            False,
            ("Expected include_timestamp to remain False when passed " "through the strategy."),
        )

        self.assertEqual(
            supplied_configuration.include_logger_name,
            True,
            ("Expected include_logger_name to remain True when passed " "through the strategy."),
        )

        self.assertEqual(
            supplied_configuration.include_process_information,
            False,
            ("Expected include_process_information to remain False when " "passed through the strategy."),
        )

        self.assertEqual(
            supplied_configuration.include_thread_information,
            True,
            ("Expected include_thread_information to remain True when " "passed through the strategy."),
        )

    def test_supports_result_changes_with_configuration(
        self,
    ) -> None:
        """Verifies that supports independently evaluates each supplied logger configuration."""
        json_configuration = LoggerConfiguration(
            json_logger_configuration=JsonLoggerConfiguration(),
        )

        plain_configuration = LoggerConfiguration(
            json_logger_configuration=None,
        )

        json_is_supported = self.json_file_formatter_strategy.supports(
            configuration=json_configuration,
        )

        plain_is_supported = self.json_file_formatter_strategy.supports(
            configuration=plain_configuration,
        )

        self.assertTrue(
            json_is_supported,
            ("Expected a configuration containing JSON logger settings " "to be supported."),
        )

        self.assertFalse(
            plain_is_supported,
            ("Expected a configuration without JSON logger settings " "not to be supported."),
        )

    def test_create_can_be_called_multiple_times(
        self,
    ) -> None:
        """Verifies that create delegates independently to the JSON formatter factory on repeated calls."""
        first_json_logger_configuration = JsonLoggerConfiguration(
            include_timestamp=True,
        )

        second_json_logger_configuration = JsonLoggerConfiguration(
            include_timestamp=False,
        )

        first_configuration = LoggerConfiguration(
            json_logger_configuration=first_json_logger_configuration,
        )

        second_configuration = LoggerConfiguration(
            json_logger_configuration=second_json_logger_configuration,
        )

        first_formatter = MagicMock(
            spec=logging.Formatter,
        )

        second_formatter = MagicMock(
            spec=logging.Formatter,
        )

        self.json_formatter_factory.create.side_effect = [
            first_formatter,
            second_formatter,
        ]

        first_created_formatter = self.json_file_formatter_strategy.create(
            configuration=first_configuration,
        )

        second_created_formatter = self.json_file_formatter_strategy.create(
            configuration=second_configuration,
        )

        self.assertIs(
            first_created_formatter,
            first_formatter,
            ("Expected the first create() call to return the first " "formatter produced by the factory."),
        )

        self.assertIs(
            second_created_formatter,
            second_formatter,
            ("Expected the second create() call to return the second " "formatter produced by the factory."),
        )

        self.assertEqual(
            self.json_formatter_factory.create.call_count,
            2,
            ("Expected the JSON formatter factory to be invoked once " "for each create() call."),
        )

    def test_create_does_not_modify_logger_configuration(
        self,
    ) -> None:
        """Verifies that create does not replace or mutate the JSON logger configuration stored on LoggerConfiguration."""
        json_logger_configuration = JsonLoggerConfiguration()

        configuration = LoggerConfiguration(
            json_logger_configuration=json_logger_configuration,
        )

        formatter = MagicMock(
            spec=logging.Formatter,
        )

        self.json_formatter_factory.create.return_value = formatter

        self.json_file_formatter_strategy.create(
            configuration=configuration,
        )

        self.assertIs(
            configuration.json_logger_configuration,
            json_logger_configuration,
            ("Expected create() to leave the original JSON logger " "configuration instance unchanged."),
        )
