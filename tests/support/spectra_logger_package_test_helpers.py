from __future__ import annotations

import os
import subprocess
import sys
import unittest
from pathlib import Path


def run_consumer_script(
    script: str,
    timeout_seconds: int = 15,
) -> subprocess.CompletedProcess[str]:
    """Execute a Python consumer script against the local SpectraLog source tree.

    The supplied script is executed in a separate Python process using the
    currently running Python interpreter.

    The project's ``src`` directory is prepended to ``PYTHONPATH`` so that the
    consumer process imports the local SpectraLog implementation instead of an
    installed package version.

    Existing ``PYTHONPATH`` entries are preserved.

    Args:
        script:
            Python source code to execute using ``python -c``.

        timeout_seconds:
            Maximum number of seconds to allow the consumer process to run
            before :func:`subprocess.run` raises
            :class:`subprocess.TimeoutExpired`.

    Returns:
        subprocess.CompletedProcess[str]:
            The completed consumer process containing its return code,
            standard output, and standard error.
    """
    project_root = (
        Path(
            __file__,
        )
        .resolve()
        .parents[2]
    )

    source_directory = project_root / "src"

    environment = os.environ.copy()

    existing_python_path = environment.get(
        "PYTHONPATH",
    )

    if existing_python_path:
        environment["PYTHONPATH"] = (
            f"{source_directory}"
            f"{os.pathsep}"
            f"{existing_python_path}"
        )
    else:
        environment["PYTHONPATH"] = str(
            source_directory,
        )

    completed_process = subprocess.run(
        [
            sys.executable,
            "-c",
            script,
        ],
        capture_output=True,
        text=True,
        timeout=timeout_seconds,
        check=False,
        env=environment,
    )

    return completed_process


def assert_consumer_succeeded(
    test_case: unittest.TestCase,
    completed_process: subprocess.CompletedProcess[str],
) -> None:
    """Assert that a consumer subprocess completed successfully.

    Args:
        test_case:
            Active :class:`unittest.TestCase` instance used to perform the
            assertion.

        completed_process:
            Result returned by :func:`run_consumer_script`.

    Raises:
        AssertionError:
            If the consumer process returned a non-zero exit status.
    """
    test_case.assertEqual(
        completed_process.returncode,
        0,
        (
            "Expected consumer process to exit successfully.\n"
            f"stdout:\n{completed_process.stdout}\n"
            f"stderr:\n{completed_process.stderr}"
        ),
    )