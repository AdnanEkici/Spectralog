from __future__ import annotations

import logging
from collections.abc import Sequence

from spectralog.configuration.configuration import LoggerConfiguration
from spectralog.core.protocols import FileFormatterStrategyProtocol


class FileFormatterResolver:
    """Resolve the appropriate file formatter for a logger configuration.

    ``FileFormatterResolver`` selects a file formatter through an ordered sequence
    of formatter strategies implementing :class:`FileFormatterStrategyProtocol`.

    Strategies are evaluated in the order supplied to the resolver. The first
    strategy whose :meth:`FileFormatterStrategyProtocol.supports` method returns
    ``True`` is selected, and that strategy is then used to create the
    :class:`logging.Formatter`.

    The strategy sequence is copied to an immutable tuple during initialization so
    that later changes to the original collection do not affect formatter
    resolution behavior.

    This design allows SpectraLog to support multiple file output formats, such as
    JSON and plain text, without coupling the file handler directly to concrete
    formatter implementations."""

    def __init__(
        self,
        formatter_strategies: Sequence[FileFormatterStrategyProtocol],
    ) -> None:
        """Initialize the resolver with an ordered collection of formatter strategies.

        The supplied strategy sequence is copied into a tuple and preserved in the
        same order. Resolution order is significant because the first strategy that
        reports support for a configuration is selected.

        Args:
            formatter_strategies:
                Ordered collection of file formatter strategies. Each strategy is
                queried through ``supports`` and may create the formatter when it is
                the first strategy compatible with the supplied logger configuration."""
        self._formatter_strategies = tuple(
            formatter_strategies,
        )

    def resolve(
        self,
        configuration: LoggerConfiguration,
    ) -> logging.Formatter:
        """Resolve and create the file formatter for a logger configuration.

        Each configured formatter strategy is evaluated in order. When a strategy
        reports that it supports the supplied :class:`LoggerConfiguration`, its
        ``create`` method is called and the resulting formatter is returned
        immediately.

        No later strategies are evaluated after a compatible strategy has been
        selected.

        Args:
            configuration:
                Logger configuration used by each strategy to determine whether it
                supports the requested file logging mode.

        Raises:
            RuntimeError:
                If none of the configured formatter strategies supports the supplied
                logger configuration.

        Returns:
            logging.Formatter:
                The formatter created by the first compatible file formatter strategy."""
        for formatter_strategy in self._formatter_strategies:
            if formatter_strategy.supports(
                configuration,
            ):
                formatter = formatter_strategy.create(
                    configuration,
                )

                resolved_formatter = formatter

                return resolved_formatter

        raise RuntimeError(
            "No file formatter strategy supports " "the supplied logger configuration.",
        )
