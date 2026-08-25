from __future__ import annotations

import logging
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import call
from unittest.mock import MagicMock
from unittest.mock import patch

PROJECT_ROOT = Path(__file__).resolve().parents[3]  # noqa
SRC_DIR = PROJECT_ROOT / "src"  # noqa
sys.path.insert(0, str(SRC_DIR))  # noqa


from spectralog.configuration.configuration import LoggerConfiguration  # noqa: E402
from spectralog.configuration.rich_console_configuration import RichConsoleConfiguration  # noqa: E402
from spectralog.configuration.syslog_configuration import SyslogConfiguration  # noqa: E402
from spectralog.core.builder import ApplicationLoggerBuilder  # noqa: E402
from spectralog.core.models import LoggerBuildResult  # noqa: E402
from spectralog.core.protocols import ConsoleHandlerFactoryProtocol  # noqa: E402
from spectralog.core.protocols import FileHandlerFactoryProtocol  # noqa: E402
from spectralog.core.protocols import LogFilePathResolverProtocol  # noqa: E402
from spectralog.core.protocols import MultiprocessingHandlerFactoryProtocol  # noqa: E402
from spectralog.core.protocols import RichConsoleHandlerFactoryProtocol  # noqa: E402
from spectralog.core.protocols import SyslogHandlerFactoryProtocol  # noqa: E402
from spectralog.runtime.multiprocessing_logging_runtime import MultiprocessingLoggingRuntime  # noqa: E402


class UnitTestApplicationLoggerBuilder(unittest.TestCase):
    def setUp(self) -> None:
        self.console_handler_factory = MagicMock(
            spec=ConsoleHandlerFactoryProtocol,
        )

        self.rich_console_handler_factory = MagicMock(
            spec=RichConsoleHandlerFactoryProtocol,
        )

        self.file_handler_factory = MagicMock(
            spec=FileHandlerFactoryProtocol,
        )

        self.multiprocessing_handler_factory = MagicMock(
            spec=MultiprocessingHandlerFactoryProtocol,
        )

        self.syslog_handler_factory = MagicMock(
            spec=SyslogHandlerFactoryProtocol,
        )

        self.log_file_path_resolver = MagicMock(
            spec=LogFilePathResolverProtocol,
        )

    def _create_builder(
        self,
        configuration: LoggerConfiguration,
    ) -> ApplicationLoggerBuilder:
        application_logger_builder = ApplicationLoggerBuilder(
            configuration=configuration,
            console_handler_factory=self.console_handler_factory,
            rich_console_handler_factory=self.rich_console_handler_factory,
            file_handler_factory=self.file_handler_factory,
            multiprocessing_handler_factory=self.multiprocessing_handler_factory,
            syslog_handler_factory=self.syslog_handler_factory,
            log_file_path_resolver=self.log_file_path_resolver,
        )

        created_application_logger_builder = application_logger_builder

        return created_application_logger_builder

    def _create_logger_mock(
        self,
    ) -> MagicMock:
        logger = MagicMock(
            spec=logging.Logger,
        )

        logger.handlers = []

        created_logger = logger

        return created_logger

    @patch(
        "spectralog.core.builder.logging.getLogger",
    )
    def test_build_requests_logger_using_supplied_name(
        self,
        get_logger_mock: MagicMock,
    ) -> None:
        """Verifies that build requests a logging.Logger using the supplied logger name."""
        configuration = LoggerConfiguration(
            save_logs=False,
        )

        application_logger_builder = self._create_builder(
            configuration=configuration,
        )

        logger = self._create_logger_mock()

        console_handler = MagicMock(
            spec=logging.Handler,
        )

        get_logger_mock.return_value = logger
        self.console_handler_factory.create.return_value = console_handler

        application_logger_builder.build(
            name="spectralog.application",
        )

        get_logger_mock.assert_called_once_with(
            "spectralog.application",
        )

    @patch(
        "spectralog.core.builder.logging.getLogger",
    )
    def test_build_sets_logger_level_from_configuration(
        self,
        get_logger_mock: MagicMock,
    ) -> None:
        """Verifies that build configures the logger with the resolved logging level from LoggerConfiguration."""
        configuration = LoggerConfiguration(
            debug_mode=True,
            save_logs=False,
        )

        application_logger_builder = self._create_builder(
            configuration=configuration,
        )

        logger = self._create_logger_mock()

        console_handler = MagicMock(
            spec=logging.Handler,
        )

        get_logger_mock.return_value = logger
        self.console_handler_factory.create.return_value = console_handler

        application_logger_builder.build(
            name="spectralog.application",
        )

        logger.setLevel.assert_called_once_with(
            logging.DEBUG,
        )

    @patch(
        "spectralog.core.builder.logging.getLogger",
    )
    def test_build_uses_info_level_when_debug_mode_is_disabled(
        self,
        get_logger_mock: MagicMock,
    ) -> None:
        """Verifies that build configures the logger at INFO level when debug mode is disabled."""
        configuration = LoggerConfiguration(
            debug_mode=False,
            save_logs=False,
        )

        application_logger_builder = self._create_builder(
            configuration=configuration,
        )

        logger = self._create_logger_mock()

        self.console_handler_factory.create.return_value = MagicMock(
            spec=logging.Handler,
        )

        get_logger_mock.return_value = logger

        application_logger_builder.build(
            name="spectralog.application",
        )

        logger.setLevel.assert_called_once_with(
            logging.INFO,
        )

    @patch(
        "spectralog.core.builder.logging.getLogger",
    )
    def test_build_uses_standard_console_handler_when_rich_configuration_is_absent(
        self,
        get_logger_mock: MagicMock,
    ) -> None:
        """Verifies that build creates the standard console handler when Rich console configuration is absent."""
        configuration = LoggerConfiguration(
            save_logs=False,
            rich_console_configuration=None,
        )

        application_logger_builder = self._create_builder(
            configuration=configuration,
        )

        logger = self._create_logger_mock()

        console_handler = MagicMock(
            spec=logging.Handler,
        )

        get_logger_mock.return_value = logger
        self.console_handler_factory.create.return_value = console_handler

        application_logger_builder.build(
            name="spectralog.application",
        )

        self.console_handler_factory.create.assert_called_once_with(
            configuration,
        )

        self.rich_console_handler_factory.create.assert_not_called()

    @patch(
        "spectralog.core.builder.logging.getLogger",
    )
    def test_build_adds_standard_console_handler_to_logger(
        self,
        get_logger_mock: MagicMock,
    ) -> None:
        """Verifies that build attaches the standard console handler when Rich console output is disabled."""
        configuration = LoggerConfiguration(
            save_logs=False,
            rich_console_configuration=None,
        )

        application_logger_builder = self._create_builder(
            configuration=configuration,
        )

        logger = self._create_logger_mock()

        console_handler = MagicMock(
            spec=logging.Handler,
        )

        get_logger_mock.return_value = logger
        self.console_handler_factory.create.return_value = console_handler

        application_logger_builder.build(
            name="spectralog.application",
        )

        logger.addHandler.assert_called_once_with(
            console_handler,
        )

    @patch(
        "spectralog.core.builder.logging.getLogger",
    )
    def test_build_uses_rich_console_handler_when_rich_configuration_is_present(
        self,
        get_logger_mock: MagicMock,
    ) -> None:
        """Verifies that build uses the Rich console handler instead of the standard console handler when configured."""
        rich_console_configuration = RichConsoleConfiguration()

        configuration = LoggerConfiguration(
            save_logs=False,
            rich_console_configuration=rich_console_configuration,
        )

        application_logger_builder = self._create_builder(
            configuration=configuration,
        )

        logger = self._create_logger_mock()

        rich_console_handler = MagicMock(
            spec=logging.Handler,
        )

        get_logger_mock.return_value = logger
        self.rich_console_handler_factory.create.return_value = rich_console_handler

        application_logger_builder.build(
            name="spectralog.application",
        )

        self.rich_console_handler_factory.create.assert_called_once_with(
            logger_configuration=configuration,
            rich_configuration=rich_console_configuration,
        )

        self.console_handler_factory.create.assert_not_called()

    @patch(
        "spectralog.core.builder.logging.getLogger",
    )
    def test_build_adds_rich_console_handler_to_logger(
        self,
        get_logger_mock: MagicMock,
    ) -> None:
        """Verifies that build attaches the Rich console handler when Rich console configuration is enabled."""
        rich_console_configuration = RichConsoleConfiguration()

        configuration = LoggerConfiguration(
            save_logs=False,
            rich_console_configuration=rich_console_configuration,
        )

        application_logger_builder = self._create_builder(
            configuration=configuration,
        )

        logger = self._create_logger_mock()

        rich_console_handler = MagicMock(
            spec=logging.Handler,
        )

        get_logger_mock.return_value = logger
        self.rich_console_handler_factory.create.return_value = rich_console_handler

        application_logger_builder.build(
            name="spectralog.application",
        )

        logger.addHandler.assert_called_once_with(
            rich_console_handler,
        )

    @patch(
        "spectralog.core.builder.logging.getLogger",
    )
    def test_build_does_not_resolve_file_path_when_save_logs_is_disabled(
        self,
        get_logger_mock: MagicMock,
    ) -> None:
        """Verifies that build does not resolve a log file path when file logging is disabled."""
        configuration = LoggerConfiguration(
            save_logs=False,
        )

        application_logger_builder = self._create_builder(
            configuration=configuration,
        )

        logger = self._create_logger_mock()

        get_logger_mock.return_value = logger

        self.console_handler_factory.create.return_value = MagicMock(
            spec=logging.Handler,
        )

        application_logger_builder.build(
            name="spectralog.application",
        )

        self.log_file_path_resolver.resolve.assert_not_called()
        self.file_handler_factory.create.assert_not_called()
        self.multiprocessing_handler_factory.create.assert_not_called()

    @patch(
        "spectralog.core.builder.logging.getLogger",
    )
    def test_build_resolves_log_file_path_when_save_logs_is_enabled(
        self,
        get_logger_mock: MagicMock,
    ) -> None:
        """Verifies that build resolves the log file path when file logging is enabled."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            configuration = LoggerConfiguration(
                save_logs=True,
            )

            application_logger_builder = self._create_builder(
                configuration=configuration,
            )

            logger = self._create_logger_mock()

            log_file_path = (
                Path(
                    temporary_directory,
                )
                / "application.log"
            )

            get_logger_mock.return_value = logger

            self.console_handler_factory.create.return_value = MagicMock(
                spec=logging.Handler,
            )

            self.log_file_path_resolver.resolve.return_value = log_file_path

            self.file_handler_factory.create.return_value = MagicMock(
                spec=logging.Handler,
            )

            application_logger_builder.build(
                name="spectralog.application",
            )

            self.log_file_path_resolver.resolve.assert_called_once_with(
                configuration,
            )

    @patch(
        "spectralog.core.builder.logging.getLogger",
    )
    def test_build_marks_missing_log_file_as_new(
        self,
        get_logger_mock: MagicMock,
    ) -> None:
        """Verifies that build marks a missing log file as new."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            log_file_path = (
                Path(
                    temporary_directory,
                )
                / "application.log"
            )

            configuration = LoggerConfiguration(
                save_logs=True,
            )

            application_logger_builder = self._create_builder(
                configuration=configuration,
            )

            logger = self._create_logger_mock()

            get_logger_mock.return_value = logger

            self.console_handler_factory.create.return_value = MagicMock(
                spec=logging.Handler,
            )

            self.log_file_path_resolver.resolve.return_value = log_file_path

            self.file_handler_factory.create.return_value = MagicMock(
                spec=logging.Handler,
            )

            logger_build_result = application_logger_builder.build(
                name="spectralog.application",
            )

            self.assertTrue(
                logger_build_result.is_new_log_file,
                "Expected a missing log file to be classified as a new log file.",
            )

    @patch(
        "spectralog.core.builder.logging.getLogger",
    )
    def test_build_marks_empty_existing_log_file_as_new(
        self,
        get_logger_mock: MagicMock,
    ) -> None:
        """Verifies that build marks an existing empty log file as new."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            log_file_path = (
                Path(
                    temporary_directory,
                )
                / "application.log"
            )

            log_file_path.touch()

            configuration = LoggerConfiguration(
                save_logs=True,
            )

            application_logger_builder = self._create_builder(
                configuration=configuration,
            )

            logger = self._create_logger_mock()

            get_logger_mock.return_value = logger

            self.console_handler_factory.create.return_value = MagicMock(
                spec=logging.Handler,
            )

            self.log_file_path_resolver.resolve.return_value = log_file_path

            self.file_handler_factory.create.return_value = MagicMock(
                spec=logging.Handler,
            )

            logger_build_result = application_logger_builder.build(
                name="spectralog.application",
            )

            self.assertTrue(
                logger_build_result.is_new_log_file,
                "Expected an existing empty log file to be classified as new.",
            )

    @patch(
        "spectralog.core.builder.logging.getLogger",
    )
    def test_build_marks_non_empty_existing_log_file_as_not_new(
        self,
        get_logger_mock: MagicMock,
    ) -> None:
        """Verifies that build marks an existing non-empty log file as not new."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            log_file_path = (
                Path(
                    temporary_directory,
                )
                / "application.log"
            )

            log_file_path.write_text(
                "existing log entry",
                encoding="utf-8",
            )

            configuration = LoggerConfiguration(
                save_logs=True,
            )

            application_logger_builder = self._create_builder(
                configuration=configuration,
            )

            logger = self._create_logger_mock()

            get_logger_mock.return_value = logger

            self.console_handler_factory.create.return_value = MagicMock(
                spec=logging.Handler,
            )

            self.log_file_path_resolver.resolve.return_value = log_file_path

            self.file_handler_factory.create.return_value = MagicMock(
                spec=logging.Handler,
            )

            logger_build_result = application_logger_builder.build(
                name="spectralog.application",
            )

            self.assertFalse(
                logger_build_result.is_new_log_file,
                "Expected an existing non-empty log file not to be classified as new.",
            )

    @patch(
        "spectralog.core.builder.logging.getLogger",
    )
    def test_build_creates_standard_file_handler_when_multiprocessing_is_disabled(
        self,
        get_logger_mock: MagicMock,
    ) -> None:
        """Verifies that build creates a standard file handler when multiprocessing-safe logging is disabled."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            configuration = LoggerConfiguration(
                save_logs=True,
                multiprocessing_safe=False,
            )

            application_logger_builder = self._create_builder(
                configuration=configuration,
            )

            logger = self._create_logger_mock()

            log_file_path = (
                Path(
                    temporary_directory,
                )
                / "application.log"
            )

            file_handler = MagicMock(
                spec=logging.Handler,
            )

            get_logger_mock.return_value = logger

            self.console_handler_factory.create.return_value = MagicMock(
                spec=logging.Handler,
            )

            self.log_file_path_resolver.resolve.return_value = log_file_path
            self.file_handler_factory.create.return_value = file_handler

            application_logger_builder.build(
                name="spectralog.application",
            )

            self.file_handler_factory.create.assert_called_once_with(
                configuration=configuration,
                log_file_path=log_file_path,
            )

            self.multiprocessing_handler_factory.create.assert_not_called()

    @patch(
        "spectralog.core.builder.logging.getLogger",
    )
    def test_build_adds_standard_file_handler_to_logger(
        self,
        get_logger_mock: MagicMock,
    ) -> None:
        """Verifies that build attaches the file handler when standard file logging is enabled."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            configuration = LoggerConfiguration(
                save_logs=True,
                multiprocessing_safe=False,
            )

            application_logger_builder = self._create_builder(
                configuration=configuration,
            )

            logger = self._create_logger_mock()

            console_handler = MagicMock(
                spec=logging.Handler,
            )

            file_handler = MagicMock(
                spec=logging.Handler,
            )

            log_file_path = (
                Path(
                    temporary_directory,
                )
                / "application.log"
            )

            get_logger_mock.return_value = logger
            self.console_handler_factory.create.return_value = console_handler
            self.log_file_path_resolver.resolve.return_value = log_file_path
            self.file_handler_factory.create.return_value = file_handler

            application_logger_builder.build(
                name="spectralog.application",
            )

            expected_handler_calls = [
                call(
                    console_handler,
                ),
                call(
                    file_handler,
                ),
            ]

            self.assertEqual(
                logger.addHandler.call_args_list,
                expected_handler_calls,
                ("Expected the console handler to be attached first and " "the standard file handler second."),
            )

    @patch(
        "spectralog.core.builder.logging.getLogger",
    )
    def test_build_creates_multiprocessing_runtime_when_enabled(
        self,
        get_logger_mock: MagicMock,
    ) -> None:
        """Verifies that build creates the multiprocessing logging runtime when multiprocessing-safe logging is enabled."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            configuration = LoggerConfiguration(
                save_logs=True,
                multiprocessing_safe=True,
            )

            application_logger_builder = self._create_builder(
                configuration=configuration,
            )

            logger = self._create_logger_mock()

            log_file_path = (
                Path(
                    temporary_directory,
                )
                / "application.log"
            )

            multiprocessing_logging_runtime = MagicMock(
                spec=MultiprocessingLoggingRuntime,
            )

            queue_handler = MagicMock(
                spec=logging.Handler,
            )

            multiprocessing_logging_runtime.queue_handler = queue_handler

            get_logger_mock.return_value = logger

            self.console_handler_factory.create.return_value = MagicMock(
                spec=logging.Handler,
            )

            self.log_file_path_resolver.resolve.return_value = log_file_path
            self.multiprocessing_handler_factory.create.return_value = multiprocessing_logging_runtime

            application_logger_builder.build(
                name="spectralog.application",
            )

            self.multiprocessing_handler_factory.create.assert_called_once_with(
                configuration=configuration,
                log_file_path=log_file_path,
            )

            self.file_handler_factory.create.assert_not_called()

    @patch(
        "spectralog.core.builder.logging.getLogger",
    )
    def test_build_adds_multiprocessing_queue_handler_to_logger(
        self,
        get_logger_mock: MagicMock,
    ) -> None:
        """Verifies that build attaches the multiprocessing queue handler instead of a direct file handler."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            configuration = LoggerConfiguration(
                save_logs=True,
                multiprocessing_safe=True,
            )

            application_logger_builder = self._create_builder(
                configuration=configuration,
            )

            logger = self._create_logger_mock()

            console_handler = MagicMock(
                spec=logging.Handler,
            )

            queue_handler = MagicMock(
                spec=logging.Handler,
            )

            multiprocessing_logging_runtime = MagicMock(
                spec=MultiprocessingLoggingRuntime,
            )

            multiprocessing_logging_runtime.queue_handler = queue_handler

            log_file_path = (
                Path(
                    temporary_directory,
                )
                / "application.log"
            )

            get_logger_mock.return_value = logger
            self.console_handler_factory.create.return_value = console_handler
            self.log_file_path_resolver.resolve.return_value = log_file_path
            self.multiprocessing_handler_factory.create.return_value = multiprocessing_logging_runtime

            application_logger_builder.build(
                name="spectralog.application",
            )

            expected_handler_calls = [
                call(
                    console_handler,
                ),
                call(
                    queue_handler,
                ),
            ]

            self.assertEqual(
                logger.addHandler.call_args_list,
                expected_handler_calls,
                ("Expected the console handler to be attached first and " "the multiprocessing queue handler second."),
            )

    @patch(
        "spectralog.core.builder.logging.getLogger",
    )
    def test_build_creates_syslog_handler_when_syslog_configuration_is_present(
        self,
        get_logger_mock: MagicMock,
    ) -> None:
        """Verifies that build creates a syslog handler when syslog configuration is supplied."""
        syslog_configuration = SyslogConfiguration()

        configuration = LoggerConfiguration(
            save_logs=False,
            syslog_configuration=syslog_configuration,
        )

        application_logger_builder = self._create_builder(
            configuration=configuration,
        )

        logger = self._create_logger_mock()

        syslog_handler = MagicMock(
            spec=logging.Handler,
        )

        get_logger_mock.return_value = logger

        self.console_handler_factory.create.return_value = MagicMock(
            spec=logging.Handler,
        )

        self.syslog_handler_factory.create.return_value = syslog_handler

        application_logger_builder.build(
            name="spectralog.application",
        )

        self.syslog_handler_factory.create.assert_called_once_with(
            logger_configuration=configuration,
            syslog_configuration=syslog_configuration,
        )

    @patch(
        "spectralog.core.builder.logging.getLogger",
    )
    def test_build_does_not_create_syslog_handler_when_configuration_is_absent(
        self,
        get_logger_mock: MagicMock,
    ) -> None:
        """Verifies that build does not create a syslog handler when no syslog configuration is supplied."""
        configuration = LoggerConfiguration(
            save_logs=False,
            syslog_configuration=None,
        )

        application_logger_builder = self._create_builder(
            configuration=configuration,
        )

        logger = self._create_logger_mock()

        get_logger_mock.return_value = logger

        self.console_handler_factory.create.return_value = MagicMock(
            spec=logging.Handler,
        )

        application_logger_builder.build(
            name="spectralog.application",
        )

        self.syslog_handler_factory.create.assert_not_called()

    @patch(
        "spectralog.core.builder.logging.getLogger",
    )
    def test_build_adds_syslog_handler_to_logger(
        self,
        get_logger_mock: MagicMock,
    ) -> None:
        """Verifies that build attaches the created syslog handler to the logger."""
        syslog_configuration = SyslogConfiguration()

        configuration = LoggerConfiguration(
            save_logs=False,
            syslog_configuration=syslog_configuration,
        )

        application_logger_builder = self._create_builder(
            configuration=configuration,
        )

        logger = self._create_logger_mock()

        console_handler = MagicMock(
            spec=logging.Handler,
        )

        syslog_handler = MagicMock(
            spec=logging.Handler,
        )

        get_logger_mock.return_value = logger
        self.console_handler_factory.create.return_value = console_handler
        self.syslog_handler_factory.create.return_value = syslog_handler

        application_logger_builder.build(
            name="spectralog.application",
        )

        expected_handler_calls = [
            call(
                console_handler,
            ),
            call(
                syslog_handler,
            ),
        ]

        self.assertEqual(
            logger.addHandler.call_args_list,
            expected_handler_calls,
            ("Expected the console handler to be attached first and " "the syslog handler second."),
        )

    @patch(
        "spectralog.core.builder.logging.getLogger",
    )
    def test_build_disables_logger_propagation(
        self,
        get_logger_mock: MagicMock,
    ) -> None:
        """Verifies that build disables propagation to prevent duplicate logging through ancestor loggers."""
        configuration = LoggerConfiguration(
            save_logs=False,
        )

        application_logger_builder = self._create_builder(
            configuration=configuration,
        )

        logger = self._create_logger_mock()

        get_logger_mock.return_value = logger

        self.console_handler_factory.create.return_value = MagicMock(
            spec=logging.Handler,
        )

        application_logger_builder.build(
            name="spectralog.application",
        )

        self.assertFalse(
            logger.propagate,
            "Expected build() to disable logger propagation.",
        )

    @patch(
        "spectralog.core.builder.logging.getLogger",
    )
    def test_build_returns_logger_build_result(
        self,
        get_logger_mock: MagicMock,
    ) -> None:
        """Verifies that build returns a LoggerBuildResult containing the configured logger."""
        configuration = LoggerConfiguration(
            save_logs=False,
        )

        application_logger_builder = self._create_builder(
            configuration=configuration,
        )

        logger = self._create_logger_mock()

        get_logger_mock.return_value = logger

        self.console_handler_factory.create.return_value = MagicMock(
            spec=logging.Handler,
        )

        logger_build_result = application_logger_builder.build(
            name="spectralog.application",
        )

        self.assertIsInstance(
            logger_build_result,
            LoggerBuildResult,
            "Expected build() to return a LoggerBuildResult instance.",
        )

        self.assertIs(
            logger_build_result.logger,
            logger,
            ("Expected LoggerBuildResult to contain the logger produced " "by logging.getLogger()."),
        )

    @patch(
        "spectralog.core.builder.logging.getLogger",
    )
    def test_build_result_contains_none_file_path_when_save_logs_is_disabled(
        self,
        get_logger_mock: MagicMock,
    ) -> None:
        """Verifies that LoggerBuildResult contains no log file path when file logging is disabled."""
        configuration = LoggerConfiguration(
            save_logs=False,
        )

        application_logger_builder = self._create_builder(
            configuration=configuration,
        )

        logger = self._create_logger_mock()

        get_logger_mock.return_value = logger

        self.console_handler_factory.create.return_value = MagicMock(
            spec=logging.Handler,
        )

        logger_build_result = application_logger_builder.build(
            name="spectralog.application",
        )

        self.assertIsNone(
            logger_build_result.log_file_path,
            "Expected log_file_path to be None when save_logs is disabled.",
        )

        self.assertFalse(
            logger_build_result.is_new_log_file,
            "Expected is_new_log_file to remain False when save_logs is disabled.",
        )

        self.assertIsNone(
            logger_build_result.multiprocessing_logging_runtime,
            ("Expected multiprocessing_logging_runtime to be None when " "file logging is disabled."),
        )

    @patch(
        "spectralog.core.builder.logging.getLogger",
    )
    def test_build_result_contains_resolved_log_file_path(
        self,
        get_logger_mock: MagicMock,
    ) -> None:
        """Verifies that LoggerBuildResult contains the resolved file path when file logging is enabled."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            configuration = LoggerConfiguration(
                save_logs=True,
            )

            application_logger_builder = self._create_builder(
                configuration=configuration,
            )

            logger = self._create_logger_mock()

            log_file_path = (
                Path(
                    temporary_directory,
                )
                / "application.log"
            )

            get_logger_mock.return_value = logger

            self.console_handler_factory.create.return_value = MagicMock(
                spec=logging.Handler,
            )

            self.log_file_path_resolver.resolve.return_value = log_file_path

            self.file_handler_factory.create.return_value = MagicMock(
                spec=logging.Handler,
            )

            logger_build_result = application_logger_builder.build(
                name="spectralog.application",
            )

            self.assertIs(
                logger_build_result.log_file_path,
                log_file_path,
                ("Expected LoggerBuildResult to contain the exact " "resolved log file path."),
            )

    @patch(
        "spectralog.core.builder.logging.getLogger",
    )
    def test_build_result_contains_multiprocessing_runtime_when_enabled(
        self,
        get_logger_mock: MagicMock,
    ) -> None:
        """Verifies that LoggerBuildResult contains the multiprocessing runtime when multiprocessing-safe logging is enabled."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            configuration = LoggerConfiguration(
                save_logs=True,
                multiprocessing_safe=True,
            )

            application_logger_builder = self._create_builder(
                configuration=configuration,
            )

            logger = self._create_logger_mock()

            log_file_path = (
                Path(
                    temporary_directory,
                )
                / "application.log"
            )

            multiprocessing_logging_runtime = MagicMock(
                spec=MultiprocessingLoggingRuntime,
            )

            multiprocessing_logging_runtime.queue_handler = MagicMock(
                spec=logging.Handler,
            )

            get_logger_mock.return_value = logger

            self.console_handler_factory.create.return_value = MagicMock(
                spec=logging.Handler,
            )

            self.log_file_path_resolver.resolve.return_value = log_file_path
            self.multiprocessing_handler_factory.create.return_value = multiprocessing_logging_runtime

            logger_build_result = application_logger_builder.build(
                name="spectralog.application",
            )

            self.assertIs(
                logger_build_result.multiprocessing_logging_runtime,
                multiprocessing_logging_runtime,
                ("Expected LoggerBuildResult to contain the exact " "multiprocessing runtime returned by the factory."),
            )

    def test_reset_logger_removes_all_existing_handlers(
        self,
    ) -> None:
        """Verifies that _reset_logger removes every handler currently attached to the logger."""
        configuration = LoggerConfiguration()

        application_logger_builder = self._create_builder(
            configuration=configuration,
        )

        logger = self._create_logger_mock()

        first_handler = MagicMock(
            spec=logging.Handler,
        )

        second_handler = MagicMock(
            spec=logging.Handler,
        )

        logger.handlers = [
            first_handler,
            second_handler,
        ]

        application_logger_builder._reset_logger(
            logger=logger,
        )

        expected_remove_calls = [
            call(
                first_handler,
            ),
            call(
                second_handler,
            ),
        ]

        self.assertEqual(
            logger.removeHandler.call_args_list,
            expected_remove_calls,
            ("Expected _reset_logger() to remove every existing handler " "from the logger."),
        )

    def test_reset_logger_closes_all_existing_handlers(
        self,
    ) -> None:
        """Verifies that _reset_logger closes every handler removed from the logger."""
        configuration = LoggerConfiguration()

        application_logger_builder = self._create_builder(
            configuration=configuration,
        )

        logger = self._create_logger_mock()

        first_handler = MagicMock(
            spec=logging.Handler,
        )

        second_handler = MagicMock(
            spec=logging.Handler,
        )

        logger.handlers = [
            first_handler,
            second_handler,
        ]

        application_logger_builder._reset_logger(
            logger=logger,
        )

        first_handler.close.assert_called_once_with()
        second_handler.close.assert_called_once_with()

    def test_reset_logger_removes_handler_before_closing_it(
        self,
    ) -> None:
        """Verifies that each existing handler is removed from the logger before it is closed."""
        configuration = LoggerConfiguration()

        application_logger_builder = self._create_builder(
            configuration=configuration,
        )

        logger = self._create_logger_mock()

        existing_handler = MagicMock(
            spec=logging.Handler,
        )

        logger.handlers = [
            existing_handler,
        ]

        parent_mock = MagicMock()

        parent_mock.attach_mock(
            logger.removeHandler,
            "remove_handler",
        )

        parent_mock.attach_mock(
            existing_handler.close,
            "close_handler",
        )

        application_logger_builder._reset_logger(
            logger=logger,
        )

        expected_method_calls = [
            call.remove_handler(
                existing_handler,
            ),
            call.close_handler(),
        ]

        self.assertEqual(
            parent_mock.method_calls,
            expected_method_calls,
            ("Expected _reset_logger() to remove an existing handler " "before closing it."),
        )

    def test_reset_logger_does_nothing_when_logger_has_no_handlers(
        self,
    ) -> None:
        """Verifies that _reset_logger performs no removal operations when the logger has no handlers."""
        configuration = LoggerConfiguration()

        application_logger_builder = self._create_builder(
            configuration=configuration,
        )

        logger = self._create_logger_mock()

        application_logger_builder._reset_logger(
            logger=logger,
        )

        logger.removeHandler.assert_not_called()

    def test_reset_logger_uses_copy_of_handler_collection(
        self,
    ) -> None:
        """Verifies that _reset_logger safely iterates over a copied handler collection while removing handlers."""
        configuration = LoggerConfiguration()

        application_logger_builder = self._create_builder(
            configuration=configuration,
        )

        first_handler = MagicMock(
            spec=logging.Handler,
        )

        second_handler = MagicMock(
            spec=logging.Handler,
        )

        logger = logging.Logger(
            name="spectralog-reset-test",
        )

        logger.addHandler(
            first_handler,
        )

        logger.addHandler(
            second_handler,
        )

        application_logger_builder._reset_logger(
            logger=logger,
        )

        self.assertEqual(
            logger.handlers,
            [],
            ("Expected _reset_logger() to remove all handlers safely " "while iterating over a copied handler collection."),
        )

        first_handler.close.assert_called_once_with()
        second_handler.close.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
