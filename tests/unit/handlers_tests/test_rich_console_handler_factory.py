from __future__ import annotations

import logging
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock
from unittest.mock import patch

from rich.logging import RichHandler


PROJECT_ROOT = Path(__file__).resolve().parents[3]  # noqa
SRC_DIR = PROJECT_ROOT / "src"  # noqa
sys.path.insert(0, str(SRC_DIR))  # noqa


from spectralog.configuration.configuration import LoggerConfiguration  # noqa: E402
from spectralog.configuration.rich_console_configuration import RichConsoleConfiguration  # noqa: E402
from spectralog.handlers.rich_console_handler_factory import RichConsoleHandlerFactory  # noqa: E402


class UnitTestRichConsoleHandlerFactory(unittest.TestCase):
    def setUp(self) -> None:
        self.rich_console_handler_factory = RichConsoleHandlerFactory()

    @patch(
        "spectralog.handlers.rich_console_handler_factory.RichHandler",
    )
    def test_create_returns_created_rich_handler(
        self,
        rich_handler_class_mock: MagicMock,
    ) -> None:
        """Verifies that create returns the RichHandler instance created by the handler constructor."""
        logger_configuration = LoggerConfiguration()

        rich_configuration = RichConsoleConfiguration()

        rich_handler = MagicMock(
            spec=RichHandler,
        )

        rich_handler_class_mock.return_value = rich_handler

        created_handler = self.rich_console_handler_factory.create(
            logger_configuration=logger_configuration,
            rich_configuration=rich_configuration,
        )

        self.assertIs(
            created_handler,
            rich_handler,
            ("Expected create() to return the same RichHandler instance " "created by the RichHandler constructor."),
        )

    @patch(
        "spectralog.handlers.rich_console_handler_factory.RichHandler",
    )
    def test_create_constructs_rich_handler_with_logger_level(
        self,
        rich_handler_class_mock: MagicMock,
    ) -> None:
        """Verifies that create passes the logger configuration level to the RichHandler constructor."""
        logger_configuration = LoggerConfiguration(
            debug_mode=True,
        )

        rich_configuration = RichConsoleConfiguration()

        rich_handler_class_mock.return_value = MagicMock(
            spec=RichHandler,
        )

        self.rich_console_handler_factory.create(
            logger_configuration=logger_configuration,
            rich_configuration=rich_configuration,
        )

        rich_handler_class_mock.assert_called_once_with(
            level=logging.DEBUG,
            show_time=rich_configuration.show_time,
            show_level=rich_configuration.show_level,
            show_path=rich_configuration.show_path,
            rich_tracebacks=rich_configuration.rich_tracebacks,
            markup=rich_configuration.markup,
        )

    @patch(
        "spectralog.handlers.rich_console_handler_factory.RichHandler",
    )
    def test_create_uses_info_level_when_debug_mode_is_disabled(
        self,
        rich_handler_class_mock: MagicMock,
    ) -> None:
        """Verifies that create configures RichHandler at INFO level when debug mode is disabled."""
        logger_configuration = LoggerConfiguration(
            debug_mode=False,
        )

        rich_configuration = RichConsoleConfiguration()

        rich_handler_class_mock.return_value = MagicMock(
            spec=RichHandler,
        )

        self.rich_console_handler_factory.create(
            logger_configuration=logger_configuration,
            rich_configuration=rich_configuration,
        )

        rich_handler_class_mock.assert_called_once_with(
            level=logging.INFO,
            show_time=rich_configuration.show_time,
            show_level=rich_configuration.show_level,
            show_path=rich_configuration.show_path,
            rich_tracebacks=rich_configuration.rich_tracebacks,
            markup=rich_configuration.markup,
        )

    @patch(
        "spectralog.handlers.rich_console_handler_factory.RichHandler",
    )
    def test_create_passes_show_time_configuration(
        self,
        rich_handler_class_mock: MagicMock,
    ) -> None:
        """Verifies that create passes the configured show_time value to the RichHandler constructor."""
        logger_configuration = LoggerConfiguration()

        rich_configuration = RichConsoleConfiguration(
            show_time=False,
        )

        rich_handler_class_mock.return_value = MagicMock(
            spec=RichHandler,
        )

        self.rich_console_handler_factory.create(
            logger_configuration=logger_configuration,
            rich_configuration=rich_configuration,
        )

        rich_handler_class_mock.assert_called_once_with(
            level=logger_configuration.log_level,
            show_time=False,
            show_level=rich_configuration.show_level,
            show_path=rich_configuration.show_path,
            rich_tracebacks=rich_configuration.rich_tracebacks,
            markup=rich_configuration.markup,
        )

    @patch(
        "spectralog.handlers.rich_console_handler_factory.RichHandler",
    )
    def test_create_passes_show_level_configuration(
        self,
        rich_handler_class_mock: MagicMock,
    ) -> None:
        """Verifies that create passes the configured show_level value to the RichHandler constructor."""
        logger_configuration = LoggerConfiguration()

        rich_configuration = RichConsoleConfiguration(
            show_level=False,
        )

        rich_handler_class_mock.return_value = MagicMock(
            spec=RichHandler,
        )

        self.rich_console_handler_factory.create(
            logger_configuration=logger_configuration,
            rich_configuration=rich_configuration,
        )

        rich_handler_class_mock.assert_called_once_with(
            level=logger_configuration.log_level,
            show_time=rich_configuration.show_time,
            show_level=False,
            show_path=rich_configuration.show_path,
            rich_tracebacks=rich_configuration.rich_tracebacks,
            markup=rich_configuration.markup,
        )

    @patch(
        "spectralog.handlers.rich_console_handler_factory.RichHandler",
    )
    def test_create_passes_show_path_configuration(
        self,
        rich_handler_class_mock: MagicMock,
    ) -> None:
        """Verifies that create passes the configured show_path value to the RichHandler constructor."""
        logger_configuration = LoggerConfiguration()

        rich_configuration = RichConsoleConfiguration(
            show_path=False,
        )

        rich_handler_class_mock.return_value = MagicMock(
            spec=RichHandler,
        )

        self.rich_console_handler_factory.create(
            logger_configuration=logger_configuration,
            rich_configuration=rich_configuration,
        )

        rich_handler_class_mock.assert_called_once_with(
            level=logger_configuration.log_level,
            show_time=rich_configuration.show_time,
            show_level=rich_configuration.show_level,
            show_path=False,
            rich_tracebacks=rich_configuration.rich_tracebacks,
            markup=rich_configuration.markup,
        )

    @patch(
        "spectralog.handlers.rich_console_handler_factory.RichHandler",
    )
    def test_create_passes_rich_tracebacks_configuration(
        self,
        rich_handler_class_mock: MagicMock,
    ) -> None:
        """Verifies that create passes the configured rich_tracebacks value to the RichHandler constructor."""
        logger_configuration = LoggerConfiguration()

        rich_configuration = RichConsoleConfiguration(
            rich_tracebacks=False,
        )

        rich_handler_class_mock.return_value = MagicMock(
            spec=RichHandler,
        )

        self.rich_console_handler_factory.create(
            logger_configuration=logger_configuration,
            rich_configuration=rich_configuration,
        )

        rich_handler_class_mock.assert_called_once_with(
            level=logger_configuration.log_level,
            show_time=rich_configuration.show_time,
            show_level=rich_configuration.show_level,
            show_path=rich_configuration.show_path,
            rich_tracebacks=False,
            markup=rich_configuration.markup,
        )

    @patch(
        "spectralog.handlers.rich_console_handler_factory.RichHandler",
    )
    def test_create_passes_markup_configuration(
        self,
        rich_handler_class_mock: MagicMock,
    ) -> None:
        """Verifies that create passes the configured markup value to the RichHandler constructor."""
        logger_configuration = LoggerConfiguration()

        rich_configuration = RichConsoleConfiguration(
            markup=True,
        )

        rich_handler_class_mock.return_value = MagicMock(
            spec=RichHandler,
        )

        self.rich_console_handler_factory.create(
            logger_configuration=logger_configuration,
            rich_configuration=rich_configuration,
        )

        rich_handler_class_mock.assert_called_once_with(
            level=logger_configuration.log_level,
            show_time=rich_configuration.show_time,
            show_level=rich_configuration.show_level,
            show_path=rich_configuration.show_path,
            rich_tracebacks=rich_configuration.rich_tracebacks,
            markup=True,
        )

    @patch(
        "spectralog.handlers.rich_console_handler_factory.logging.Formatter",
    )
    @patch(
        "spectralog.handlers.rich_console_handler_factory.RichHandler",
    )
    def test_create_constructs_message_only_formatter(
        self,
        rich_handler_class_mock: MagicMock,
        formatter_class_mock: MagicMock,
    ) -> None:
        """Verifies that create builds a message-only formatter using the configured logger date format."""
        logger_configuration = LoggerConfiguration(
            date_format="%d/%m/%Y %H:%M:%S",
        )

        rich_configuration = RichConsoleConfiguration()

        rich_handler_class_mock.return_value = MagicMock(
            spec=RichHandler,
        )

        formatter = MagicMock()

        formatter_class_mock.return_value = formatter

        self.rich_console_handler_factory.create(
            logger_configuration=logger_configuration,
            rich_configuration=rich_configuration,
        )

        formatter_class_mock.assert_called_once_with(
            fmt="%(message)s",
            datefmt=logger_configuration.date_format,
        )

    @patch(
        "spectralog.handlers.rich_console_handler_factory.logging.Formatter",
    )
    @patch(
        "spectralog.handlers.rich_console_handler_factory.RichHandler",
    )
    def test_create_assigns_created_formatter_to_rich_handler(
        self,
        rich_handler_class_mock: MagicMock,
        formatter_class_mock: MagicMock,
    ) -> None:
        """Verifies that create assigns the created logging formatter to the RichHandler instance."""
        logger_configuration = LoggerConfiguration()

        rich_configuration = RichConsoleConfiguration()

        rich_handler = MagicMock(
            spec=RichHandler,
        )

        formatter = MagicMock()

        rich_handler_class_mock.return_value = rich_handler
        formatter_class_mock.return_value = formatter

        self.rich_console_handler_factory.create(
            logger_configuration=logger_configuration,
            rich_configuration=rich_configuration,
        )

        rich_handler.setFormatter.assert_called_once_with(
            formatter,
        )

    @patch(
        "spectralog.handlers.rich_console_handler_factory.logging.Formatter",
    )
    @patch(
        "spectralog.handlers.rich_console_handler_factory.RichHandler",
    )
    def test_create_returns_handler_after_formatter_is_assigned(
        self,
        rich_handler_class_mock: MagicMock,
        formatter_class_mock: MagicMock,
    ) -> None:
        """Verifies that create returns the configured handler after assigning its formatter."""
        logger_configuration = LoggerConfiguration()

        rich_configuration = RichConsoleConfiguration()

        rich_handler = MagicMock(
            spec=RichHandler,
        )

        formatter = MagicMock()

        rich_handler_class_mock.return_value = rich_handler
        formatter_class_mock.return_value = formatter

        created_handler = self.rich_console_handler_factory.create(
            logger_configuration=logger_configuration,
            rich_configuration=rich_configuration,
        )

        rich_handler.setFormatter.assert_called_once_with(
            formatter,
        )

        self.assertIs(
            created_handler,
            rich_handler,
            ("Expected create() to return the RichHandler instance after " "its formatter was configured."),
        )
