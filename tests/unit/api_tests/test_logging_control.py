from __future__ import annotations

import logging
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock
from unittest.mock import patch
import tempfile

PROJECT_ROOT = Path(__file__).resolve().parents[3]  # noqa
SRC_DIR = PROJECT_ROOT / "src"  # noqa
sys.path.insert(0, str(SRC_DIR))  # noqa


from spectralog.api.logging_control import disable_application_logging  # noqa: E402
from spectralog.api.colored_logger import CreateSpectraLogger  # noqa: E402
from spectralog.core.logger import ApplicationLogger  # noqa: E402
from spectralog.core.models import LoggerBuildResult  # noqa: E402
from spectralog.api.logging_control import silence_application_logging  # noqa: E402
from spectralog.api.colored_logger import get_logger  # noqa: E402
from spectralog.core.logger import ApplicationLogger  # noqa: E402
from spectralog.core.models import LoggerBuildResult  # noqa: E402


class UnitTestDisableApplicationLogging(unittest.TestCase):
    def setUp(self) -> None:
        self.previous_application_logger_instance = ApplicationLogger._instance
        ApplicationLogger._instance = None

    def tearDown(self) -> None:
        ApplicationLogger._instance = self.previous_application_logger_instance

    def test_decorator_returns_same_test_class(
        self,
    ) -> None:
        """Verifies that disable_application_logging returns the exact decorated test class."""

        class ExampleTestCase(unittest.TestCase):
            pass

        decorated_test_class = disable_application_logging(
            ExampleTestCase,
        )

        self.assertIs(
            decorated_test_class,
            ExampleTestCase,
            ("Expected disable_application_logging() to return the exact " "test class supplied to the decorator."),
        )

    def test_decorator_replaces_set_up_class_with_classmethod(
        self,
    ) -> None:
        """Verifies that the decorator installs a callable setUpClass implementation on the decorated class."""

        class ExampleTestCase(unittest.TestCase):
            pass

        original_set_up_class = ExampleTestCase.setUpClass

        disable_application_logging(
            ExampleTestCase,
        )

        decorated_set_up_class = ExampleTestCase.setUpClass

        self.assertIsNot(
            decorated_set_up_class,
            original_set_up_class,
            ("Expected the decorator to replace the original setUpClass " "implementation."),
        )

        self.assertTrue(
            callable(decorated_set_up_class),
            "Expected the decorated setUpClass attribute to remain callable.",
        )

    def test_decorator_replaces_tear_down_class_with_classmethod(
        self,
    ) -> None:
        """Verifies that the decorator installs a callable tearDownClass implementation on the decorated class."""

        class ExampleTestCase(unittest.TestCase):
            pass

        original_tear_down_class = ExampleTestCase.tearDownClass

        disable_application_logging(
            ExampleTestCase,
        )

        decorated_tear_down_class = ExampleTestCase.tearDownClass

        self.assertIsNot(
            decorated_tear_down_class,
            original_tear_down_class,
            ("Expected the decorator to replace the original " "tearDownClass implementation."),
        )

        self.assertTrue(
            callable(decorated_tear_down_class),
            "Expected the decorated tearDownClass attribute to remain callable.",
        )

    @patch(
        "spectralog.api.logging_control.patch",
    )
    @patch(
        "spectralog.api.logging_control.logging.getLogger",
    )
    def test_set_up_class_creates_dedicated_disabled_logger(
        self,
        get_logger_mock: MagicMock,
        patch_mock: MagicMock,
    ) -> None:
        """Verifies that class setup requests a dedicated logger derived from the decorated test class identity."""
        disabled_logger = MagicMock(
            spec=logging.Logger,
        )

        disabled_logger.handlers = []

        get_logger_mock.return_value = disabled_logger

        logger_build_patch = MagicMock()
        atexit_register_patch = MagicMock()

        patch_mock.side_effect = [
            logger_build_patch,
            atexit_register_patch,
        ]

        @disable_application_logging
        class ExampleTestCase(unittest.TestCase):
            pass

        ExampleTestCase.setUpClass()

        try:
            expected_logger_name = f"disabled-{ExampleTestCase.__module__}." f"{ExampleTestCase.__name__}"

            get_logger_mock.assert_called_once_with(
                expected_logger_name,
            )
        finally:
            ExampleTestCase.tearDownClass()

    @patch(
        "spectralog.api.logging_control.patch",
    )
    @patch(
        "spectralog.api.logging_control.logging.getLogger",
    )
    def test_set_up_class_disables_logger_and_propagation(
        self,
        get_logger_mock: MagicMock,
        patch_mock: MagicMock,
    ) -> None:
        """Verifies that class setup disables the dedicated logger and prevents propagation."""
        disabled_logger = MagicMock(
            spec=logging.Logger,
        )

        disabled_logger.handlers = []

        get_logger_mock.return_value = disabled_logger

        logger_build_patch = MagicMock()
        atexit_register_patch = MagicMock()

        patch_mock.side_effect = [
            logger_build_patch,
            atexit_register_patch,
        ]

        @disable_application_logging
        class ExampleTestCase(unittest.TestCase):
            pass

        ExampleTestCase.setUpClass()

        try:
            self.assertTrue(
                disabled_logger.disabled,
                "Expected the dedicated test logger to be disabled.",
            )

            self.assertFalse(
                disabled_logger.propagate,
                ("Expected propagation to be disabled for the dedicated " "test logger."),
            )
        finally:
            ExampleTestCase.tearDownClass()

    @patch(
        "spectralog.api.logging_control.patch",
    )
    @patch(
        "spectralog.api.logging_control.logging.getLogger",
    )
    def test_set_up_class_removes_and_closes_existing_handlers(
        self,
        get_logger_mock: MagicMock,
        patch_mock: MagicMock,
    ) -> None:
        """Verifies that class setup removes and closes handlers already attached to the dedicated logger."""
        first_handler = MagicMock(
            spec=logging.Handler,
        )

        second_handler = MagicMock(
            spec=logging.Handler,
        )

        disabled_logger = MagicMock(
            spec=logging.Logger,
        )

        disabled_logger.handlers = [
            first_handler,
            second_handler,
        ]

        get_logger_mock.return_value = disabled_logger

        logger_build_patch = MagicMock()
        atexit_register_patch = MagicMock()

        patch_mock.side_effect = [
            logger_build_patch,
            atexit_register_patch,
        ]

        @disable_application_logging
        class ExampleTestCase(unittest.TestCase):
            pass

        ExampleTestCase.setUpClass()

        try:
            self.assertEqual(
                disabled_logger.removeHandler.call_count,
                2,
                ("Expected every existing handler to be removed from " "the dedicated test logger."),
            )

            disabled_logger.removeHandler.assert_any_call(
                first_handler,
            )

            disabled_logger.removeHandler.assert_any_call(
                second_handler,
            )

            first_handler.close.assert_called_once_with()
            second_handler.close.assert_called_once_with()
        finally:
            ExampleTestCase.tearDownClass()

    @patch(
        "spectralog.api.logging_control.patch",
    )
    @patch(
        "spectralog.api.logging_control.logging.getLogger",
    )
    def test_set_up_class_patches_application_logger_builder_build(
        self,
        get_logger_mock: MagicMock,
        patch_mock: MagicMock,
    ) -> None:
        """Verifies that class setup patches ApplicationLoggerBuilder.build with a disabled LoggerBuildResult."""
        disabled_logger = MagicMock(
            spec=logging.Logger,
        )

        disabled_logger.handlers = []

        get_logger_mock.return_value = disabled_logger

        logger_build_patch = MagicMock()
        atexit_register_patch = MagicMock()

        patch_mock.side_effect = [
            logger_build_patch,
            atexit_register_patch,
        ]

        @disable_application_logging
        class ExampleTestCase(unittest.TestCase):
            pass

        ExampleTestCase.setUpClass()

        try:
            first_patch_call = patch_mock.call_args_list[0]

            self.assertEqual(
                first_patch_call.args[0],
                "spectralog.core.builder.ApplicationLoggerBuilder.build",
                ("Expected class setup to patch " "ApplicationLoggerBuilder.build."),
            )

            logger_build_result = first_patch_call.kwargs["return_value"]

            self.assertIsInstance(
                logger_build_result,
                LoggerBuildResult,
                ("Expected the builder patch to return a " "LoggerBuildResult."),
            )

            self.assertIs(
                logger_build_result.logger,
                disabled_logger,
                ("Expected the patched builder result to contain the " "dedicated disabled logger."),
            )

            self.assertIsNone(
                logger_build_result.log_file_path,
                ("Expected disabled application logging not to expose " "a log file path."),
            )

            self.assertFalse(
                logger_build_result.is_new_log_file,
                ("Expected disabled application logging not to report " "creation of a new log file."),
            )

            self.assertIsNone(
                logger_build_result.multiprocessing_logging_runtime,
                ("Expected disabled application logging not to create " "a multiprocessing logging runtime."),
            )
        finally:
            ExampleTestCase.tearDownClass()

    @patch(
        "spectralog.api.logging_control.patch",
    )
    @patch(
        "spectralog.api.logging_control.logging.getLogger",
    )
    def test_set_up_class_patches_atexit_registration(
        self,
        get_logger_mock: MagicMock,
        patch_mock: MagicMock,
    ) -> None:
        """Verifies that class setup patches ApplicationLogger atexit registration."""
        disabled_logger = MagicMock(
            spec=logging.Logger,
        )

        disabled_logger.handlers = []

        get_logger_mock.return_value = disabled_logger

        logger_build_patch = MagicMock()
        atexit_register_patch = MagicMock()

        patch_mock.side_effect = [
            logger_build_patch,
            atexit_register_patch,
        ]

        @disable_application_logging
        class ExampleTestCase(unittest.TestCase):
            pass

        ExampleTestCase.setUpClass()

        try:
            second_patch_call = patch_mock.call_args_list[1]

            self.assertEqual(
                second_patch_call.args[0],
                "spectralog.core.logger.atexit.register",
                ("Expected class setup to patch ApplicationLogger " "atexit registration."),
            )
        finally:
            ExampleTestCase.tearDownClass()

    @patch(
        "spectralog.api.logging_control.patch",
    )
    @patch(
        "spectralog.api.logging_control.logging.getLogger",
    )
    def test_set_up_class_starts_both_patches(
        self,
        get_logger_mock: MagicMock,
        patch_mock: MagicMock,
    ) -> None:
        """Verifies that class setup starts both logging-related patches before running tests."""
        disabled_logger = MagicMock(
            spec=logging.Logger,
        )

        disabled_logger.handlers = []

        get_logger_mock.return_value = disabled_logger

        logger_build_patch = MagicMock()
        atexit_register_patch = MagicMock()

        patch_mock.side_effect = [
            logger_build_patch,
            atexit_register_patch,
        ]

        @disable_application_logging
        class ExampleTestCase(unittest.TestCase):
            pass

        ExampleTestCase.setUpClass()

        try:
            logger_build_patch.start.assert_called_once_with()
            atexit_register_patch.start.assert_called_once_with()
        finally:
            ExampleTestCase.tearDownClass()

    @patch(
        "spectralog.api.logging_control.patch",
    )
    @patch(
        "spectralog.api.logging_control.logging.getLogger",
    )
    def test_set_up_preserves_previous_application_logger_instance(
        self,
        get_logger_mock: MagicMock,
        patch_mock: MagicMock,
    ) -> None:
        """Verifies that per-test setup preserves and clears the current ApplicationLogger singleton."""
        disabled_logger = MagicMock(
            spec=logging.Logger,
        )

        disabled_logger.handlers = []

        get_logger_mock.return_value = disabled_logger

        logger_build_patch = MagicMock()
        atexit_register_patch = MagicMock()

        patch_mock.side_effect = [
            logger_build_patch,
            atexit_register_patch,
        ]

        previous_application_logger_instance = MagicMock(
            spec=ApplicationLogger,
        )

        ApplicationLogger._instance = previous_application_logger_instance

        @disable_application_logging
        class ExampleTestCase(unittest.TestCase):
            pass

        ExampleTestCase.setUpClass()

        example_test_case = ExampleTestCase(
            methodName="runTest",
        )

        example_test_case.setUp()

        try:
            stored_application_logger_instance = getattr(
                example_test_case,
                "_spectralog_previous_application_logger_instance",
            )

            self.assertIs(
                stored_application_logger_instance,
                previous_application_logger_instance,
                ("Expected per-test setup to preserve the exact " "ApplicationLogger singleton that existed before the test."),
            )

            self.assertIsNone(
                ApplicationLogger._instance,
                ("Expected per-test setup to clear the ApplicationLogger " "singleton before the test executes."),
            )
        finally:
            example_test_case.tearDown()
            ExampleTestCase.tearDownClass()

    @patch(
        "spectralog.api.logging_control.patch",
    )
    @patch(
        "spectralog.api.logging_control.logging.getLogger",
    )
    def test_set_up_class_calls_original_set_up_class(
        self,
        get_logger_mock: MagicMock,
        patch_mock: MagicMock,
    ) -> None:
        """Verifies that the decorated class retains and executes its original setUpClass behavior."""
        disabled_logger = MagicMock(
            spec=logging.Logger,
        )

        disabled_logger.handlers = []

        get_logger_mock.return_value = disabled_logger

        logger_build_patch = MagicMock()
        atexit_register_patch = MagicMock()

        patch_mock.side_effect = [
            logger_build_patch,
            atexit_register_patch,
        ]

        original_set_up_class_mock = MagicMock()

        class ExampleTestCase(unittest.TestCase):
            @classmethod
            def setUpClass(cls) -> None:
                original_set_up_class_mock()

        disable_application_logging(
            ExampleTestCase,
        )

        ExampleTestCase.setUpClass()

        try:
            original_set_up_class_mock.assert_called_once_with()
        finally:
            ExampleTestCase.tearDownClass()

    @patch(
        "spectralog.api.logging_control.patch",
    )
    @patch(
        "spectralog.api.logging_control.logging.getLogger",
    )
    def test_set_up_class_restores_state_when_original_setup_raises(
        self,
        get_logger_mock: MagicMock,
        patch_mock: MagicMock,
    ) -> None:
        """Verifies that failed original class setup restores singleton state and stops started patches."""
        disabled_logger = MagicMock(
            spec=logging.Logger,
        )

        disabled_logger.handlers = []

        get_logger_mock.return_value = disabled_logger

        logger_build_patch = MagicMock()
        atexit_register_patch = MagicMock()

        patch_mock.side_effect = [
            logger_build_patch,
            atexit_register_patch,
        ]

        previous_application_logger_instance = MagicMock(
            spec=ApplicationLogger,
        )

        ApplicationLogger._instance = previous_application_logger_instance

        class ExampleTestCase(unittest.TestCase):
            @classmethod
            def setUpClass(cls) -> None:
                raise RuntimeError(
                    "Setup failed",
                )

        disable_application_logging(
            ExampleTestCase,
        )

        with self.assertRaisesRegex(
            RuntimeError,
            "Setup failed",
            msg=("Expected the original setUpClass exception to propagate " "through the decorator."),
        ):
            ExampleTestCase.setUpClass()

        self.assertIs(
            ApplicationLogger._instance,
            previous_application_logger_instance,
            ("Expected failed setup to restore the previous " "ApplicationLogger singleton."),
        )

        logger_build_patch.stop.assert_called_once_with()
        atexit_register_patch.stop.assert_called_once_with()

    @patch(
        "spectralog.api.logging_control.patch",
    )
    @patch(
        "spectralog.api.logging_control.logging.getLogger",
    )
    def test_tear_down_class_calls_original_tear_down_class(
        self,
        get_logger_mock: MagicMock,
        patch_mock: MagicMock,
    ) -> None:
        """Verifies that decorated teardown executes the original tearDownClass implementation."""
        disabled_logger = MagicMock(
            spec=logging.Logger,
        )

        disabled_logger.handlers = []

        get_logger_mock.return_value = disabled_logger

        logger_build_patch = MagicMock()
        atexit_register_patch = MagicMock()

        patch_mock.side_effect = [
            logger_build_patch,
            atexit_register_patch,
        ]

        original_tear_down_class_mock = MagicMock()

        class ExampleTestCase(unittest.TestCase):
            @classmethod
            def tearDownClass(cls) -> None:
                original_tear_down_class_mock()

        disable_application_logging(
            ExampleTestCase,
        )

        ExampleTestCase.setUpClass()
        ExampleTestCase.tearDownClass()

        original_tear_down_class_mock.assert_called_once_with()

    @patch(
        "spectralog.api.logging_control.patch",
    )
    @patch(
        "spectralog.api.logging_control.logging.getLogger",
    )
    def test_tear_down_class_stops_both_patches(
        self,
        get_logger_mock: MagicMock,
        patch_mock: MagicMock,
    ) -> None:
        """Verifies that class teardown stops both patches installed during setup."""
        disabled_logger = MagicMock(
            spec=logging.Logger,
        )

        disabled_logger.handlers = []

        get_logger_mock.return_value = disabled_logger

        logger_build_patch = MagicMock()
        atexit_register_patch = MagicMock()

        patch_mock.side_effect = [
            logger_build_patch,
            atexit_register_patch,
        ]

        @disable_application_logging
        class ExampleTestCase(unittest.TestCase):
            pass

        ExampleTestCase.setUpClass()
        ExampleTestCase.tearDownClass()

        logger_build_patch.stop.assert_called_once_with()
        atexit_register_patch.stop.assert_called_once_with()

    @patch(
    "spectralog.api.logging_control.ApplicationLogger.get_instance",
    )
    def test_decorator_allows_application_logger_usage_without_real_logging_side_effects(
        self,
        get_instance_mock: MagicMock,
    ) -> None:
        """Verifies that application code may still request and use ApplicationLogger while logging infrastructure is disabled."""
        application_logger = MagicMock(
            spec=ApplicationLogger,
        )

        get_instance_mock.return_value = application_logger

        @disable_application_logging
        class ExampleTestCase(unittest.TestCase):
            pass

        example_test_case = ExampleTestCase()

        ExampleTestCase.setUpClass()

        try:
            example_test_case.setUp()

            try:
                resolved_application_logger = ApplicationLogger.get_instance()

                resolved_application_logger.info(
                    "Application message",
                )

                application_logger.info.assert_called_once_with(
                    "Application message",
                )
            finally:
                example_test_case.tearDown()
        finally:
            ExampleTestCase.tearDownClass()

    @patch(
        "spectralog.api.logging_control.patch",
    )
    @patch(
        "spectralog.api.logging_control.logging.getLogger",
    )
    def test_tear_down_shuts_down_current_application_logger(
        self,
        get_logger_mock: MagicMock,
        patch_mock: MagicMock,
    ) -> None:
        """Verifies that per-test teardown shuts down an ApplicationLogger instance created during the test."""
        disabled_logger = MagicMock(
            spec=logging.Logger,
        )

        disabled_logger.handlers = []

        get_logger_mock.return_value = disabled_logger

        logger_build_patch = MagicMock()
        atexit_register_patch = MagicMock()

        patch_mock.side_effect = [
            logger_build_patch,
            atexit_register_patch,
        ]

        @disable_application_logging
        class ExampleTestCase(unittest.TestCase):
            pass

        ExampleTestCase.setUpClass()

        example_test_case = ExampleTestCase(
            methodName="runTest",
        )

        example_test_case.setUp()

        current_application_logger_instance = MagicMock(
            spec=ApplicationLogger,
        )

        ApplicationLogger._instance = current_application_logger_instance

        try:
            example_test_case.tearDown()

            current_application_logger_instance.shutdown.assert_called_once_with()
        finally:
            ExampleTestCase.tearDownClass()

    @patch(
        "spectralog.api.logging_control.patch",
    )
    @patch(
        "spectralog.api.logging_control.logging.getLogger",
    )
    def test_tear_down_restores_previous_application_logger_instance(
        self,
        get_logger_mock: MagicMock,
        patch_mock: MagicMock,
    ) -> None:
        """Verifies that per-test teardown restores the ApplicationLogger singleton that existed before the test."""
        disabled_logger = MagicMock(
            spec=logging.Logger,
        )

        disabled_logger.handlers = []

        get_logger_mock.return_value = disabled_logger

        logger_build_patch = MagicMock()
        atexit_register_patch = MagicMock()

        patch_mock.side_effect = [
            logger_build_patch,
            atexit_register_patch,
        ]

        previous_application_logger_instance = MagicMock(
            spec=ApplicationLogger,
        )

        ApplicationLogger._instance = previous_application_logger_instance

        @disable_application_logging
        class ExampleTestCase(unittest.TestCase):
            pass

        ExampleTestCase.setUpClass()

        example_test_case = ExampleTestCase(
            methodName="runTest",
        )

        example_test_case.setUp()

        current_application_logger_instance = MagicMock(
            spec=ApplicationLogger,
        )

        ApplicationLogger._instance = current_application_logger_instance

        try:
            example_test_case.tearDown()

            self.assertIs(
                ApplicationLogger._instance,
                previous_application_logger_instance,
                ("Expected per-test teardown to restore the exact " "ApplicationLogger singleton that existed before setup."),
            )
        finally:
            ExampleTestCase.tearDownClass()


    def test_decorator_creates_disabled_fallback_logger_when_get_logger_is_called_before_initialization(
    self,
    ) -> None:
        """Verifies that get_logger returns a disabled fallback logger before explicit initialization."""

        @disable_application_logging
        class ExampleTestCase(unittest.TestCase):
            pass

        example_test_case = ExampleTestCase()

        ExampleTestCase.setUpClass()

        try:
            example_test_case.setUp()

            try:
                application_logger = ApplicationLogger.get_instance()

                self.assertTrue(
                    application_logger._logger.disabled,
                    "Expected the fallback logger to be disabled.",
                )

                self.assertEqual(
                    [],
                    application_logger._logger.handlers,
                    "Expected the fallback logger to have no handlers.",
                )

                self.assertFalse(
                    application_logger._logger.propagate,
                    "Expected the fallback logger not to propagate records.",
                )
            finally:
                example_test_case.tearDown()
        finally:
            ExampleTestCase.tearDownClass()
            
    def test_decorator_allows_explicit_initialization_after_fallback_logger_creation(
        self,
    ) -> None:
        """Verifies that explicit initialization replaces the temporary fallback logger."""

        @disable_application_logging
        class ExampleTestCase(unittest.TestCase):
            pass

        example_test_case = ExampleTestCase()

        ExampleTestCase.setUpClass()

        try:
            example_test_case.setUp()

            try:
                fallback_logger = ApplicationLogger.get_instance()

                configured_logger = CreateSpectraLogger(
                    debug_mode=True,
                )

                self.assertIsNot(
                    configured_logger,
                    fallback_logger,
                    "Expected explicit initialization to replace the fallback logger.",
                )

                self.assertIs(
                    ApplicationLogger._instance,
                    configured_logger,
                    "Expected the explicitly initialized logger to become the active singleton.",
                )
            finally:
                example_test_case.tearDown()
        finally:
            ExampleTestCase.tearDownClass()
                
    def test_silence_application_logging_preserves_function_return_value(
        self,
    ) -> None:
        """Verifies that silence_application_logging preserves the decorated function return value."""

        @silence_application_logging
        def example_function() -> int:
            return 42

        returned_value = example_function()

        self.assertEqual(
            returned_value,
            42,
            (
                "Expected silence_application_logging to preserve the "
                "decorated function return value."
            ),
        )


    def test_silence_application_logging_allows_get_logger_without_initialization(
        self,
    ) -> None:
        """Verifies that get_logger can be used without explicit initialization while logging is silenced."""

        @silence_application_logging
        def example_function() -> ApplicationLogger:
            application_logger = get_logger()

            application_logger.info(
                "Silenced message",
            )

            return application_logger

        application_logger = example_function()

        self.assertTrue(
            application_logger._logger.disabled,
            "Expected the silenced fallback logger to be disabled.",
        )

        self.assertEqual(
            application_logger._logger.handlers,
            [],
            "Expected the silenced fallback logger to contain no handlers.",
        )

        self.assertFalse(
            application_logger._logger.propagate,
            "Expected the silenced fallback logger not to propagate records.",
        )


    def test_silence_application_logging_prevents_log_file_creation(
        self,
    ) -> None:
        """Verifies that silence_application_logging prevents explicit initialization from creating a log file."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            logs_directory = (
                Path(
                    temporary_directory,
                )
                / "logs"
            )

            @silence_application_logging
            def example_function() -> None:
                application_logger = CreateSpectraLogger(
                    logs_directory=logs_directory,
                    log_file_name="silenced.log",
                    save_logs=True,
                )

                application_logger.info(
                    "This message must not create a log file.",
                )

            example_function()

            self.assertFalse(
                logs_directory.exists(),
                (
                    "Expected silence_application_logging to prevent "
                    "creation of the configured logs directory."
                ),
            )


    def test_silence_application_logging_allows_explicit_initialization_after_fallback_logger(
        self,
    ) -> None:
        """Verifies that explicit initialization replaces a temporary silenced fallback logger."""

        fallback_application_logger: ApplicationLogger | None = None
        configured_application_logger: ApplicationLogger | None = None

        @silence_application_logging
        def example_function() -> None:
            nonlocal fallback_application_logger
            nonlocal configured_application_logger

            fallback_application_logger = get_logger()

            configured_application_logger = CreateSpectraLogger(
                debug_mode=True,
                save_logs=False,
            )

        example_function()

        self.assertIsNotNone(
            fallback_application_logger,
            "Expected get_logger to create a temporary fallback logger.",
        )

        self.assertIsNotNone(
            configured_application_logger,
            (
                "Expected CreateSpectraLogger to initialize a logger "
                "after fallback creation."
            ),
        )

        self.assertIsNot(
            configured_application_logger,
            fallback_application_logger,
            (
                "Expected explicit initialization to replace the "
                "temporary fallback logger."
            ),
        )


    def test_silence_application_logging_restores_previous_singleton(
        self,
    ) -> None:
        """Verifies that silence_application_logging restores the previous ApplicationLogger singleton."""
        previous_application_logger_instance = MagicMock(
            spec=ApplicationLogger,
        )

        previous_standard_logger = MagicMock(
            spec=logging.Logger,
        )

        previous_standard_logger.disabled = False
        previous_application_logger_instance._logger = previous_standard_logger

        ApplicationLogger._instance = previous_application_logger_instance

        @silence_application_logging
        def example_function() -> None:
            self.assertIsNot(
                ApplicationLogger._instance,
                previous_application_logger_instance,
                (
                    "Expected the previous ApplicationLogger singleton to "
                    "be isolated during the decorated function."
                ),
            )

        example_function()

        self.assertIs(
            ApplicationLogger._instance,
            previous_application_logger_instance,
            (
                "Expected silence_application_logging to restore the "
                "previous ApplicationLogger singleton."
            ),
        )


    def test_silence_application_logging_restores_state_when_function_raises(
        self,
    ) -> None:
        """Verifies that silence_application_logging restores logger state when the decorated function raises."""
        previous_application_logger_instance = MagicMock(
            spec=ApplicationLogger,
        )

        previous_standard_logger = MagicMock(
            spec=logging.Logger,
        )

        previous_standard_logger.disabled = False
        previous_application_logger_instance._logger = previous_standard_logger

        ApplicationLogger._instance = previous_application_logger_instance

        @silence_application_logging
        def example_function() -> None:
            raise RuntimeError(
                "Function failed",
            )

        with self.assertRaisesRegex(
            RuntimeError,
            "Function failed",
            msg=(
                "Expected the decorated function exception to propagate "
                "through silence_application_logging."
            ),
        ):
            example_function()

        self.assertIs(
            ApplicationLogger._instance,
            previous_application_logger_instance,
            (
                "Expected the previous ApplicationLogger singleton to be "
                "restored after the decorated function raised."
            ),
        )

        self.assertFalse(
            previous_standard_logger.disabled,
            (
                "Expected the previous logger disabled state to be "
                "restored after the decorated function raised."
            ),
        )


    def test_silence_application_logging_supports_instance_methods(
        self,
    ) -> None:
        """Verifies that silence_application_logging can decorate an instance method."""

        class ExampleService:
            @silence_application_logging
            def execute(
                self,
                message: str,
            ) -> str:
                application_logger = get_logger()

                application_logger.info(
                    message,
                )

                return message

        example_service = ExampleService()

        returned_message = example_service.execute(
            "Silenced method message",
        )

        self.assertEqual(
            returned_message,
            "Silenced method message",
            (
                "Expected silence_application_logging to preserve "
                "instance method arguments and return values."
            ),
        )