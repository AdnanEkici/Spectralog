from __future__ import annotations

import logging
import sys
import tempfile
import unittest
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import cast
from unittest.mock import call
from unittest.mock import MagicMock
from unittest.mock import patch

PROJECT_ROOT = Path(__file__).resolve().parents[3]  # noqa
SRC_DIR = PROJECT_ROOT / "src"  # noqa
sys.path.insert(0, str(SRC_DIR))  # noqa

from spectralog.configuration.configuration import LoggerConfiguration  # noqa: E402
from spectralog.core.protocols import FileFormatterResolverProtocol  # noqa: E402
from spectralog.formatting.relative_path_filter import RelativePathFilter  # noqa: E402
from spectralog.handlers.file_handler_factory import FileHandlerFactory  # noqa: E402


class UnitTestFileHandlerFactory(unittest.TestCase):
    def setUp(self) -> None:
        self.file_formatter_resolver = MagicMock(
            spec=FileFormatterResolverProtocol,
        )

        self.relative_path_filter = MagicMock(
            spec=RelativePathFilter,
        )

        self.file_handler_factory = FileHandlerFactory(
            file_formatter_resolver=self.file_formatter_resolver,
            relative_path_filter=self.relative_path_filter,
        )

    @patch(
        "spectralog.handlers.file_handler_factory.RotatingFileHandler",
    )
    def test_create_returns_created_rotating_file_handler(
        self,
        rotating_file_handler_class_mock: MagicMock,
    ) -> None:
        """Verifies that create returns the RotatingFileHandler instance produced by the handler constructor."""
        configuration = LoggerConfiguration()

        log_file_path = Path(
            "logs/application.log",
        )

        formatter = MagicMock(
            spec=logging.Formatter,
        )

        file_handler = MagicMock(
            spec=RotatingFileHandler,
        )

        self.file_formatter_resolver.resolve.return_value = formatter

        rotating_file_handler_class_mock.return_value = file_handler

        created_handler = self.file_handler_factory.create(
            configuration=configuration,
            log_file_path=log_file_path,
        )

        self.assertIs(
            created_handler,
            file_handler,
            ("Expected create() to return the same RotatingFileHandler " "instance created by the handler constructor."),
        )

    @patch(
        "spectralog.handlers.file_handler_factory.RotatingFileHandler",
    )
    def test_create_resolves_formatter_using_logger_configuration(
        self,
        rotating_file_handler_class_mock: MagicMock,
    ) -> None:
        """Verifies that create resolves the file formatter using the supplied logger configuration."""
        configuration = LoggerConfiguration(
            debug_mode=True,
        )

        log_file_path = Path(
            "logs/application.log",
        )

        formatter = MagicMock(
            spec=logging.Formatter,
        )

        self.file_formatter_resolver.resolve.return_value = formatter

        rotating_file_handler_class_mock.return_value = MagicMock(
            spec=RotatingFileHandler,
        )

        self.file_handler_factory.create(
            configuration=configuration,
            log_file_path=log_file_path,
        )

        self.file_formatter_resolver.resolve.assert_called_once_with(
            configuration,
        )

    @patch(
        "spectralog.handlers.file_handler_factory.RotatingFileHandler",
    )
    def test_create_constructs_rotating_file_handler_with_expected_configuration(
        self,
        rotating_file_handler_class_mock: MagicMock,
    ) -> None:
        """Verifies that create constructs RotatingFileHandler with the configured file path, rotation limits, and UTF-8 encoding."""
        configuration = LoggerConfiguration(
            max_bytes=5_000_000,
            backup_count=3,
        )

        log_file_path = Path(
            "logs/application.log",
        )

        self.file_formatter_resolver.resolve.return_value = MagicMock(
            spec=logging.Formatter,
        )

        rotating_file_handler_class_mock.return_value = MagicMock(
            spec=RotatingFileHandler,
        )

        self.file_handler_factory.create(
            configuration=configuration,
            log_file_path=log_file_path,
        )

        rotating_file_handler_class_mock.assert_called_once_with(
            filename=log_file_path,
            maxBytes=configuration.max_bytes,
            backupCount=configuration.backup_count,
            encoding="utf-8",
        )

    @patch(
        "spectralog.handlers.file_handler_factory.RotatingFileHandler",
    )
    def test_create_sets_info_level_when_debug_mode_is_disabled(
        self,
        rotating_file_handler_class_mock: MagicMock,
    ) -> None:
        """Verifies that create configures the file handler at INFO level when debug mode is disabled."""
        configuration = LoggerConfiguration(
            debug_mode=False,
        )

        log_file_path = Path(
            "logs/application.log",
        )

        file_handler = MagicMock(
            spec=RotatingFileHandler,
        )

        self.file_formatter_resolver.resolve.return_value = MagicMock(
            spec=logging.Formatter,
        )

        rotating_file_handler_class_mock.return_value = file_handler

        self.file_handler_factory.create(
            configuration=configuration,
            log_file_path=log_file_path,
        )

        file_handler.setLevel.assert_called_once_with(
            logging.INFO,
        )

    @patch(
        "spectralog.handlers.file_handler_factory.RotatingFileHandler",
    )
    def test_create_sets_debug_level_when_debug_mode_is_enabled(
        self,
        rotating_file_handler_class_mock: MagicMock,
    ) -> None:
        """Verifies that create configures the file handler at DEBUG level when debug mode is enabled."""
        configuration = LoggerConfiguration(
            debug_mode=True,
        )

        log_file_path = Path(
            "logs/application.log",
        )

        file_handler = MagicMock(
            spec=RotatingFileHandler,
        )

        self.file_formatter_resolver.resolve.return_value = MagicMock(
            spec=logging.Formatter,
        )

        rotating_file_handler_class_mock.return_value = file_handler

        self.file_handler_factory.create(
            configuration=configuration,
            log_file_path=log_file_path,
        )

        file_handler.setLevel.assert_called_once_with(
            logging.DEBUG,
        )

    @patch(
        "spectralog.handlers.file_handler_factory.RotatingFileHandler",
    )
    def test_create_uses_resolved_formatter(
        self,
        rotating_file_handler_class_mock: MagicMock,
    ) -> None:
        """Verifies that create assigns the formatter returned by the file formatter resolver to the file handler."""
        configuration = LoggerConfiguration()

        log_file_path = Path(
            "logs/application.log",
        )

        formatter = MagicMock(
            spec=logging.Formatter,
        )

        file_handler = MagicMock(
            spec=RotatingFileHandler,
        )

        self.file_formatter_resolver.resolve.return_value = formatter

        rotating_file_handler_class_mock.return_value = file_handler

        self.file_handler_factory.create(
            configuration=configuration,
            log_file_path=log_file_path,
        )

        file_handler.setFormatter.assert_called_once_with(
            formatter,
        )

    @patch(
        "spectralog.handlers.file_handler_factory.RotatingFileHandler",
    )
    def test_create_adds_relative_path_filter(
        self,
        rotating_file_handler_class_mock: MagicMock,
    ) -> None:
        """Verifies that create attaches the supplied RelativePathFilter to the rotating file handler."""
        configuration = LoggerConfiguration()

        log_file_path = Path(
            "logs/application.log",
        )

        file_handler = MagicMock(
            spec=RotatingFileHandler,
        )

        self.file_formatter_resolver.resolve.return_value = MagicMock(
            spec=logging.Formatter,
        )

        rotating_file_handler_class_mock.return_value = file_handler

        self.file_handler_factory.create(
            configuration=configuration,
            log_file_path=log_file_path,
        )

        file_handler.addFilter.assert_called_once_with(
            self.relative_path_filter,
        )

    @patch(
        "spectralog.handlers.file_handler_factory.RotatingFileHandler",
    )
    def test_create_configures_handler_in_expected_order(
        self,
        rotating_file_handler_class_mock: MagicMock,
    ) -> None:
        """Verifies that create applies the level, formatter, and relative path filter in the expected order."""
        configuration = LoggerConfiguration(
            debug_mode=True,
        )

        log_file_path = Path(
            "logs/application.log",
        )

        formatter = MagicMock(
            spec=logging.Formatter,
        )

        file_handler = MagicMock(
            spec=RotatingFileHandler,
        )

        self.file_formatter_resolver.resolve.return_value = formatter

        rotating_file_handler_class_mock.return_value = file_handler

        self.file_handler_factory.create(
            configuration=configuration,
            log_file_path=log_file_path,
        )

        expected_method_calls = [
            call.setLevel(
                logging.DEBUG,
            ),
            call.setFormatter(
                formatter,
            ),
            call.addFilter(
                self.relative_path_filter,
            ),
        ]

        self.assertEqual(
            file_handler.method_calls,
            expected_method_calls,
            ("Expected the file handler to be configured in the order " "setLevel(), setFormatter(), then addFilter()."),
        )

    @patch(
        "spectralog.handlers.file_handler_factory.RotatingFileHandler",
    )
    def test_create_uses_configuration_log_level_property(
        self,
        rotating_file_handler_class_mock: MagicMock,
    ) -> None:
        """Verifies that create uses the resolved log level provided by the logger configuration."""
        configuration = MagicMock(
            spec=LoggerConfiguration,
        )

        configuration.log_level = logging.ERROR
        configuration.max_bytes = 10_000
        configuration.backup_count = 2

        log_file_path = Path(
            "logs/application.log",
        )

        file_handler = MagicMock(
            spec=RotatingFileHandler,
        )

        self.file_formatter_resolver.resolve.return_value = MagicMock(
            spec=logging.Formatter,
        )

        rotating_file_handler_class_mock.return_value = file_handler

        self.file_handler_factory.create(
            configuration=configuration,
            log_file_path=log_file_path,
        )

        file_handler.setLevel.assert_called_once_with(
            logging.ERROR,
        )

    @patch(
        "spectralog.handlers.file_handler_factory.RotatingFileHandler",
    )
    def test_create_supports_jsonl_log_file_path(
        self,
        rotating_file_handler_class_mock: MagicMock,
    ) -> None:
        """Verifies that create forwards a JSON Lines file path unchanged to the RotatingFileHandler constructor."""
        configuration = LoggerConfiguration()

        log_file_path = Path(
            "logs/application.jsonl",
        )

        self.file_formatter_resolver.resolve.return_value = MagicMock(
            spec=logging.Formatter,
        )

        rotating_file_handler_class_mock.return_value = MagicMock(
            spec=RotatingFileHandler,
        )

        self.file_handler_factory.create(
            configuration=configuration,
            log_file_path=log_file_path,
        )

        rotating_file_handler_class_mock.assert_called_once_with(
            filename=log_file_path,
            maxBytes=configuration.max_bytes,
            backupCount=configuration.backup_count,
            encoding="utf-8",
        )

    @patch(
        "spectralog.handlers.file_handler_factory.RotatingFileHandler",
    )
    def test_create_uses_custom_rotation_configuration(
        self,
        rotating_file_handler_class_mock: MagicMock,
    ) -> None:
        """Verifies that create forwards custom rotation size and backup count values to RotatingFileHandler."""
        custom_max_bytes = 25_000_000
        custom_backup_count = 7

        configuration = LoggerConfiguration(
            max_bytes=custom_max_bytes,
            backup_count=custom_backup_count,
        )

        log_file_path = Path(
            "logs/application.log",
        )

        self.file_formatter_resolver.resolve.return_value = MagicMock(
            spec=logging.Formatter,
        )

        rotating_file_handler_class_mock.return_value = MagicMock(
            spec=RotatingFileHandler,
        )

        self.file_handler_factory.create(
            configuration=configuration,
            log_file_path=log_file_path,
        )

        rotating_file_handler_class_mock.assert_called_once_with(
            filename=log_file_path,
            maxBytes=custom_max_bytes,
            backupCount=custom_backup_count,
            encoding="utf-8",
        )

    def test_create_returns_real_rotating_file_handler(
        self,
    ) -> None:
        """Verifies that create produces a real RotatingFileHandler with the expected formatter, level, filter, and rotation settings."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            log_file_path = (
                Path(
                    temporary_directory,
                )
                / "application.log"
            )

            configuration = LoggerConfiguration(
                debug_mode=True,
                max_bytes=50_000,
                backup_count=4,
            )

            formatter = logging.Formatter(
                "%(levelname)s | %(message)s",
            )

            file_formatter_resolver = MagicMock(
                spec=FileFormatterResolverProtocol,
            )

            file_formatter_resolver.resolve.return_value = formatter

            relative_path_filter = RelativePathFilter()

            file_handler_factory = FileHandlerFactory(
                file_formatter_resolver=file_formatter_resolver,
                relative_path_filter=relative_path_filter,
            )

            created_handler = file_handler_factory.create(
                configuration=configuration,
                log_file_path=log_file_path,
            )

            self.assertIsInstance(
                created_handler,
                RotatingFileHandler,
                ("Expected create() to return a real RotatingFileHandler " "when the handler constructor is not mocked."),
            )

            rotating_file_handler = cast(
                RotatingFileHandler,
                created_handler,
            )

            self.assertEqual(
                rotating_file_handler.level,
                logging.DEBUG,
                ("Expected the real file handler to use DEBUG level when " "debug mode is enabled."),
            )

            self.assertIs(
                rotating_file_handler.formatter,
                formatter,
                ("Expected the real file handler to retain the formatter " "returned by the file formatter resolver."),
            )

            self.assertIn(
                relative_path_filter,
                rotating_file_handler.filters,
                ("Expected the real file handler to contain the supplied " "RelativePathFilter."),
            )

            self.assertEqual(
                rotating_file_handler.maxBytes,
                configuration.max_bytes,
                ("Expected the real RotatingFileHandler maxBytes value to " "match the logger configuration."),
            )

            self.assertEqual(
                rotating_file_handler.backupCount,
                configuration.backup_count,
                ("Expected the real RotatingFileHandler backupCount value " "to match the logger configuration."),
            )

            self.assertEqual(
                Path(rotating_file_handler.baseFilename),
                log_file_path.resolve(),
                ("Expected the real RotatingFileHandler to target the " "supplied log file path."),
            )

            rotating_file_handler.close()
