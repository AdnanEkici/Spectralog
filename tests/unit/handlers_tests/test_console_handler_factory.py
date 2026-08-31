from __future__ import annotations

import logging
import sys
import unittest
from pathlib import Path
from unittest.mock import call
from unittest.mock import MagicMock
from unittest.mock import patch

PROJECT_ROOT = Path(__file__).resolve().parents[3]  # noqa
SRC_DIR = PROJECT_ROOT / "src"  # noqa
sys.path.insert(0, str(SRC_DIR))  # noqa

from spectralog.core.log_routing import ConsoleRoutingFilter # noqa: E402
from spectralog.configuration.configuration import LoggerConfiguration  # noqa: E402
from spectralog.formatting.formatter_factory import LoggerFormatterFactory  # noqa: E402
from spectralog.formatting.relative_path_filter import RelativePathFilter  # noqa: E402
from spectralog.handlers.console_handler_factory import ConsoleHandlerFactory  # noqa: E402


class UnitTestConsoleHandlerFactory(unittest.TestCase):
    def setUp(self) -> None:
        self.formatter_factory = MagicMock(
            spec=LoggerFormatterFactory,
        )

        self.relative_path_filter = MagicMock(
            spec=RelativePathFilter,
        )

        self.console_handler_factory = ConsoleHandlerFactory(
            formatter_factory=self.formatter_factory,
            relative_path_filter=self.relative_path_filter,
        )

    @patch(
        "spectralog.handlers.console_handler_factory.logging.StreamHandler",
    )
    def test_create_returns_created_console_handler(
        self,
        stream_handler_class_mock: MagicMock,
    ) -> None:
        """Verifies that create returns the StreamHandler instance produced by the handler constructor."""
        configuration = LoggerConfiguration()

        formatter = MagicMock(
            spec=logging.Formatter,
        )

        console_handler = MagicMock()

        self.formatter_factory.create_console_formatter.return_value = formatter
        stream_handler_class_mock.return_value = console_handler

        created_handler = self.console_handler_factory.create(
            configuration=configuration,
        )

        self.assertIs(
            created_handler,
            console_handler,
            ("Expected create() to return the same StreamHandler instance " "created by logging.StreamHandler."),
        )

    @patch(
        "spectralog.handlers.console_handler_factory.logging.StreamHandler",
    )
    def test_create_requests_console_formatter_with_configuration(
        self,
        stream_handler_class_mock: MagicMock,
    ) -> None:
        """Verifies that create requests a console formatter using the supplied logger configuration."""
        configuration = LoggerConfiguration(
            debug_mode=True,
        )

        formatter = MagicMock(
            spec=logging.Formatter,
        )

        self.formatter_factory.create_console_formatter.return_value = formatter
        stream_handler_class_mock.return_value = MagicMock()

        self.console_handler_factory.create(
            configuration=configuration,
        )

        self.formatter_factory.create_console_formatter.assert_called_once_with(
            configuration,
        )

    @patch(
        "spectralog.handlers.console_handler_factory.logging.StreamHandler",
    )
    def test_create_constructs_stream_handler_without_arguments(
        self,
        stream_handler_class_mock: MagicMock,
    ) -> None:
        """Verifies that create constructs the default StreamHandler without supplying a custom output stream."""
        configuration = LoggerConfiguration()

        self.formatter_factory.create_console_formatter.return_value = MagicMock(
            spec=logging.Formatter,
        )

        stream_handler_class_mock.return_value = MagicMock()

        self.console_handler_factory.create(
            configuration=configuration,
        )

        stream_handler_class_mock.assert_called_once_with()

    @patch(
        "spectralog.handlers.console_handler_factory.logging.StreamHandler",
    )
    def test_create_sets_info_level_when_debug_mode_is_disabled(
        self,
        stream_handler_class_mock: MagicMock,
    ) -> None:
        """Verifies that create configures the console handler at INFO level when debug mode is disabled."""
        configuration = LoggerConfiguration(
            debug_mode=False,
        )

        console_handler = MagicMock()

        self.formatter_factory.create_console_formatter.return_value = MagicMock(
            spec=logging.Formatter,
        )

        stream_handler_class_mock.return_value = console_handler

        self.console_handler_factory.create(
            configuration=configuration,
        )

        console_handler.setLevel.assert_called_once_with(
            logging.INFO,
        )

    @patch(
        "spectralog.handlers.console_handler_factory.logging.StreamHandler",
    )
    def test_create_sets_debug_level_when_debug_mode_is_enabled(
        self,
        stream_handler_class_mock: MagicMock,
    ) -> None:
        """Verifies that create configures the console handler at DEBUG level when debug mode is enabled."""
        configuration = LoggerConfiguration(
            debug_mode=True,
        )

        console_handler = MagicMock()

        self.formatter_factory.create_console_formatter.return_value = MagicMock(
            spec=logging.Formatter,
        )

        stream_handler_class_mock.return_value = console_handler

        self.console_handler_factory.create(
            configuration=configuration,
        )

        console_handler.setLevel.assert_called_once_with(
            logging.DEBUG,
        )

    @patch(
        "spectralog.handlers.console_handler_factory.logging.StreamHandler",
    )
    def test_create_assigns_formatter_returned_by_formatter_factory(
        self,
        stream_handler_class_mock: MagicMock,
    ) -> None:
        """Verifies that create assigns the formatter returned by the formatter factory to the console handler."""
        configuration = LoggerConfiguration()

        formatter = MagicMock(
            spec=logging.Formatter,
        )

        console_handler = MagicMock()

        self.formatter_factory.create_console_formatter.return_value = formatter
        stream_handler_class_mock.return_value = console_handler

        self.console_handler_factory.create(
            configuration=configuration,
        )

        console_handler.setFormatter.assert_called_once_with(
            formatter,
        )

    @patch(
        "spectralog.handlers.console_handler_factory.logging.StreamHandler",
    )
    def test_create_adds_relative_path_filter(
        self,
        stream_handler_class_mock: MagicMock,
    ) -> None:
        """Verifies that create attaches the supplied RelativePathFilter to the console handler."""
        configuration = LoggerConfiguration()

        console_handler = MagicMock()

        self.formatter_factory.create_console_formatter.return_value = MagicMock(
            spec=logging.Formatter,
        )

        stream_handler_class_mock.return_value = console_handler

        self.console_handler_factory.create(
            configuration=configuration,
        )

        self.assertEqual(
        console_handler.addFilter.call_count,
        2,
        (
            "Expected the console handler to receive both the relative-path "
            "filter and the console-routing filter."
        ),
        )

        console_handler.addFilter.assert_any_call(
            self.relative_path_filter,
        )

    @patch(
    "spectralog.handlers.console_handler_factory.logging.StreamHandler",
    )
    def test_create_configures_handler_in_expected_order(
        self,
        stream_handler_class_mock: MagicMock,
    ) -> None:
        """Verifies that create configures the console handler in the expected order."""
        configuration = LoggerConfiguration(
            debug_mode=True,
        )

        formatter = MagicMock(
            spec=logging.Formatter,
        )

        console_handler = MagicMock()

        self.formatter_factory.create_console_formatter.return_value = formatter
        stream_handler_class_mock.return_value = console_handler

        self.console_handler_factory.create(
            configuration=configuration,
        )

        self.assertEqual(
            len(
                console_handler.method_calls,
            ),
            4,
            (
                "Expected the console handler to receive four configuration "
                "calls."
            ),
        )

        self.assertEqual(
            console_handler.method_calls[0],
            call.setLevel(
                logging.DEBUG,
            ),
            "Expected setLevel() to be called first.",
        )

        self.assertEqual(
            console_handler.method_calls[1],
            call.setFormatter(
                formatter,
            ),
            "Expected setFormatter() to be called second.",
        )

        self.assertEqual(
            console_handler.method_calls[2],
            call.addFilter(
                self.relative_path_filter,
            ),
            "Expected RelativePathFilter to be added third.",
        )

        routing_filter = console_handler.method_calls[3].args[0]

        self.assertIsInstance(
            routing_filter,
            ConsoleRoutingFilter,
            "Expected ConsoleRoutingFilter to be added last.",
        )

    @patch(
        "spectralog.handlers.console_handler_factory.logging.StreamHandler",
    )
    def test_create_uses_configuration_log_level_property(
        self,
        stream_handler_class_mock: MagicMock,
    ) -> None:
        """Verifies that create uses the logger configuration's resolved log level rather than defining its own level policy."""
        configuration = MagicMock(
            spec=LoggerConfiguration,
        )

        configuration.log_level = logging.ERROR

        formatter = MagicMock(
            spec=logging.Formatter,
        )

        console_handler = MagicMock()

        self.formatter_factory.create_console_formatter.return_value = formatter
        stream_handler_class_mock.return_value = console_handler

        self.console_handler_factory.create(
            configuration=configuration,
        )

        console_handler.setLevel.assert_called_once_with(
            logging.ERROR,
        )

    @patch(
        "spectralog.handlers.console_handler_factory.logging.StreamHandler",
    )
    def test_create_uses_same_configuration_for_formatter_and_handler_level(
        self,
        stream_handler_class_mock: MagicMock,
    ) -> None:
        """Verifies that the same logger configuration determines both formatter creation and the console handler level."""
        configuration = LoggerConfiguration(
            debug_mode=True,
            show_datetime=False,
            show_line=True,
        )

        formatter = MagicMock(
            spec=logging.Formatter,
        )

        console_handler = MagicMock()

        self.formatter_factory.create_console_formatter.return_value = formatter
        stream_handler_class_mock.return_value = console_handler

        self.console_handler_factory.create(
            configuration=configuration,
        )

        self.formatter_factory.create_console_formatter.assert_called_once_with(
            configuration,
        )

        console_handler.setLevel.assert_called_once_with(
            configuration.log_level,
        )

    def test_create_returns_real_stream_handler_when_dependencies_are_real(
        self,
    ) -> None:
        """Verifies that create produces a real StreamHandler with the expected level, formatter, and relative path filter."""
        configuration = LoggerConfiguration(
            debug_mode=True,
        )

        formatter_factory = MagicMock(
            spec=LoggerFormatterFactory,
        )

        formatter = logging.Formatter(
            "%(levelname)s | %(message)s",
        )

        formatter_factory.create_console_formatter.return_value = formatter

        relative_path_filter = RelativePathFilter()

        console_handler_factory = ConsoleHandlerFactory(
            formatter_factory=formatter_factory,
            relative_path_filter=relative_path_filter,
        )

        created_handler = console_handler_factory.create(
            configuration=configuration,
        )

        self.assertIsInstance(
            created_handler,
            logging.StreamHandler,
            ("Expected create() to return a real logging.StreamHandler " "when StreamHandler is not mocked."),
        )

        self.assertEqual(
            created_handler.level,
            logging.DEBUG,
            ("Expected the real console handler to use DEBUG level when " "debug mode is enabled."),
        )

        self.assertIs(
            created_handler.formatter,
            formatter,
            ("Expected the real console handler to retain the formatter " "returned by the formatter factory."),
        )

        self.assertIn(
            relative_path_filter,
            created_handler.filters,
            ("Expected the real console handler to contain the supplied " "RelativePathFilter."),
        )

        created_handler.close()
