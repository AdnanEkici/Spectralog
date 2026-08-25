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
from spectralog.core.protocols import LoggerFormatterFactoryProtocol  # noqa: E402
from spectralog.formatting.plain_text_file_formatter_strategy import PlainTextFileFormatterStrategy  # noqa: E402


class UnitTestPlainTextFileFormatterStrategy(unittest.TestCase):
    def setUp(self) -> None:
        self.formatter_factory = MagicMock(
            spec=LoggerFormatterFactoryProtocol,
        )

        self.plain_text_file_formatter_strategy = PlainTextFileFormatterStrategy(
            formatter_factory=self.formatter_factory,
        )

    def test_supports_returns_true_when_json_logger_configuration_is_absent(
        self,
    ) -> None:
        """Verifies that supports returns True when JSON logger configuration is not present."""
        configuration = LoggerConfiguration(
            json_logger_configuration=None,
        )

        is_supported = self.plain_text_file_formatter_strategy.supports(
            configuration=configuration,
        )

        self.assertTrue(
            is_supported,
            ("Expected supports() to return True when " "json_logger_configuration is not configured."),
        )

    def test_supports_returns_false_when_json_logger_configuration_is_present(
        self,
    ) -> None:
        """Verifies that supports returns False when JSON logger configuration is present."""
        configuration = MagicMock(
            spec=LoggerConfiguration,
        )

        configuration.json_logger_configuration = object()

        is_supported = self.plain_text_file_formatter_strategy.supports(
            configuration=configuration,
        )

        self.assertFalse(
            is_supported,
            ("Expected supports() to return False when " "json_logger_configuration is configured."),
        )

    def test_supports_does_not_call_formatter_factory(
        self,
    ) -> None:
        """Verifies that supports only inspects configuration and does not invoke the formatter factory."""
        configuration = LoggerConfiguration(
            json_logger_configuration=None,
        )

        self.plain_text_file_formatter_strategy.supports(
            configuration=configuration,
        )

        self.formatter_factory.create_file_formatter.assert_not_called()

    def test_create_requests_file_formatter_using_configuration(
        self,
    ) -> None:
        """Verifies that create delegates file formatter creation using the supplied logger configuration."""
        configuration = LoggerConfiguration(
            debug_mode=True,
            show_datetime=False,
            show_line=True,
        )

        formatter = MagicMock(
            spec=logging.Formatter,
        )

        self.formatter_factory.create_file_formatter.return_value = formatter

        self.plain_text_file_formatter_strategy.create(
            configuration=configuration,
        )

        self.formatter_factory.create_file_formatter.assert_called_once_with(
            configuration,
        )

    def test_create_returns_formatter_created_by_formatter_factory(
        self,
    ) -> None:
        """Verifies that create returns the exact formatter produced by the formatter factory."""
        configuration = LoggerConfiguration()

        formatter = MagicMock(
            spec=logging.Formatter,
        )

        self.formatter_factory.create_file_formatter.return_value = formatter

        created_formatter = self.plain_text_file_formatter_strategy.create(
            configuration=configuration,
        )

        self.assertIs(
            created_formatter,
            formatter,
            ("Expected create() to return the exact formatter instance " "produced by the formatter factory."),
        )

    def test_create_passes_same_configuration_instance(
        self,
    ) -> None:
        """Verifies that create passes the exact LoggerConfiguration instance supplied by the caller."""
        configuration = LoggerConfiguration(
            debug_mode=True,
            show_datetime=False,
            show_folder_name=True,
            show_line=True,
        )

        formatter = MagicMock(
            spec=logging.Formatter,
        )

        self.formatter_factory.create_file_formatter.return_value = formatter

        self.plain_text_file_formatter_strategy.create(
            configuration=configuration,
        )

        supplied_configuration = self.formatter_factory.create_file_formatter.call_args.args[0]

        self.assertIs(
            supplied_configuration,
            configuration,
            ("Expected the formatter factory to receive the exact " "LoggerConfiguration instance supplied to create()."),
        )

    def test_create_can_be_called_when_strategy_supports_configuration(
        self,
    ) -> None:
        """Verifies that create successfully delegates formatter creation for a supported plain-text configuration."""
        configuration = LoggerConfiguration(
            json_logger_configuration=None,
        )

        formatter = MagicMock(
            spec=logging.Formatter,
        )

        self.formatter_factory.create_file_formatter.return_value = formatter

        is_supported = self.plain_text_file_formatter_strategy.supports(
            configuration=configuration,
        )

        created_formatter = self.plain_text_file_formatter_strategy.create(
            configuration=configuration,
        )

        self.assertTrue(
            is_supported,
            ("Expected the plain-text strategy to support a configuration " "without JSON logger configuration."),
        )

        self.assertIs(
            created_formatter,
            formatter,
            ("Expected create() to return the formatter produced by the " "formatter factory for a supported configuration."),
        )

    def test_create_delegates_even_when_supports_would_return_false(
        self,
    ) -> None:
        """Verifies that create delegates directly and does not independently enforce the supports result."""
        configuration = MagicMock(
            spec=LoggerConfiguration,
        )

        configuration.json_logger_configuration = object()

        formatter = MagicMock(
            spec=logging.Formatter,
        )

        self.formatter_factory.create_file_formatter.return_value = formatter

        is_supported = self.plain_text_file_formatter_strategy.supports(
            configuration=configuration,
        )

        created_formatter = self.plain_text_file_formatter_strategy.create(
            configuration=configuration,
        )

        self.assertFalse(
            is_supported,
            ("Expected supports() to reject a configuration containing " "JSON logger configuration."),
        )

        self.assertIs(
            created_formatter,
            formatter,
            ("Expected create() to delegate directly to the formatter " "factory because support validation belongs to the resolver."),
        )

        self.formatter_factory.create_file_formatter.assert_called_once_with(
            configuration,
        )

    def test_create_can_be_called_multiple_times(
        self,
    ) -> None:
        """Verifies that repeated create calls independently delegate to the formatter factory."""
        first_configuration = LoggerConfiguration(
            debug_mode=False,
        )

        second_configuration = LoggerConfiguration(
            debug_mode=True,
        )

        first_formatter = MagicMock(
            spec=logging.Formatter,
        )

        second_formatter = MagicMock(
            spec=logging.Formatter,
        )

        self.formatter_factory.create_file_formatter.side_effect = [
            first_formatter,
            second_formatter,
        ]

        first_created_formatter = self.plain_text_file_formatter_strategy.create(
            configuration=first_configuration,
        )

        second_created_formatter = self.plain_text_file_formatter_strategy.create(
            configuration=second_configuration,
        )

        self.assertIs(
            first_created_formatter,
            first_formatter,
            ("Expected the first create() call to return the first " "formatter produced by the formatter factory."),
        )

        self.assertIs(
            second_created_formatter,
            second_formatter,
            ("Expected the second create() call to return the second " "formatter produced by the formatter factory."),
        )

        self.assertEqual(
            self.formatter_factory.create_file_formatter.call_count,
            2,
            ("Expected the formatter factory to be called once for each " "create() invocation."),
        )

    def test_create_preserves_custom_file_format_configuration(
        self,
    ) -> None:
        """Verifies that create forwards a configuration containing a custom file format without modification."""
        custom_file_format = "%(name)s :: %(levelname)s :: %(message)s"

        configuration = LoggerConfiguration(
            file_format=custom_file_format,
        )

        formatter = MagicMock(
            spec=logging.Formatter,
        )

        self.formatter_factory.create_file_formatter.return_value = formatter

        self.plain_text_file_formatter_strategy.create(
            configuration=configuration,
        )

        supplied_configuration = self.formatter_factory.create_file_formatter.call_args.args[0]

        self.assertEqual(
            supplied_configuration.file_format,
            custom_file_format,
            ("Expected create() to preserve the custom file format when " "delegating to the formatter factory."),
        )

    def test_create_preserves_date_format_configuration(
        self,
    ) -> None:
        """Verifies that create forwards the configured date format unchanged to the formatter factory."""
        custom_date_format = "%d/%m/%Y %H:%M:%S"

        configuration = LoggerConfiguration(
            date_format=custom_date_format,
        )

        formatter = MagicMock(
            spec=logging.Formatter,
        )

        self.formatter_factory.create_file_formatter.return_value = formatter

        self.plain_text_file_formatter_strategy.create(
            configuration=configuration,
        )

        supplied_configuration = self.formatter_factory.create_file_formatter.call_args.args[0]

        self.assertEqual(
            supplied_configuration.date_format,
            custom_date_format,
            ("Expected create() to preserve the configured date format " "when delegating formatter creation."),
        )

    def test_create_preserves_location_formatting_configuration(
        self,
    ) -> None:
        """Verifies that create forwards folder and line formatting options unchanged to the formatter factory."""
        configuration = LoggerConfiguration(
            show_folder_name=True,
            show_line=True,
        )

        formatter = MagicMock(
            spec=logging.Formatter,
        )

        self.formatter_factory.create_file_formatter.return_value = formatter

        self.plain_text_file_formatter_strategy.create(
            configuration=configuration,
        )

        supplied_configuration = self.formatter_factory.create_file_formatter.call_args.args[0]

        self.assertTrue(
            supplied_configuration.show_folder_name,
            ("Expected show_folder_name to remain enabled when the " "configuration is passed to the formatter factory."),
        )

        self.assertTrue(
            supplied_configuration.show_line,
            ("Expected show_line to remain enabled when the configuration " "is passed to the formatter factory."),
        )

    def test_supports_independently_evaluates_each_configuration(
        self,
    ) -> None:
        """Verifies that supports independently evaluates whether each supplied configuration uses JSON logging."""
        plain_configuration = LoggerConfiguration(
            json_logger_configuration=None,
        )

        json_configuration = MagicMock(
            spec=LoggerConfiguration,
        )

        json_configuration.json_logger_configuration = object()

        plain_is_supported = self.plain_text_file_formatter_strategy.supports(
            configuration=plain_configuration,
        )

        json_is_supported = self.plain_text_file_formatter_strategy.supports(
            configuration=json_configuration,
        )

        self.assertTrue(
            plain_is_supported,
            ("Expected a configuration without JSON logger settings to " "be supported by the plain-text strategy."),
        )

        self.assertFalse(
            json_is_supported,
            ("Expected a configuration with JSON logger settings not to " "be supported by the plain-text strategy."),
        )
