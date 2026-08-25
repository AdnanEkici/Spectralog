from __future__ import annotations

import logging
import unittest
from typing import TypeVar
from unittest.mock import patch

from spectralog.core.logger import ApplicationLogger
from spectralog.core.models import LoggerBuildResult


TestCaseClass = TypeVar(
    "TestCaseClass",
    bound=type[unittest.TestCase],
)


def disable_application_logging(
    test_class: TestCaseClass,
) -> TestCaseClass:
    """Disable SpectraLog output and logging side effects for a unittest class.

    This decorator is intended for test suites that exercise application code
    which initializes or retrieves SpectraLog through its normal public API, but
    where actual logging infrastructure is undesirable.

    While the decorated test class runs, SpectraLog's logger builder is replaced
    with a build result containing a disabled standard-library logger. The
    disabled logger has no active handlers, does not propagate records, does not
    create log files, and does not initialize a multiprocessing logging runtime.

    The decorator also suppresses SpectraLog's ``atexit`` registration so that
    test execution does not accumulate shutdown callbacks.

    Logging infrastructure is disabled for the lifetime of the decorated test
    class, while the :class:`ApplicationLogger` singleton is isolated separately
    for each individual test method. Before each test, the current singleton
    instance is preserved and cleared. After each test, any logger created during
    that test is shut down and the previously existing singleton is restored.

    Existing ``setUpClass``, ``tearDownClass``, ``setUp``, and ``tearDown``
    implementations on the decorated test class are preserved and invoked as part
    of the wrapped lifecycle. Logging patches are also cleaned up if class setup
    fails, and singleton state is restored if per-test setup fails.

    Application code may continue to call :func:`CreateSpectraLogger`,
    :func:`get_logger`, and normal logging methods while this decorator is active.
    Those calls operate against a valid :class:`ApplicationLogger`, but no
    SpectraLog console, file, Rich, syslog, or multiprocessing output is produced.

    Args:
        test_class:
            The :class:`unittest.TestCase` subclass for which SpectraLog output
            and logging side effects should be disabled.

    Returns:
        TestCaseClass:
            The same test class with wrapped class-level and per-test lifecycle
            methods that manage disabled logging and singleton isolation.

    Example:
        Apply the decorator directly to a unittest class::

            import unittest

            from spectralog import CreateSpectraLogger
            from spectralog import disable_application_logging
            from spectralog import get_logger


            @disable_application_logging
            class UnitTestExperimentService(unittest.TestCase):
                def test_experiment_execution(self) -> None:
                    CreateSpectraLogger(
                        log_file_name="application.log",
                        save_logs=True,
                    )

                    logger = get_logger()
                    logger.info("Experiment started")

                    self.assertTrue(True)

        The application may initialize and use SpectraLog normally inside the
        test, but no log file or other logging infrastructure is created.

    Note:
        The decorator is designed specifically for
        :class:`unittest.TestCase` subclasses.

        Singleton isolation occurs per test method rather than only once per test
        class. This allows multiple tests in the same decorated class to call
        :func:`CreateSpectraLogger` independently without triggering SpectraLog's
        reconfiguration protection.
    """
    original_set_up_class = test_class.setUpClass
    original_tear_down_class = test_class.tearDownClass
    original_set_up = test_class.setUp
    original_tear_down = test_class.tearDown

    def set_up_class(
        cls: type[unittest.TestCase],
    ) -> None:
        disabled_logger = logging.getLogger(
            f"disabled-{cls.__module__}.{cls.__name__}",
        )

        existing_handlers = list(
            disabled_logger.handlers,
        )

        for existing_handler in existing_handlers:
            disabled_logger.removeHandler(
                existing_handler,
            )

            existing_handler.close()

        disabled_logger.disabled = True
        disabled_logger.propagate = False

        disabled_logger_build_result = LoggerBuildResult(
            logger=disabled_logger,
            log_file_path=None,
            is_new_log_file=False,
            multiprocessing_logging_runtime=None,
        )

        logger_build_patch = patch(
            "spectralog.core.builder.ApplicationLoggerBuilder.build",
            return_value=disabled_logger_build_result,
        )

        atexit_register_patch = patch(
            "spectralog.core.logger.atexit.register",
        )

        logger_build_patch.start()
        atexit_register_patch.start()

        setattr(
            cls,
            "_spectralog_logger_build_patch",
            logger_build_patch,
        )

        setattr(
            cls,
            "_spectralog_atexit_register_patch",
            atexit_register_patch,
        )

        try:
            original_set_up_class()
        except Exception:
            atexit_register_patch.stop()
            logger_build_patch.stop()

            raise

    def tear_down_class(
        cls: type[unittest.TestCase],
    ) -> None:
        logger_build_patch = getattr(
            cls,
            "_spectralog_logger_build_patch",
        )

        atexit_register_patch = getattr(
            cls,
            "_spectralog_atexit_register_patch",
        )

        try:
            original_tear_down_class()
        finally:
            atexit_register_patch.stop()
            logger_build_patch.stop()

    def set_up(
        self: unittest.TestCase,
    ) -> None:
        previous_application_logger_instance = ApplicationLogger._instance

        setattr(
            self,
            "_spectralog_previous_application_logger_instance",
            previous_application_logger_instance,
        )

        ApplicationLogger._instance = None

        try:
            original_set_up(self)
        except Exception:
            ApplicationLogger._instance = previous_application_logger_instance

            raise

    def tear_down(
        self: unittest.TestCase,
    ) -> None:
        previous_application_logger_instance = getattr(
            self,
            "_spectralog_previous_application_logger_instance",
        )

        try:
            original_tear_down(self)
        finally:
            current_application_logger_instance = ApplicationLogger._instance

            if current_application_logger_instance is not None:
                current_application_logger_instance.shutdown()

            ApplicationLogger._instance = previous_application_logger_instance

    setattr(
        test_class,
        "setUpClass",
        classmethod(
            set_up_class,
        ),
    )

    setattr(
        test_class,
        "tearDownClass",
        classmethod(
            tear_down_class,
        ),
    )

    setattr(
        test_class,
        "setUp",
        set_up,
    )

    setattr(
        test_class,
        "tearDown",
        tear_down,
    )

    decorated_test_class = test_class

    return decorated_test_class
