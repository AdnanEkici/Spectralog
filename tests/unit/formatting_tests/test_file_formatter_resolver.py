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
from spectralog.core.protocols import FileFormatterStrategyProtocol  # noqa: E402
from spectralog.formatting.file_formatter_resolver import FileFormatterResolver  # noqa: E402


class UnitTestFileFormatterResolver(unittest.TestCase):
    def test_constructor_preserves_formatter_strategy_order(
        self,
    ) -> None:
        """Verifies that the resolver evaluates formatter strategies in the same order they were supplied."""
        first_formatter_strategy = MagicMock(
            spec=FileFormatterStrategyProtocol,
        )

        second_formatter_strategy = MagicMock(
            spec=FileFormatterStrategyProtocol,
        )

        file_formatter_resolver = FileFormatterResolver(
            formatter_strategies=[
                first_formatter_strategy,
                second_formatter_strategy,
            ],
        )

        self.assertEqual(
            file_formatter_resolver._formatter_strategies,
            (
                first_formatter_strategy,
                second_formatter_strategy,
            ),
            ("Expected formatter strategies to be stored in the same " "order they were supplied."),
        )

    def test_constructor_converts_strategy_sequence_to_tuple(
        self,
    ) -> None:
        """Verifies that the resolver stores the supplied formatter strategies as an immutable tuple."""
        formatter_strategy = MagicMock(
            spec=FileFormatterStrategyProtocol,
        )

        file_formatter_resolver = FileFormatterResolver(
            formatter_strategies=[
                formatter_strategy,
            ],
        )

        self.assertIsInstance(
            file_formatter_resolver._formatter_strategies,
            tuple,
            ("Expected formatter strategies to be stored as a tuple " "inside the resolver."),
        )

    def test_constructor_copies_supplied_sequence(
        self,
    ) -> None:
        """Verifies that mutating the original strategy sequence does not change the resolver's stored strategies."""
        first_formatter_strategy = MagicMock(
            spec=FileFormatterStrategyProtocol,
        )

        second_formatter_strategy = MagicMock(
            spec=FileFormatterStrategyProtocol,
        )

        formatter_strategies = [
            first_formatter_strategy,
        ]

        file_formatter_resolver = FileFormatterResolver(
            formatter_strategies=formatter_strategies,
        )

        formatter_strategies.append(
            second_formatter_strategy,
        )

        self.assertEqual(
            file_formatter_resolver._formatter_strategies,
            (first_formatter_strategy,),
            ("Expected the resolver to retain an independent tuple copy " "of the strategies supplied during construction."),
        )

    def test_resolve_returns_formatter_from_first_supported_strategy(
        self,
    ) -> None:
        """Verifies that resolve returns the formatter created by the first strategy that supports the configuration."""
        configuration = LoggerConfiguration()

        first_formatter_strategy = MagicMock(
            spec=FileFormatterStrategyProtocol,
        )

        second_formatter_strategy = MagicMock(
            spec=FileFormatterStrategyProtocol,
        )

        first_formatter = MagicMock(
            spec=logging.Formatter,
        )

        second_formatter = MagicMock(
            spec=logging.Formatter,
        )

        first_formatter_strategy.supports.return_value = True
        first_formatter_strategy.create.return_value = first_formatter

        second_formatter_strategy.supports.return_value = True
        second_formatter_strategy.create.return_value = second_formatter

        file_formatter_resolver = FileFormatterResolver(
            formatter_strategies=[
                first_formatter_strategy,
                second_formatter_strategy,
            ],
        )

        resolved_formatter = file_formatter_resolver.resolve(
            configuration=configuration,
        )

        self.assertIs(
            resolved_formatter,
            first_formatter,
            ("Expected resolve() to return the formatter created by the " "first strategy that supports the configuration."),
        )

    def test_resolve_checks_first_strategy_support(
        self,
    ) -> None:
        """Verifies that resolve asks the first strategy whether it supports the supplied configuration."""
        configuration = LoggerConfiguration()

        formatter_strategy = MagicMock(
            spec=FileFormatterStrategyProtocol,
        )

        formatter_strategy.supports.return_value = True
        formatter_strategy.create.return_value = MagicMock(
            spec=logging.Formatter,
        )

        file_formatter_resolver = FileFormatterResolver(
            formatter_strategies=[
                formatter_strategy,
            ],
        )

        file_formatter_resolver.resolve(
            configuration=configuration,
        )

        formatter_strategy.supports.assert_called_once_with(
            configuration,
        )

    def test_resolve_creates_formatter_using_supported_strategy(
        self,
    ) -> None:
        """Verifies that resolve passes the supplied configuration to the supported strategy's create method."""
        configuration = LoggerConfiguration(
            debug_mode=True,
        )

        formatter_strategy = MagicMock(
            spec=FileFormatterStrategyProtocol,
        )

        formatter_strategy.supports.return_value = True
        formatter_strategy.create.return_value = MagicMock(
            spec=logging.Formatter,
        )

        file_formatter_resolver = FileFormatterResolver(
            formatter_strategies=[
                formatter_strategy,
            ],
        )

        file_formatter_resolver.resolve(
            configuration=configuration,
        )

        formatter_strategy.create.assert_called_once_with(
            configuration,
        )

    def test_resolve_skips_unsupported_strategy(
        self,
    ) -> None:
        """Verifies that resolve skips a strategy that does not support the supplied configuration."""
        configuration = LoggerConfiguration()

        unsupported_formatter_strategy = MagicMock(
            spec=FileFormatterStrategyProtocol,
        )

        supported_formatter_strategy = MagicMock(
            spec=FileFormatterStrategyProtocol,
        )

        formatter = MagicMock(
            spec=logging.Formatter,
        )

        unsupported_formatter_strategy.supports.return_value = False
        supported_formatter_strategy.supports.return_value = True
        supported_formatter_strategy.create.return_value = formatter

        file_formatter_resolver = FileFormatterResolver(
            formatter_strategies=[
                unsupported_formatter_strategy,
                supported_formatter_strategy,
            ],
        )

        resolved_formatter = file_formatter_resolver.resolve(
            configuration=configuration,
        )

        self.assertIs(
            resolved_formatter,
            formatter,
            ("Expected resolve() to return the formatter created by the " "first supported strategy after skipping unsupported ones."),
        )

        unsupported_formatter_strategy.create.assert_not_called()

    def test_resolve_evaluates_strategies_in_supplied_order(
        self,
    ) -> None:
        """Verifies that resolve evaluates formatter strategy support in the order the strategies were supplied."""
        configuration = LoggerConfiguration()

        first_formatter_strategy = MagicMock(
            spec=FileFormatterStrategyProtocol,
        )

        second_formatter_strategy = MagicMock(
            spec=FileFormatterStrategyProtocol,
        )

        third_formatter_strategy = MagicMock(
            spec=FileFormatterStrategyProtocol,
        )

        third_formatter_strategy.create.return_value = MagicMock(
            spec=logging.Formatter,
        )

        evaluation_order: list[str] = []

        def first_supports(
            supplied_configuration: LoggerConfiguration,
        ) -> bool:
            evaluation_order.append(
                "first",
            )

            is_supported = False

            return is_supported

        def second_supports(
            supplied_configuration: LoggerConfiguration,
        ) -> bool:
            evaluation_order.append(
                "second",
            )

            is_supported = False

            return is_supported

        def third_supports(
            supplied_configuration: LoggerConfiguration,
        ) -> bool:
            evaluation_order.append(
                "third",
            )

            is_supported = True

            return is_supported

        first_formatter_strategy.supports.side_effect = first_supports
        second_formatter_strategy.supports.side_effect = second_supports
        third_formatter_strategy.supports.side_effect = third_supports

        file_formatter_resolver = FileFormatterResolver(
            formatter_strategies=[
                first_formatter_strategy,
                second_formatter_strategy,
                third_formatter_strategy,
            ],
        )

        file_formatter_resolver.resolve(
            configuration=configuration,
        )

        self.assertEqual(
            evaluation_order,
            [
                "first",
                "second",
                "third",
            ],
            ("Expected formatter strategies to be evaluated in the exact " "order they were supplied."),
        )

    def test_resolve_stops_evaluating_after_first_supported_strategy(
        self,
    ) -> None:
        """Verifies that resolve stops evaluating additional strategies after finding the first supported strategy."""
        configuration = LoggerConfiguration()

        first_formatter_strategy = MagicMock(
            spec=FileFormatterStrategyProtocol,
        )

        second_formatter_strategy = MagicMock(
            spec=FileFormatterStrategyProtocol,
        )

        third_formatter_strategy = MagicMock(
            spec=FileFormatterStrategyProtocol,
        )

        first_formatter_strategy.supports.return_value = False
        second_formatter_strategy.supports.return_value = True
        third_formatter_strategy.supports.return_value = True

        second_formatter_strategy.create.return_value = MagicMock(
            spec=logging.Formatter,
        )

        file_formatter_resolver = FileFormatterResolver(
            formatter_strategies=[
                first_formatter_strategy,
                second_formatter_strategy,
                third_formatter_strategy,
            ],
        )

        file_formatter_resolver.resolve(
            configuration=configuration,
        )

        first_formatter_strategy.supports.assert_called_once_with(
            configuration,
        )

        second_formatter_strategy.supports.assert_called_once_with(
            configuration,
        )

        third_formatter_strategy.supports.assert_not_called()
        third_formatter_strategy.create.assert_not_called()

    def test_resolve_calls_create_only_on_selected_strategy(
        self,
    ) -> None:
        """Verifies that resolve calls create only on the strategy selected as the first supported strategy."""
        configuration = LoggerConfiguration()

        first_formatter_strategy = MagicMock(
            spec=FileFormatterStrategyProtocol,
        )

        second_formatter_strategy = MagicMock(
            spec=FileFormatterStrategyProtocol,
        )

        third_formatter_strategy = MagicMock(
            spec=FileFormatterStrategyProtocol,
        )

        first_formatter_strategy.supports.return_value = False
        second_formatter_strategy.supports.return_value = True
        third_formatter_strategy.supports.return_value = True

        second_formatter_strategy.create.return_value = MagicMock(
            spec=logging.Formatter,
        )

        file_formatter_resolver = FileFormatterResolver(
            formatter_strategies=[
                first_formatter_strategy,
                second_formatter_strategy,
                third_formatter_strategy,
            ],
        )

        file_formatter_resolver.resolve(
            configuration=configuration,
        )

        first_formatter_strategy.create.assert_not_called()

        second_formatter_strategy.create.assert_called_once_with(
            configuration,
        )

        third_formatter_strategy.create.assert_not_called()

    def test_resolve_raises_runtime_error_when_no_strategy_supports_configuration(
        self,
    ) -> None:
        """Verifies that resolve raises RuntimeError when no formatter strategy supports the supplied configuration."""
        configuration = LoggerConfiguration()

        first_formatter_strategy = MagicMock(
            spec=FileFormatterStrategyProtocol,
        )

        second_formatter_strategy = MagicMock(
            spec=FileFormatterStrategyProtocol,
        )

        first_formatter_strategy.supports.return_value = False
        second_formatter_strategy.supports.return_value = False

        file_formatter_resolver = FileFormatterResolver(
            formatter_strategies=[
                first_formatter_strategy,
                second_formatter_strategy,
            ],
        )

        with self.assertRaisesRegex(
            RuntimeError,
            ("No file formatter strategy supports " "the supplied logger configuration."),
            msg=("Expected resolve() to raise RuntimeError when no formatter " "strategy supports the supplied configuration."),
        ):
            file_formatter_resolver.resolve(
                configuration=configuration,
            )

    def test_resolve_raises_runtime_error_when_strategy_collection_is_empty(
        self,
    ) -> None:
        """Verifies that resolve raises RuntimeError when the resolver contains no formatter strategies."""
        configuration = LoggerConfiguration()

        file_formatter_resolver = FileFormatterResolver(
            formatter_strategies=[],
        )

        with self.assertRaisesRegex(
            RuntimeError,
            ("No file formatter strategy supports " "the supplied logger configuration."),
            msg=("Expected resolve() to raise RuntimeError when no formatter " "strategies are configured."),
        ):
            file_formatter_resolver.resolve(
                configuration=configuration,
            )

    def test_resolve_checks_every_strategy_when_none_support_configuration(
        self,
    ) -> None:
        """Verifies that resolve evaluates every configured strategy before raising when none support the configuration."""
        configuration = LoggerConfiguration()

        first_formatter_strategy = MagicMock(
            spec=FileFormatterStrategyProtocol,
        )

        second_formatter_strategy = MagicMock(
            spec=FileFormatterStrategyProtocol,
        )

        third_formatter_strategy = MagicMock(
            spec=FileFormatterStrategyProtocol,
        )

        first_formatter_strategy.supports.return_value = False
        second_formatter_strategy.supports.return_value = False
        third_formatter_strategy.supports.return_value = False

        file_formatter_resolver = FileFormatterResolver(
            formatter_strategies=[
                first_formatter_strategy,
                second_formatter_strategy,
                third_formatter_strategy,
            ],
        )

        with self.assertRaises(
            RuntimeError,
            msg=("Expected resolve() to raise RuntimeError after all " "formatter strategies reject the configuration."),
        ):
            file_formatter_resolver.resolve(
                configuration=configuration,
            )

        first_formatter_strategy.supports.assert_called_once_with(
            configuration,
        )

        second_formatter_strategy.supports.assert_called_once_with(
            configuration,
        )

        third_formatter_strategy.supports.assert_called_once_with(
            configuration,
        )

    def test_resolve_does_not_create_formatter_when_no_strategy_supports_configuration(
        self,
    ) -> None:
        """Verifies that resolve never calls create when every formatter strategy rejects the supplied configuration."""
        configuration = LoggerConfiguration()

        first_formatter_strategy = MagicMock(
            spec=FileFormatterStrategyProtocol,
        )

        second_formatter_strategy = MagicMock(
            spec=FileFormatterStrategyProtocol,
        )

        first_formatter_strategy.supports.return_value = False
        second_formatter_strategy.supports.return_value = False

        file_formatter_resolver = FileFormatterResolver(
            formatter_strategies=[
                first_formatter_strategy,
                second_formatter_strategy,
            ],
        )

        with self.assertRaises(
            RuntimeError,
            msg=("Expected resolve() to raise RuntimeError when every " "formatter strategy rejects the configuration."),
        ):
            file_formatter_resolver.resolve(
                configuration=configuration,
            )

        first_formatter_strategy.create.assert_not_called()
        second_formatter_strategy.create.assert_not_called()

    def test_resolve_passes_same_configuration_instance_to_supports_and_create(
        self,
    ) -> None:
        """Verifies that resolve passes the exact same configuration instance to both supports and create."""
        configuration = LoggerConfiguration(
            debug_mode=True,
            show_datetime=False,
            show_line=True,
        )

        formatter_strategy = MagicMock(
            spec=FileFormatterStrategyProtocol,
        )

        formatter = MagicMock(
            spec=logging.Formatter,
        )

        formatter_strategy.supports.return_value = True
        formatter_strategy.create.return_value = formatter

        file_formatter_resolver = FileFormatterResolver(
            formatter_strategies=[
                formatter_strategy,
            ],
        )

        resolved_formatter = file_formatter_resolver.resolve(
            configuration=configuration,
        )

        supports_configuration = formatter_strategy.supports.call_args.args[0]
        create_configuration = formatter_strategy.create.call_args.args[0]

        self.assertIs(
            supports_configuration,
            configuration,
            ("Expected supports() to receive the exact logger " "configuration instance supplied to resolve()."),
        )

        self.assertIs(
            create_configuration,
            configuration,
            ("Expected create() to receive the exact logger configuration " "instance supplied to resolve()."),
        )

        self.assertIs(
            resolved_formatter,
            formatter,
            ("Expected resolve() to return the formatter produced by the " "selected strategy."),
        )
