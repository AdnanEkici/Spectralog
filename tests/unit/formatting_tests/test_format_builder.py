from __future__ import annotations

import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]  # noqa
SRC_DIR = PROJECT_ROOT / "src"  # noqa
sys.path.insert(0, str(SRC_DIR))  # noqa

from spectralog.configuration.configuration import LoggerConfiguration  # noqa: E402
from spectralog.formatting.format_builder import LogFormatBuilder  # noqa: E402


class UnitTestLogFormatBuilder(unittest.TestCase):
    def setUp(self) -> None:
        self.log_format_builder = LogFormatBuilder()

    def test_build_console_format_returns_custom_console_format(
        self,
    ) -> None:
        """Verifies that build_console_format returns the configured custom console format unchanged."""
        custom_console_format = "%(levelname)s :: %(message)s"

        configuration = LoggerConfiguration(
            console_format=custom_console_format,
        )

        built_console_format = self.log_format_builder.build_console_format(
            configuration=configuration,
        )

        self.assertEqual(
            built_console_format,
            custom_console_format,
            ("Expected build_console_format() to return the custom " "console format unchanged."),
        )

    def test_build_console_format_adds_color_prefix_and_reset_suffix(
        self,
    ) -> None:
        """Verifies that build_console_format wraps the plain format with log color and reset placeholders."""
        configuration = LoggerConfiguration(
            show_datetime=False,
            show_folder_name=False,
            show_line=False,
        )

        built_console_format = self.log_format_builder.build_console_format(
            configuration=configuration,
        )

        expected_console_format = "%(log_color)s" "%(levelname)s | %(message)s" "%(reset)s"

        self.assertEqual(
            built_console_format,
            expected_console_format,
            ("Expected the default console format to wrap the plain " "format with log_color and reset placeholders."),
        )

    def test_build_console_format_ignores_default_builder_when_custom_format_is_supplied(
        self,
    ) -> None:
        """Verifies that a custom console format takes precedence over generated formatting options."""
        custom_console_format = "%(message)s"

        configuration = LoggerConfiguration(
            console_format=custom_console_format,
            show_datetime=True,
            show_folder_name=True,
            show_line=True,
        )

        built_console_format = self.log_format_builder.build_console_format(
            configuration=configuration,
        )

        self.assertEqual(
            built_console_format,
            custom_console_format,
            ("Expected a custom console format to take precedence over " "all generated formatting options."),
        )

    def test_build_file_format_returns_custom_file_format(
        self,
    ) -> None:
        """Verifies that build_file_format returns the configured custom file format unchanged."""
        custom_file_format = "%(asctime)s :: %(message)s"

        configuration = LoggerConfiguration(
            file_format=custom_file_format,
        )

        built_file_format = self.log_format_builder.build_file_format(
            configuration=configuration,
        )

        self.assertEqual(
            built_file_format,
            custom_file_format,
            ("Expected build_file_format() to return the custom file " "format unchanged."),
        )

    def test_build_file_format_does_not_add_color_placeholders(
        self,
    ) -> None:
        """Verifies that the generated file format does not contain console color placeholders."""
        configuration = LoggerConfiguration(
            show_datetime=False,
            show_folder_name=False,
            show_line=False,
        )

        built_file_format = self.log_format_builder.build_file_format(
            configuration=configuration,
        )

        self.assertEqual(
            built_file_format,
            "%(levelname)s | %(message)s",
            ("Expected the generated file format to contain only the " "plain logging fields."),
        )

        self.assertNotIn(
            "%(log_color)s",
            built_file_format,
            ("Expected the generated file format not to contain the " "log_color placeholder."),
        )

        self.assertNotIn(
            "%(reset)s",
            built_file_format,
            ("Expected the generated file format not to contain the " "reset placeholder."),
        )

    def test_build_file_format_ignores_default_builder_when_custom_format_is_supplied(
        self,
    ) -> None:
        """Verifies that a custom file format takes precedence over generated formatting options."""
        custom_file_format = "%(message)s"

        configuration = LoggerConfiguration(
            file_format=custom_file_format,
            show_datetime=True,
            show_folder_name=True,
            show_line=True,
        )

        built_file_format = self.log_format_builder.build_file_format(
            configuration=configuration,
        )

        self.assertEqual(
            built_file_format,
            custom_file_format,
            ("Expected a custom file format to take precedence over all " "generated formatting options."),
        )

    def test_plain_format_contains_datetime_when_enabled(
        self,
    ) -> None:
        """Verifies that the generated plain format includes the asctime placeholder when datetime output is enabled."""
        configuration = LoggerConfiguration(
            show_datetime=True,
            show_folder_name=False,
            show_line=False,
        )

        built_file_format = self.log_format_builder.build_file_format(
            configuration=configuration,
        )

        self.assertEqual(
            built_file_format,
            "%(asctime)s | %(levelname)s | %(message)s",
            ("Expected the generated format to include asctime when " "show_datetime is enabled."),
        )

    def test_plain_format_excludes_datetime_when_disabled(
        self,
    ) -> None:
        """Verifies that the generated plain format excludes the asctime placeholder when datetime output is disabled."""
        configuration = LoggerConfiguration(
            show_datetime=False,
            show_folder_name=False,
            show_line=False,
        )

        built_file_format = self.log_format_builder.build_file_format(
            configuration=configuration,
        )

        self.assertEqual(
            built_file_format,
            "%(levelname)s | %(message)s",
            ("Expected the generated format to exclude asctime when " "show_datetime is disabled."),
        )

    def test_plain_format_always_contains_log_level(
        self,
    ) -> None:
        """Verifies that the generated plain format always contains the logging level placeholder."""
        configuration = LoggerConfiguration(
            show_datetime=False,
            show_folder_name=False,
            show_line=False,
        )

        built_file_format = self.log_format_builder.build_file_format(
            configuration=configuration,
        )

        self.assertIn(
            "%(levelname)s",
            built_file_format,
            ("Expected the generated plain format to always contain the " "logging level placeholder."),
        )

    def test_plain_format_always_contains_message(
        self,
    ) -> None:
        """Verifies that the generated plain format always contains the log message placeholder."""
        configuration = LoggerConfiguration(
            show_datetime=False,
            show_folder_name=False,
            show_line=False,
        )

        built_file_format = self.log_format_builder.build_file_format(
            configuration=configuration,
        )

        self.assertIn(
            "%(message)s",
            built_file_format,
            ("Expected the generated plain format to always contain the " "message placeholder."),
        )

    def test_plain_format_contains_relative_path_when_folder_name_is_enabled(
        self,
    ) -> None:
        """Verifies that the generated plain format contains relative_path when folder name output is enabled."""
        configuration = LoggerConfiguration(
            show_datetime=False,
            show_folder_name=True,
            show_line=False,
        )

        built_file_format = self.log_format_builder.build_file_format(
            configuration=configuration,
        )

        self.assertEqual(
            built_file_format,
            "%(levelname)s | %(relative_path)s | %(message)s",
            ("Expected the generated format to contain relative_path " "when show_folder_name is enabled."),
        )

    def test_plain_format_contains_relative_path_and_line_when_both_are_enabled(
        self,
    ) -> None:
        """Verifies that the generated plain format appends the line number directly to relative_path when both location options are enabled."""
        configuration = LoggerConfiguration(
            show_datetime=False,
            show_folder_name=True,
            show_line=True,
        )

        built_file_format = self.log_format_builder.build_file_format(
            configuration=configuration,
        )

        self.assertEqual(
            built_file_format,
            "%(levelname)s | %(relative_path)s:%(lineno)d | %(message)s",
            ("Expected the generated format to combine relative_path and " "lineno when folder and line output are enabled."),
        )

    def test_plain_format_contains_line_label_when_only_line_is_enabled(
        self,
    ) -> None:
        """Verifies that the generated plain format contains the line label when line output is enabled without folder output."""
        configuration = LoggerConfiguration(
            show_datetime=False,
            show_folder_name=False,
            show_line=True,
        )

        built_file_format = self.log_format_builder.build_file_format(
            configuration=configuration,
        )

        self.assertEqual(
            built_file_format,
            "%(levelname)s | line %(lineno)d | %(message)s",
            ("Expected the generated format to contain 'line %(lineno)d' " "when show_line is enabled without show_folder_name."),
        )

    def test_plain_format_does_not_include_location_when_both_location_options_are_disabled(
        self,
    ) -> None:
        """Verifies that the generated plain format excludes path and line fields when both location options are disabled."""
        configuration = LoggerConfiguration(
            show_datetime=False,
            show_folder_name=False,
            show_line=False,
        )

        built_file_format = self.log_format_builder.build_file_format(
            configuration=configuration,
        )

        self.assertEqual(
            built_file_format,
            "%(levelname)s | %(message)s",
            ("Expected the generated format to exclude all location " "information when both location options are disabled."),
        )

    def test_plain_format_contains_all_default_fields(
        self,
    ) -> None:
        """Verifies that the generated format contains all fields enabled by the default logger configuration."""
        configuration = LoggerConfiguration()

        built_file_format = self.log_format_builder.build_file_format(
            configuration=configuration,
        )

        self.assertEqual(
            built_file_format,
            "%(asctime)s | %(levelname)s | %(message)s",
            ("Expected the default logger configuration to generate " "datetime, log level, and message fields."),
        )

    def test_plain_format_contains_all_optional_fields_when_enabled(
        self,
    ) -> None:
        """Verifies that the generated plain format contains datetime, level, relative path, line number, and message when all options are enabled."""
        configuration = LoggerConfiguration(
            show_datetime=True,
            show_folder_name=True,
            show_line=True,
        )

        built_file_format = self.log_format_builder.build_file_format(
            configuration=configuration,
        )

        self.assertEqual(
            built_file_format,
            ("%(asctime)s | %(levelname)s | " "%(relative_path)s:%(lineno)d | %(message)s"),
            ("Expected the generated format to contain every optional " "field when all formatting options are enabled."),
        )

    def test_console_and_file_formats_share_same_plain_structure(
        self,
    ) -> None:
        """Verifies that generated console and file formats use the same plain field structure apart from console color wrappers."""
        configuration = LoggerConfiguration(
            show_datetime=True,
            show_folder_name=True,
            show_line=True,
        )

        built_console_format = self.log_format_builder.build_console_format(
            configuration=configuration,
        )

        built_file_format = self.log_format_builder.build_file_format(
            configuration=configuration,
        )

        expected_console_format = "%(log_color)s" f"{built_file_format}" "%(reset)s"

        self.assertEqual(
            built_console_format,
            expected_console_format,
            ("Expected the generated console format to wrap the same " "plain structure used by the generated file format."),
        )

    def test_custom_console_format_does_not_receive_color_wrappers(
        self,
    ) -> None:
        """Verifies that a custom console format is returned exactly as supplied without automatic color placeholders."""
        custom_console_format = "%(levelname)s %(message)s"

        configuration = LoggerConfiguration(
            console_format=custom_console_format,
        )

        built_console_format = self.log_format_builder.build_console_format(
            configuration=configuration,
        )

        self.assertEqual(
            built_console_format,
            custom_console_format,
            ("Expected the custom console format to remain unchanged " "without automatic color wrappers."),
        )

        self.assertNotIn(
            "%(log_color)s",
            built_console_format,
            ("Expected the custom console format not to receive an " "automatic log_color placeholder."),
        )

        self.assertNotIn(
            "%(reset)s",
            built_console_format,
            ("Expected the custom console format not to receive an " "automatic reset placeholder."),
        )

    def test_custom_file_format_is_not_modified(
        self,
    ) -> None:
        """Verifies that a custom file format is returned byte-for-byte unchanged by the builder."""
        custom_file_format = "%(name)s::%(levelname)s::%(message)s"

        configuration = LoggerConfiguration(
            file_format=custom_file_format,
        )

        built_file_format = self.log_format_builder.build_file_format(
            configuration=configuration,
        )

        self.assertEqual(
            built_file_format,
            custom_file_format,
            ("Expected the custom file format to be returned exactly as " "supplied."),
        )

    def test_empty_custom_console_format_is_respected(
        self,
    ) -> None:
        """Verifies that an explicitly configured empty console format is treated as a valid custom format."""
        configuration = LoggerConfiguration(
            console_format="",
        )

        built_console_format = self.log_format_builder.build_console_format(
            configuration=configuration,
        )

        self.assertEqual(
            built_console_format,
            "",
            ("Expected an explicitly configured empty console format to " "be returned unchanged."),
        )

    def test_empty_custom_file_format_is_respected(
        self,
    ) -> None:
        """Verifies that an explicitly configured empty file format is treated as a valid custom format."""
        configuration = LoggerConfiguration(
            file_format="",
        )

        built_file_format = self.log_format_builder.build_file_format(
            configuration=configuration,
        )

        self.assertEqual(
            built_file_format,
            "",
            ("Expected an explicitly configured empty file format to be " "returned unchanged."),
        )
