from __future__ import annotations

import logging
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock
from unittest.mock import patch

import colorlog

PROJECT_ROOT = Path(__file__).resolve().parents[3]  # noqa
SRC_DIR = PROJECT_ROOT / "src"  # noqa
sys.path.insert(0, str(SRC_DIR))  # noqa

from spectralog.configuration.configuration import LoggerConfiguration  # noqa: E402
from spectralog.formatting.format_builder import LogFormatBuilder  # noqa: E402
from spectralog.formatting.formatter_factory import LoggerFormatterFactory  # noqa: E402
from spectralog.levels.log_level_registry import LogLevelRegistry  # noqa: E402


class UnitTestLoggerFormatterFactory(unittest.TestCase):
    def setUp(self) -> None:
        self.format_builder = MagicMock(
            spec=LogFormatBuilder,
        )

        self.log_level_registry = MagicMock(
            spec=LogLevelRegistry,
        )

        self.logger_formatter_factory = LoggerFormatterFactory(
            format_builder=self.format_builder,
            log_level_registry=self.log_level_registry,
        )

    @patch(
        "spectralog.formatting.formatter_factory.colorlog.ColoredFormatter",
    )
    def test_create_console_formatter_requests_console_format_from_builder(
        self,
        colored_formatter_class_mock: MagicMock,
    ) -> None:
        """Verifies that create_console_formatter requests the console format using the supplied logger configuration."""
        configuration = LoggerConfiguration()

        console_format = "%(levelname)s | %(message)s"

        self.format_builder.build_console_format.return_value = console_format

        colored_formatter_class_mock.return_value = MagicMock()

        self.logger_formatter_factory.create_console_formatter(
            configuration=configuration,
        )

        self.format_builder.build_console_format.assert_called_once_with(
            configuration,
        )

    @patch(
        "spectralog.formatting.formatter_factory.colorlog.ColoredFormatter",
    )
    def test_create_console_formatter_constructs_colored_formatter_with_expected_format(
        self,
        colored_formatter_class_mock: MagicMock,
    ) -> None:
        """Verifies that create_console_formatter passes the generated console format to ColoredFormatter."""
        configuration = LoggerConfiguration()

        console_format = "%(log_color)s%(levelname)s | %(message)s%(reset)s"

        self.format_builder.build_console_format.return_value = console_format
        self.log_level_registry.colors = {
            "INFO": "green",
        }

        colored_formatter_class_mock.return_value = MagicMock()

        self.logger_formatter_factory.create_console_formatter(
            configuration=configuration,
        )

        colored_formatter_class_mock.assert_called_once_with(
            fmt=console_format,
            datefmt=configuration.date_format,
            log_colors=self.log_level_registry.colors,
            reset=True,
        )

    @patch(
        "spectralog.formatting.formatter_factory.colorlog.ColoredFormatter",
    )
    def test_create_console_formatter_uses_configured_date_format(
        self,
        colored_formatter_class_mock: MagicMock,
    ) -> None:
        """Verifies that create_console_formatter passes the configured date format to ColoredFormatter."""
        configuration = LoggerConfiguration(
            date_format="%d/%m/%Y %H:%M:%S",
        )

        console_format = "%(message)s"

        self.format_builder.build_console_format.return_value = console_format

        self.log_level_registry.colors = {
            "INFO": "green",
        }

        colored_formatter_class_mock.return_value = MagicMock()

        self.logger_formatter_factory.create_console_formatter(
            configuration=configuration,
        )

        colored_formatter_class_mock.assert_called_once_with(
            fmt=console_format,
            datefmt="%d/%m/%Y %H:%M:%S",
            log_colors=self.log_level_registry.colors,
            reset=True,
        )

    @patch(
        "spectralog.formatting.formatter_factory.colorlog.ColoredFormatter",
    )
    def test_create_console_formatter_uses_log_level_registry_colors(
        self,
        colored_formatter_class_mock: MagicMock,
    ) -> None:
        """Verifies that create_console_formatter passes the log level registry color mapping to ColoredFormatter."""
        configuration = LoggerConfiguration()

        console_format = "%(message)s"

        log_colors = {
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "bold_yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        }

        self.format_builder.build_console_format.return_value = console_format
        self.log_level_registry.colors = log_colors

        colored_formatter_class_mock.return_value = MagicMock()

        self.logger_formatter_factory.create_console_formatter(
            configuration=configuration,
        )

        colored_formatter_class_mock.assert_called_once_with(
            fmt=console_format,
            datefmt=configuration.date_format,
            log_colors=log_colors,
            reset=True,
        )

    @patch(
        "spectralog.formatting.formatter_factory.colorlog.ColoredFormatter",
    )
    def test_create_console_formatter_enables_color_reset(
        self,
        colored_formatter_class_mock: MagicMock,
    ) -> None:
        """Verifies that create_console_formatter enables automatic color reset on ColoredFormatter."""
        configuration = LoggerConfiguration()

        console_format = "%(message)s"

        self.format_builder.build_console_format.return_value = console_format

        self.log_level_registry.colors = {
            "INFO": "green",
        }

        colored_formatter_class_mock.return_value = MagicMock()

        self.logger_formatter_factory.create_console_formatter(
            configuration=configuration,
        )

        colored_formatter_class_mock.assert_called_once_with(
            fmt=console_format,
            datefmt=configuration.date_format,
            log_colors=self.log_level_registry.colors,
            reset=True,
        )

    @patch(
        "spectralog.formatting.formatter_factory.colorlog.ColoredFormatter",
    )
    def test_create_console_formatter_returns_created_colored_formatter(
        self,
        colored_formatter_class_mock: MagicMock,
    ) -> None:
        """Verifies that create_console_formatter returns the ColoredFormatter instance produced by the constructor."""
        configuration = LoggerConfiguration()

        console_format = "%(message)s"

        self.format_builder.build_console_format.return_value = console_format

        self.log_level_registry.colors = {
            "INFO": "green",
        }

        colored_formatter = MagicMock()

        colored_formatter_class_mock.return_value = colored_formatter

        created_formatter = self.logger_formatter_factory.create_console_formatter(
            configuration=configuration,
        )

        self.assertIs(
            created_formatter,
            colored_formatter,
            ("Expected create_console_formatter() to return the same " "ColoredFormatter instance created by colorlog.ColoredFormatter."),
        )

    @patch(
        "spectralog.formatting.formatter_factory.logging.Formatter",
    )
    def test_create_file_formatter_requests_file_format_from_builder(
        self,
        formatter_class_mock: MagicMock,
    ) -> None:
        """Verifies that create_file_formatter requests the file format using the supplied logger configuration."""
        configuration = LoggerConfiguration()

        file_format = "%(levelname)s | %(message)s"

        self.format_builder.build_file_format.return_value = file_format

        formatter_class_mock.return_value = MagicMock()

        self.logger_formatter_factory.create_file_formatter(
            configuration=configuration,
        )

        self.format_builder.build_file_format.assert_called_once_with(
            configuration,
        )

    @patch(
        "spectralog.formatting.formatter_factory.logging.Formatter",
    )
    def test_create_file_formatter_constructs_formatter_with_expected_format(
        self,
        formatter_class_mock: MagicMock,
    ) -> None:
        """Verifies that create_file_formatter passes the generated file format to logging.Formatter."""
        configuration = LoggerConfiguration()

        file_format = "%(asctime)s | %(levelname)s | %(message)s"

        self.format_builder.build_file_format.return_value = file_format

        formatter_class_mock.return_value = MagicMock()

        self.logger_formatter_factory.create_file_formatter(
            configuration=configuration,
        )

        formatter_class_mock.assert_called_once_with(
            fmt=file_format,
            datefmt=configuration.date_format,
        )

    @patch(
        "spectralog.formatting.formatter_factory.logging.Formatter",
    )
    def test_create_file_formatter_uses_configured_date_format(
        self,
        formatter_class_mock: MagicMock,
    ) -> None:
        """Verifies that create_file_formatter passes the configured date format to logging.Formatter."""
        configuration = LoggerConfiguration(
            date_format="%d/%m/%Y %H:%M:%S",
        )

        file_format = "%(message)s"

        self.format_builder.build_file_format.return_value = file_format

        formatter_class_mock.return_value = MagicMock()

        self.logger_formatter_factory.create_file_formatter(
            configuration=configuration,
        )

        formatter_class_mock.assert_called_once_with(
            fmt=file_format,
            datefmt="%d/%m/%Y %H:%M:%S",
        )

    @patch(
        "spectralog.formatting.formatter_factory.logging.Formatter",
    )
    def test_create_file_formatter_returns_created_formatter(
        self,
        formatter_class_mock: MagicMock,
    ) -> None:
        """Verifies that create_file_formatter returns the logging Formatter instance produced by the constructor."""
        configuration = LoggerConfiguration()

        file_format = "%(message)s"

        self.format_builder.build_file_format.return_value = file_format

        formatter = MagicMock()

        formatter_class_mock.return_value = formatter

        created_formatter = self.logger_formatter_factory.create_file_formatter(
            configuration=configuration,
        )

        self.assertIs(
            created_formatter,
            formatter,
            ("Expected create_file_formatter() to return the same " "Formatter instance created by logging.Formatter."),
        )

    def test_create_console_formatter_returns_real_colored_formatter(
        self,
    ) -> None:
        """Verifies that create_console_formatter produces a real ColoredFormatter when dependencies are not mocked."""
        configuration = LoggerConfiguration()

        format_builder = MagicMock(
            spec=LogFormatBuilder,
        )

        console_format = "%(log_color)s%(levelname)s | %(message)s%(reset)s"

        format_builder.build_console_format.return_value = console_format

        log_level_registry = MagicMock(
            spec=LogLevelRegistry,
        )

        log_level_registry.colors = {
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "bold_yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        }

        logger_formatter_factory = LoggerFormatterFactory(
            format_builder=format_builder,
            log_level_registry=log_level_registry,
        )

        created_formatter = logger_formatter_factory.create_console_formatter(
            configuration=configuration,
        )

        self.assertIsInstance(
            created_formatter,
            colorlog.ColoredFormatter,
            ("Expected create_console_formatter() to return a real " "colorlog.ColoredFormatter instance."),
        )

    def test_create_file_formatter_returns_real_logging_formatter(
        self,
    ) -> None:
        """Verifies that create_file_formatter produces a real logging Formatter when dependencies are not mocked."""
        configuration = LoggerConfiguration()

        format_builder = MagicMock(
            spec=LogFormatBuilder,
        )

        file_format = "%(levelname)s | %(message)s"

        format_builder.build_file_format.return_value = file_format

        log_level_registry = MagicMock(
            spec=LogLevelRegistry,
        )

        logger_formatter_factory = LoggerFormatterFactory(
            format_builder=format_builder,
            log_level_registry=log_level_registry,
        )

        created_formatter = logger_formatter_factory.create_file_formatter(
            configuration=configuration,
        )

        self.assertIsInstance(
            created_formatter,
            logging.Formatter,
            ("Expected create_file_formatter() to return a real " "logging.Formatter instance."),
        )

    def test_real_console_formatter_formats_log_record_with_configured_color_mapping(
        self,
    ) -> None:
        """Verifies that a real console formatter can format a log record using the configured log level color mapping."""
        configuration = LoggerConfiguration(
            show_datetime=False,
        )

        format_builder = LogFormatBuilder()

        log_level_registry = LogLevelRegistry()

        logger_formatter_factory = LoggerFormatterFactory(
            format_builder=format_builder,
            log_level_registry=log_level_registry,
        )

        formatter = logger_formatter_factory.create_console_formatter(
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

        formatted_message = formatter.format(
            log_record,
        )

        self.assertIn(
            "INFO",
            formatted_message,
            ("Expected the real console formatter output to contain the " "logging level."),
        )

        self.assertIn(
            "Application started",
            formatted_message,
            ("Expected the real console formatter output to contain the " "log message."),
        )

    def test_real_file_formatter_formats_log_record_without_color_placeholders(
        self,
    ) -> None:
        """Verifies that a real file formatter produces plain text output without console color placeholders."""
        configuration = LoggerConfiguration(
            show_datetime=False,
        )

        format_builder = LogFormatBuilder()

        log_level_registry = LogLevelRegistry()

        logger_formatter_factory = LoggerFormatterFactory(
            format_builder=format_builder,
            log_level_registry=log_level_registry,
        )

        formatter = logger_formatter_factory.create_file_formatter(
            configuration=configuration,
        )

        log_record = logging.LogRecord(
            name="spectralog-test",
            level=logging.WARNING,
            pathname=__file__,
            lineno=100,
            msg="Warning message",
            args=(),
            exc_info=None,
        )

        formatted_message = formatter.format(
            log_record,
        )

        self.assertEqual(
            formatted_message,
            "WARNING | Warning message",
            ("Expected the real file formatter to produce the configured " "plain-text logging format."),
        )

        self.assertNotIn(
            "%(log_color)s",
            formatted_message,
            ("Expected the real file formatter output not to contain the " "log_color placeholder."),
        )

        self.assertNotIn(
            "%(reset)s",
            formatted_message,
            ("Expected the real file formatter output not to contain the " "reset placeholder."),
        )

    def test_console_and_file_formatter_use_same_date_format_configuration(
        self,
    ) -> None:
        """Verifies that console and file formatter creation both use the same date format from the logger configuration."""
        configuration = LoggerConfiguration(
            date_format="%Y/%m/%d-%H:%M:%S",
        )

        format_builder = LogFormatBuilder()

        log_level_registry = LogLevelRegistry()

        logger_formatter_factory = LoggerFormatterFactory(
            format_builder=format_builder,
            log_level_registry=log_level_registry,
        )

        console_formatter = logger_formatter_factory.create_console_formatter(
            configuration=configuration,
        )

        file_formatter = logger_formatter_factory.create_file_formatter(
            configuration=configuration,
        )

        self.assertEqual(
            console_formatter.datefmt,
            configuration.date_format,
            ("Expected the console formatter date format to match the " "logger configuration."),
        )

        self.assertEqual(
            file_formatter.datefmt,
            configuration.date_format,
            ("Expected the file formatter date format to match the " "logger configuration."),
        )
