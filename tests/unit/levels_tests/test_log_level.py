from __future__ import annotations

import logging
import sys
import unittest
from pathlib import Path
from typing import Any
from unittest.mock import patch

import colorlog

PROJECT_ROOT = Path(__file__).resolve().parents[3]  # noqa
SRC_DIR = PROJECT_ROOT / "src"  # noqa
sys.path.insert(0, str(SRC_DIR))  # noqa

from spectralog.configuration.colors import LoggerColor  # noqa: E402
from spectralog.exceptions.exceptions import InvalidSpectraLogColorError  # noqa: E402
from spectralog.exceptions.exceptions import InvalidSpectraLogLevelNameError  # noqa: E402
from spectralog.exceptions.exceptions import InvalidSpectraLogLevelSeverityError  # noqa: E402
from spectralog.exceptions.exceptions import SpectraLogLevelAlreadyExistsError  # noqa: E402
from spectralog.exceptions.exceptions import SpectraLogLevelNotFoundError  # noqa: E402
from spectralog.levels.log_level import LogLevel  # noqa: E402
from spectralog.levels.log_level_registry import LogLevelRegistry  # noqa: E402


class UnitTestLogLevelRegistry(unittest.TestCase):
    def setUp(self) -> None:
        self.log_level_registry = LogLevelRegistry()

    def test_initialization_registers_all_default_log_levels(self) -> None:
        """Verifies that a newly created registry contains every supported default logging level."""
        expected_log_levels = {
            "DEBUG": LogLevel(
                name="DEBUG",
                severity=logging.DEBUG,
                color=LoggerColor.DEBUG.value,
            ),
            "INFO": LogLevel(
                name="INFO",
                severity=logging.INFO,
                color=LoggerColor.INFO.value,
            ),
            "WARNING": LogLevel(
                name="WARNING",
                severity=logging.WARNING,
                color=LoggerColor.WARNING.value,
            ),
            "ERROR": LogLevel(
                name="ERROR",
                severity=logging.ERROR,
                color=LoggerColor.ERROR.value,
            ),
            "CRITICAL": LogLevel(
                name="CRITICAL",
                severity=logging.CRITICAL,
                color=LoggerColor.CRITICAL.value,
            ),
        }

        for log_level_name, expected_log_level in expected_log_levels.items():
            with self.subTest(log_level_name=log_level_name):
                actual_log_level = self.log_level_registry.get(
                    log_level_name,
                )

                self.assertEqual(
                    actual_log_level,
                    expected_log_level,
                    (f"Expected default log level '{log_level_name}' to be " f"{expected_log_level}, but received {actual_log_level}."),
                )

    def test_colors_returns_mapping_for_all_default_log_levels(self) -> None:
        """Verifies that the colors property exposes the configured color for every default log level."""
        expected_colors = {
            "DEBUG": LoggerColor.DEBUG.value,
            "INFO": LoggerColor.INFO.value,
            "WARNING": LoggerColor.WARNING.value,
            "ERROR": LoggerColor.ERROR.value,
            "CRITICAL": LoggerColor.CRITICAL.value,
        }

        actual_colors = self.log_level_registry.colors

        self.assertEqual(
            actual_colors,
            expected_colors,
            ("Expected the default color mapping to equal " f"{expected_colors}, but received {actual_colors}."),
        )

    def test_colors_returns_new_dictionary_on_each_access(self) -> None:
        """Verifies that modifying a returned color mapping cannot mutate the registry's internal state."""
        first_colors = self.log_level_registry.colors
        first_colors["INFO"] = "blue"

        second_colors = self.log_level_registry.colors

        self.assertEqual(
            second_colors["INFO"],
            LoggerColor.INFO.value,
            ("Expected modifying a previously returned color mapping not to " "change the registry's internal INFO color."),
        )

        self.assertIsNot(
            first_colors,
            second_colors,
            "Expected each colors property access to return a new dictionary instance.",
        )

    @patch("src.spectralog.levels.log_level_registry.logging.addLevelName")
    def test_register_adds_valid_custom_log_level(
        self,
        add_level_name_mock,
    ) -> None:
        """Verifies that registering a valid custom level stores it and registers its name with Python logging."""
        custom_log_level_name = "SUCCESS"
        custom_log_level_color = "green"
        custom_log_level_severity = 25

        registered_log_level = self.log_level_registry.register(
            name=custom_log_level_name,
            color=custom_log_level_color,
            severity=custom_log_level_severity,
        )

        expected_log_level = LogLevel(
            name=custom_log_level_name,
            severity=custom_log_level_severity,
            color=custom_log_level_color,
        )

        self.assertEqual(
            registered_log_level,
            expected_log_level,
            (f"Expected registered log level to equal {expected_log_level}, " f"but received {registered_log_level}."),
        )

        add_level_name_mock.assert_called_once_with(
            custom_log_level_severity,
            custom_log_level_name,
        )

        stored_log_level = self.log_level_registry.get(
            custom_log_level_name,
        )

        self.assertEqual(
            stored_log_level,
            expected_log_level,
            (f"Expected custom level '{custom_log_level_name}' to be stored " f"as {expected_log_level}, but received {stored_log_level}."),
        )

    @patch("src.spectralog.levels.log_level_registry.logging.addLevelName")
    def test_register_normalizes_custom_log_level_name(
        self,
        add_level_name_mock,
    ) -> None:
        """Verifies that custom level names are stripped of surrounding whitespace and converted to uppercase."""
        supplied_log_level_name = "  success  "
        expected_log_level_name = "SUCCESS"
        custom_log_level_severity = 25

        registered_log_level = self.log_level_registry.register(
            name=supplied_log_level_name,
            color="green",
            severity=custom_log_level_severity,
        )

        self.assertEqual(
            registered_log_level.name,
            expected_log_level_name,
            (
                f"Expected '{supplied_log_level_name}' to normalize to "
                f"'{expected_log_level_name}', but received "
                f"'{registered_log_level.name}'."
            ),
        )

        add_level_name_mock.assert_called_once_with(
            custom_log_level_severity,
            expected_log_level_name,
        )

    @patch("src.spectralog.levels.log_level_registry.logging.addLevelName")
    def test_register_updates_color_mapping_with_custom_log_level(
        self,
        add_level_name_mock,
    ) -> None:
        """Verifies that registering a custom log level makes its color available through the colors property."""
        custom_log_level_name = "SUCCESS"
        custom_log_level_color = "green"

        self.log_level_registry.register(
            name=custom_log_level_name,
            color=custom_log_level_color,
            severity=25,
        )

        actual_colors = self.log_level_registry.colors

        self.assertIn(
            custom_log_level_name,
            actual_colors,
            (
                f"Expected custom log level '{custom_log_level_name}' to appear "
                f"in the color mapping, but available levels were {list(actual_colors)}."
            ),
        )

        self.assertEqual(
            actual_colors[custom_log_level_name],
            custom_log_level_color,
            (
                f"Expected custom log level '{custom_log_level_name}' to use color "
                f"'{custom_log_level_color}', but received "
                f"'{actual_colors[custom_log_level_name]}'."
            ),
        )

        add_level_name_mock.assert_called_once()

    def test_get_returns_default_log_level_case_insensitively(self) -> None:
        """Verifies that retrieving a default log level is insensitive to letter casing and surrounding whitespace."""
        supplied_names = (
            "info",
            "INFO",
            "Info",
            "  info  ",
        )

        for supplied_name in supplied_names:
            with self.subTest(supplied_name=supplied_name):
                resolved_log_level = self.log_level_registry.get(
                    supplied_name,
                )

                self.assertEqual(
                    resolved_log_level.name,
                    "INFO",
                    (f"Expected supplied name '{supplied_name}' to resolve to " f"'INFO', but received '{resolved_log_level.name}'."),
                )

    def test_get_raises_when_log_level_is_not_registered(self) -> None:
        """Verifies that requesting an unknown log level raises SpectraLogLevelNotFoundError with the normalized name."""
        unknown_log_level_name = "unknown"

        with self.assertRaisesRegex(
            SpectraLogLevelNotFoundError,
            "Log level 'UNKNOWN' is not registered",
        ):
            self.log_level_registry.get(
                unknown_log_level_name,
            )

    def test_contains_returns_true_for_registered_log_level(self) -> None:
        """Verifies that contains returns True for a registered level regardless of casing or surrounding whitespace."""
        supplied_names = (
            "debug",
            " DEBUG ",
            "DeBuG",
        )

        for supplied_name in supplied_names:
            with self.subTest(supplied_name=supplied_name):
                contains_log_level = self.log_level_registry.contains(
                    supplied_name,
                )

                self.assertTrue(
                    contains_log_level,
                    (f"Expected contains('{supplied_name}') to return True " "because DEBUG is registered."),
                )

    def test_contains_returns_false_for_unregistered_log_level(self) -> None:
        """Verifies that contains returns False when the requested log level has not been registered."""
        unknown_log_level_name = "SUCCESS"

        contains_log_level = self.log_level_registry.contains(
            unknown_log_level_name,
        )

        self.assertFalse(
            contains_log_level,
            (f"Expected contains('{unknown_log_level_name}') to return False " "because the level has not been registered."),
        )

    def test_register_rejects_empty_log_level_name(self) -> None:
        """Verifies that empty and whitespace-only log level names are rejected."""
        invalid_names = (
            "",
            " ",
            "   ",
            "\t",
            "\n",
        )

        for invalid_name in invalid_names:
            with self.subTest(invalid_name=repr(invalid_name)):
                with self.assertRaisesRegex(
                    InvalidSpectraLogLevelNameError,
                    "Log level name cannot be empty",
                ):
                    self.log_level_registry.register(
                        name=invalid_name,
                        color="green",
                        severity=25,
                    )

    def test_register_rejects_invalid_log_level_name_patterns(self) -> None:
        """Verifies that log level names containing unsupported syntax are rejected."""
        invalid_names = (
            "1SUCCESS",
            "_SUCCESS",
            "SUCCESS-LEVEL",
            "SUCCESS LEVEL",
            "SUCCESS.LEVEL",
            "SUCCESS/LEVEL",
            "SUCCESS@LEVEL",
            "SUCCESS!",
        )

        for invalid_name in invalid_names:
            with self.subTest(invalid_name=invalid_name):
                with self.assertRaisesRegex(
                    InvalidSpectraLogLevelNameError,
                    "Log level name must start with a letter",
                ):
                    self.log_level_registry.register(
                        name=invalid_name,
                        color="green",
                        severity=25,
                    )

    @patch("src.spectralog.levels.log_level_registry.logging.addLevelName")
    def test_register_accepts_valid_log_level_name_patterns(
        self,
        add_level_name_mock,
    ) -> None:
        """Verifies that supported combinations of letters, numbers, and underscores can be registered as custom levels."""
        valid_log_levels = (
            ("SUCCESS", 21),
            ("SUCCESS_2", 22),
            ("LEVEL123", 23),
            ("CUSTOM_LEVEL_4", 24),
        )

        for valid_name, severity in valid_log_levels:
            with self.subTest(
                valid_name=valid_name,
                severity=severity,
            ):
                registered_log_level = self.log_level_registry.register(
                    name=valid_name,
                    color="green",
                    severity=severity,
                )

                self.assertEqual(
                    registered_log_level.name,
                    valid_name,
                    (f"Expected valid log level name '{valid_name}' to be " f"registered unchanged, but received " f"'{registered_log_level.name}'."),
                )

        self.assertEqual(
            add_level_name_mock.call_count,
            len(valid_log_levels),
            (
                f"Expected logging.addLevelName to be called "
                f"{len(valid_log_levels)} times, but it was called "
                f"{add_level_name_mock.call_count} times."
            ),
        )

    def test_register_rejects_unsupported_color(self) -> None:
        """Verifies that a color not supported by colorlog is rejected before the log level is registered."""
        unsupported_color = "definitely_not_a_real_color"

        with self.assertRaisesRegex(
            InvalidSpectraLogColorError,
            f"Unsupported logger color '{unsupported_color}'",
        ):
            self.log_level_registry.register(
                name="SUCCESS",
                color=unsupported_color,
                severity=25,
            )

    @patch("src.spectralog.levels.log_level_registry.logging.addLevelName")
    def test_register_accepts_supported_colorlog_colors(
        self,
        add_level_name_mock,
    ) -> None:
        """Verifies that representative colors provided by colorlog can be used for custom levels."""
        supported_colors = (
            "red",
            "green",
            "blue",
            "cyan",
            "purple",
            "bold_red",
            "bold_green",
            "bold_yellow",
        )

        available_colors = set(
            colorlog.escape_codes.escape_codes,
        )

        next_severity = 21

        for supported_color in supported_colors:
            if supported_color not in available_colors:
                continue

            with self.subTest(supported_color=supported_color):
                log_level_name = supported_color.replace("-", "_").upper()

                registered_log_level = self.log_level_registry.register(
                    name=log_level_name,
                    color=supported_color,
                    severity=next_severity,
                )

                self.assertEqual(
                    registered_log_level.color,
                    supported_color,
                    (f"Expected color '{supported_color}' to be accepted, " f"but the registered color was " f"'{registered_log_level.color}'."),
                )

                next_severity += 1

        self.assertGreater(
            add_level_name_mock.call_count,
            0,
            "Expected at least one supported colorlog color to be registered.",
        )

    def test_register_rejects_boolean_severity(self) -> None:
        """Verifies that boolean values are rejected even though bool is a subclass of int in Python."""
        boolean_severities = (
            True,
            False,
        )

        for boolean_severity in boolean_severities:
            with self.subTest(
                boolean_severity=boolean_severity,
            ):
                with self.assertRaisesRegex(
                    InvalidSpectraLogLevelSeverityError,
                    "Log level severity must be an integer",
                ):
                    self.log_level_registry.register(
                        name="SUCCESS",
                        color="green",
                        severity=boolean_severity,
                    )

    def test_register_rejects_non_integer_severity(self) -> None:
        """Verifies that severity values whose runtime type is not int are rejected."""
        invalid_severities: tuple = (
            25.0,
            "25",
            None,
            [],
            {},
        )

        for invalid_severity in invalid_severities:
            with self.subTest(
                invalid_severity=invalid_severity,
            ):
                with self.assertRaisesRegex(
                    InvalidSpectraLogLevelSeverityError,
                    "Log level severity must be an integer",
                ):
                    self.log_level_registry.register(
                        name="SUCCESS",
                        color="green",
                        severity=invalid_severity,
                    )

    def test_register_rejects_zero_and_negative_severity(self) -> None:
        """Verifies that custom log levels must use a positive numeric severity."""
        invalid_severities = (
            0,
            -1,
            -10,
            -100,
        )

        for invalid_severity in invalid_severities:
            with self.subTest(
                invalid_severity=invalid_severity,
            ):
                with self.assertRaisesRegex(
                    InvalidSpectraLogLevelSeverityError,
                    "Log level severity must be greater than zero",
                ):
                    self.log_level_registry.register(
                        name="SUCCESS",
                        color="green",
                        severity=invalid_severity,
                    )

    @patch("src.spectralog.levels.log_level_registry.logging.addLevelName")
    def test_register_accepts_positive_integer_severity(
        self,
        add_level_name_mock,
    ) -> None:
        """Verifies that a positive unused integer severity can be assigned to a custom log level."""
        custom_log_level_severity = 25

        registered_log_level = self.log_level_registry.register(
            name="SUCCESS",
            color="green",
            severity=custom_log_level_severity,
        )

        self.assertEqual(
            registered_log_level.severity,
            custom_log_level_severity,
            (f"Expected severity {custom_log_level_severity}, but received " f"{registered_log_level.severity}."),
        )

        add_level_name_mock.assert_called_once_with(
            custom_log_level_severity,
            "SUCCESS",
        )

    def test_register_rejects_duplicate_default_log_level_name(self) -> None:
        """Verifies that a custom registration cannot replace an existing default log level by name."""
        duplicate_log_level_name = "INFO"

        with self.assertRaisesRegex(
            SpectraLogLevelAlreadyExistsError,
            "Log level 'INFO' already exists",
        ):
            self.log_level_registry.register(
                name=duplicate_log_level_name,
                color="blue",
                severity=25,
            )

    def test_register_rejects_duplicate_custom_log_level_name(self) -> None:
        """Verifies that registering the same custom log level name more than once is rejected."""
        with patch(
            "src.spectralog.levels.log_level_registry.logging.addLevelName",
        ):
            self.log_level_registry.register(
                name="SUCCESS",
                color="green",
                severity=25,
            )

        with self.assertRaisesRegex(
            SpectraLogLevelAlreadyExistsError,
            "Log level 'SUCCESS' already exists",
        ):
            self.log_level_registry.register(
                name="success",
                color="blue",
                severity=26,
            )

    def test_register_rejects_severity_used_by_default_log_level(self) -> None:
        """Verifies that a custom log level cannot reuse the numeric severity assigned to a default level."""
        duplicate_severity = logging.INFO

        with self.assertRaisesRegex(
            SpectraLogLevelAlreadyExistsError,
            "Log level severity '20' is already assigned to 'INFO'",
        ):
            self.log_level_registry.register(
                name="SUCCESS",
                color="green",
                severity=duplicate_severity,
            )

    def test_register_rejects_severity_used_by_custom_log_level(self) -> None:
        """Verifies that two custom log levels cannot share the same numeric severity."""
        duplicate_severity = 25

        with patch(
            "src.spectralog.levels.log_level_registry.logging.addLevelName",
        ):
            self.log_level_registry.register(
                name="SUCCESS",
                color="green",
                severity=duplicate_severity,
            )

        with self.assertRaisesRegex(
            SpectraLogLevelAlreadyExistsError,
            "Log level severity '25' is already assigned to 'SUCCESS'",
        ):
            self.log_level_registry.register(
                name="NOTICE",
                color="blue",
                severity=duplicate_severity,
            )

    @patch("src.spectralog.levels.log_level_registry.logging.addLevelName")
    def test_failed_registration_does_not_call_logging_add_level_name(
        self,
        add_level_name_mock,
    ) -> None:
        """Verifies that Python's global logging level registry is not modified when registration validation fails."""
        invalid_registration_cases: tuple[dict[str, Any], ...] = (
            {
                "name": "",
                "color": "green",
                "severity": 25,
            },
            {
                "name": "SUCCESS",
                "color": "invalid_color",
                "severity": 25,
            },
            {
                "name": "SUCCESS",
                "color": "green",
                "severity": 0,
            },
            {
                "name": "INFO",
                "color": "green",
                "severity": 25,
            },
        )

        for registration_case in invalid_registration_cases:
            with self.subTest(
                registration_case=registration_case,
            ):
                with self.assertRaises(
                    (
                        InvalidSpectraLogLevelNameError,
                        InvalidSpectraLogColorError,
                        InvalidSpectraLogLevelSeverityError,
                        SpectraLogLevelAlreadyExistsError,
                    ),
                ):
                    self.log_level_registry.register(
                        name=registration_case["name"],
                        color=registration_case["color"],
                        severity=registration_case["severity"],
                    )

        add_level_name_mock.assert_not_called()

    @patch("src.spectralog.levels.log_level_registry.logging.addLevelName")
    def test_get_returns_same_log_level_created_by_register(
        self,
        add_level_name_mock,
    ) -> None:
        """Verifies that retrieving a newly registered custom level returns the same immutable LogLevel instance."""
        registered_log_level = self.log_level_registry.register(
            name="SUCCESS",
            color="green",
            severity=25,
        )

        resolved_log_level = self.log_level_registry.get(
            "SUCCESS",
        )

        self.assertIs(
            resolved_log_level,
            registered_log_level,
            ("Expected get() to return the same LogLevel instance that was " "stored during registration."),
        )

        add_level_name_mock.assert_called_once()

    @patch("src.spectralog.levels.log_level_registry.logging.addLevelName")
    def test_contains_returns_true_after_custom_log_level_registration(
        self,
        add_level_name_mock,
    ) -> None:
        """Verifies that contains recognizes a custom log level immediately after successful registration."""
        self.log_level_registry.register(
            name="SUCCESS",
            color="green",
            severity=25,
        )

        contains_custom_log_level = self.log_level_registry.contains(
            " success ",
        )

        self.assertTrue(
            contains_custom_log_level,
            ("Expected contains(' success ') to return True after SUCCESS " "was successfully registered."),
        )

        add_level_name_mock.assert_called_once()

    def test_default_log_level_models_are_frozen(self) -> None:
        """Verifies that returned LogLevel models cannot be mutated after registration."""
        default_log_level = self.log_level_registry.get(
            "INFO",
        )

        with self.assertRaises(
            AttributeError,
            msg=("Expected LogLevel to reject mutation because it is defined " "as a frozen dataclass."),
        ):
            setattr(default_log_level, "color", "blue")
