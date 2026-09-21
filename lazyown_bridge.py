#!/usr/bin/env python3
"""LazyOwn Bridge — SOLID subprocess integration for TopoSwarm.

Architecture
------------
LazyOwnPathResolver      discovers the LazyOwn directory.
LazyOwnPayloadManager    reads/writes payload.json (state persistence).
LazyOwnCommandBuilder    constructs safe invocations.
LazyOwnProcessExecutor   runs commands, handles timeouts, kills, cleanup.
LazyOwnOutputSanitizer   strips ANSI codes and framework noise.
LazyOwnBridge            orchestrates the above into a single public API.

Design constraints
------------------
- Zero absolute paths; discovery is relative or environment-driven.
- No magic numbers; all thresholds and patterns are named constants.
- No placeholders; every code path is implemented.
- Stateless LazyOwn process per command; state is injected/extracted via
  payload.json before/after each invocation.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import time
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------


class _EnvKey(str, Enum):
    """Environment variable names used for configuration."""

    LAZYOWN_DIR = "LAZYOWN_DIR"


class _FileName(str, Enum):
    """File names expected inside the LazyOwn directory."""

    PAYLOAD = "payload.json"
    RUN_SCRIPT = "run"
    PYTHON_SCRIPT = "lazyown.py"
    VENV = "env"


class _Defaults:
    """Default operational parameters."""

    TIMEOUT_SECONDS: int = 30
    FAST_TIMEOUT_SECONDS: int = 5
    MAX_OUTPUT_BYTES: int = 1_048_576
    READ_CHUNK_BYTES: int = 4096
    POLL_INTERVAL_SECONDS: float = 0.05
    EXIT_COMMAND: str = "exit"
    CMD2_COMMAND_FLAG: str = "-c"


# ---------------------------------------------------------------------------
# Data transfer object
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ExecutionResult:
    """Immutable result of a LazyOwn command execution."""

    command: str
    raw_output: str
    cleaned_output: str
    returncode: int
    latency_ms: float
    ok: bool


# ---------------------------------------------------------------------------
# LazyOwnPathResolver
# ---------------------------------------------------------------------------


class LazyOwnPathResolver:
    """Discovers the LazyOwn installation directory without hard-coded paths.

    Resolution priority:
      1. LAZYOWN_DIR environment variable.
      2. Parent directory of the current working directory (repo sibling).
      3. User home directory ~/LazyOwn.
      4. Current working directory ./LazyOwn.
    """

    _REPO_SIBLING_DEPTH: int = 2
    _HOME_SUBDIR: str = "LazyOwn"
    _CWD_SUBDIR: str = "LazyOwn"

    def __init__(self) -> None:
        self._resolved: Optional[Path] = None

    def resolve(self) -> Path:
        """Return the discovered LazyOwn directory.

        Raises:
            FileNotFoundError: if no candidate directory exists.
        """
        if self._resolved is not None:
            return self._resolved

        candidate = self._from_env()
        if candidate is None:
            candidate = self._from_repo_sibling()
        if candidate is None:
            candidate = self._from_home()
        if candidate is None:
            candidate = self._from_cwd()

        if candidate is None or not candidate.exists():
            raise FileNotFoundError(
                "LazyOwn directory not found. "
                f"Set {_EnvKey.LAZYOWN_DIR} or ensure LazyOwn is a sibling of the repo."
            )

        self._resolved = candidate
        return candidate

    def _from_env(self) -> Optional[Path]:
        raw = os.environ.get(_EnvKey.LAZYOWN_DIR.value, "").strip()
        if not raw:
            return None
        path = Path(raw).expanduser().resolve()
        return path if path.exists() else None

    def _from_repo_sibling(self) -> Optional[Path]:
        cwd = Path.cwd().resolve()
        candidate = cwd
        for _ in range(self._REPO_SIBLING_DEPTH):
            candidate = candidate.parent
        candidate = candidate / self._HOME_SUBDIR
        return candidate if candidate.exists() else None

    def _from_home(self) -> Optional[Path]:
        candidate = Path.home() / self._HOME_SUBDIR
        return candidate if candidate.exists() else None

    def _from_cwd(self) -> Optional[Path]:
        candidate = Path.cwd() / self._CWD_SUBDIR
        return candidate if candidate.exists() else None


# ---------------------------------------------------------------------------
# LazyOwnPayloadManager
# ---------------------------------------------------------------------------


class LazyOwnPayloadManager:
    """Reads and writes LazyOwn configuration via payload.json.

    This is the only state channel between TopoSwarm and LazyOwn when using
    one-shot subprocess execution.  All mutable parameters (rhost, lhost,
    domain, etc.) are persisted in payload.json so the next LazyOwn process
    sees the same state.
    """

    def __init__(self, lazyown_dir: Path) -> None:
        self._lazyown_dir = lazyown_dir
        self._payload_path = lazyown_dir / _FileName.PAYLOAD.value

    @property
    def payload_path(self) -> Path:
        return self._payload_path

    def read(self) -> Dict[str, Any]:
        """Return the current payload.json as a dictionary."""
        if not self._payload_path.exists():
            return {}
        try:
            with self._payload_path.open("r", encoding="utf-8") as handle:
                return json.load(handle)
        except (json.JSONDecodeError, OSError):
            return {}

    def write(self, data: Dict[str, Any]) -> None:
        """Atomically overwrite payload.json with the provided dictionary."""
        temp_path = self._payload_path.with_suffix(".tmp")
        with temp_path.open("w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2, ensure_ascii=False)
            handle.flush()
            os.fsync(handle.fileno())
        shutil.move(str(temp_path), str(self._payload_path))

    def get(self, key: str, default: Any = None) -> Any:
        """Read a single key from payload.json."""
        return self.read().get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Update a single key in payload.json without overwriting other keys."""
        data = self.read()
        data[key] = value
        self.write(data)

    def update(self, mapping: Dict[str, Any]) -> None:
        """Merge a dictionary into payload.json."""
        data = self.read()
        data.update(mapping)
        self.write(data)


# ---------------------------------------------------------------------------
# LazyOwnCommandBuilder
# ---------------------------------------------------------------------------


class LazyOwnCommandBuilder:
    """Builds safe, validated command sequences for LazyOwn execution.

    LazyOwn is a cmd2-based shell.  The ``run`` launcher script supports
    passing arguments through to ``python3 lazyown.py``.  cmd2 interprets
    ``-c <command>`` as a startup command, runs it, and then enters the
    interactive loop.  To avoid hanging, an ``exit`` command is piped into
    stdin so the shell terminates cleanly after the startup command finishes.
    """

    _SHELL_RUNNER: str = "bash"
    _PYTHON_WARNING_FLAG: str = "-W"
    _PYTHON_WARNING_VALUE: str = "ignore"
    _CMD2_COMMAND_FLAG: str = _Defaults.CMD2_COMMAND_FLAG
    _EXIT_COMMAND: str = _Defaults.EXIT_COMMAND
    _STDIN_PIPE_TEMPLATE: str = "{command}\n{exit}\n"

    def __init__(self, lazyown_dir: Path) -> None:
        self._lazyown_dir = lazyown_dir
        self._run_script = lazyown_dir / _FileName.RUN_SCRIPT.value
        self._python_script = lazyown_dir / _FileName.PYTHON_SCRIPT.value

    def build_argv(self, command: str) -> Tuple[List[str], str]:
        """Return the subprocess argv and the stdin payload.

        Args:
            command: The LazyOwn command to execute (e.g. "lazynmap 10.10.11.78").

        Returns:
            A tuple of (argv list, stdin string).
        """
        validated = self._validate_command(command)
        stdin_payload = self._STDIN_PIPE_TEMPLATE.format(
            command=validated, exit=self._EXIT_COMMAND
        )

        if self._run_script.exists():
            argv = [
                self._SHELL_RUNNER,
                str(self._run_script),
                self._CMD2_COMMAND_FLAG,
                validated,
            ]
        else:
            argv = [
                shutil.which("python3") or "python3",
                self._PYTHON_WARNING_FLAG,
                self._PYTHON_WARNING_VALUE,
                str(self._python_script),
                self._CMD2_COMMAND_FLAG,
                validated,
            ]

        return argv, stdin_payload

    @staticmethod
    def _validate_command(command: str) -> str:
        """Sanitize a command string to prevent injection.

        Rejects shell metacharacters that are not part of normal LazyOwn usage.
        """
        forbidden = {";", "&", "|", "<", ">", "`", "$", "(", ")"}
        if any(ch in forbidden for ch in command):
            raise ValueError(
                f"Command contains forbidden characters: {forbidden}"
            )
        return command.strip()


# ---------------------------------------------------------------------------
# LazyOwnProcessExecutor
# ---------------------------------------------------------------------------


class LazyOwnProcessExecutor:
    """Executes LazyOwn commands as subprocesses with timeout and cleanup.

    Uses a PTY when available to satisfy cmd2 terminal-size expectations,
    but falls back to a plain pipe on platforms where PTY is unavailable.
    """

    _PTY_AVAILABLE: bool = True
    _TRY_PTY: bool = True
    _ENV_TERM: str = "xterm-256color"
    _DEFAULT_TIMEOUT: int = _Defaults.TIMEOUT_SECONDS
    _FAST_TIMEOUT: int = _Defaults.FAST_TIMEOUT_SECONDS
    _READ_CHUNK: int = _Defaults.READ_CHUNK_BYTES
    _POLL_INTERVAL: float = _Defaults.POLL_INTERVAL_SECONDS
    _KILL_GRACE_PERIOD: int = 2
    _TERMINAL_ROWS: int = 50
    _TERMINAL_COLS: int = 220

    _FAST_COMMANDS: Tuple[str, ...] = (
        "get_config",
        "set_config",
        "targets",
        "list_targets",
        "sessions",
        "beacons",
        "list",
        "modules",
        "discover",
        "status",
        "poll",
        "config",
        "assign",
        "show",
        "payload",
        "ctx",
    )

    def __init__(self, lazyown_dir: Path) -> None:
        self._lazyown_dir = lazyown_dir
        try:
            import fcntl, pty, select, struct, termios
            self._pty = pty
            self._fcntl = fcntl
            self._select = select
            self._struct = struct
            self._termios = termios
        except ImportError:
            self._TRY_PTY = False

    def execute(
        self,
        argv: List[str],
        stdin_payload: str,
        timeout: Optional[int] = None,
    ) -> Tuple[str, int, float]:
        """Run a command and return (raw_stdout, returncode, latency_ms).

        Args:
            argv: The subprocess argument vector.
            stdin_payload: Text to feed into stdin.
            timeout: Optional override for the process timeout in seconds.

        Returns:
            Tuple of (stdout text, return code, elapsed milliseconds).
        """
        effective_timeout = self._resolve_timeout(argv, timeout)
        env = {**os.environ, "TERM": self._ENV_TERM}
        t0 = time.monotonic()

        if self._TRY_PTY:
            stdout, returncode = self._execute_with_pty(
                argv, stdin_payload, effective_timeout, env
            )
        else:
            stdout, returncode = self._execute_with_pipe(
                argv, stdin_payload, effective_timeout, env
            )

        latency_ms = (time.monotonic() - t0) * 1000.0
        return stdout, returncode, latency_ms

    def _resolve_timeout(
        self, argv: List[str], override: Optional[int]
    ) -> int:
        if override is not None:
            return override
        command_str = " ".join(argv)
        lower = command_str.lower()
        for hint in self._FAST_COMMANDS:
            if hint in lower:
                return self._FAST_TIMEOUT
        return self._DEFAULT_TIMEOUT

    def _execute_with_pty(
        self,
        argv: List[str],
        stdin_payload: str,
        timeout: int,
        env: Dict[str, str],
    ) -> Tuple[str, int]:
        master_fd, slave_fd = self._pty.openpty()
        winsize = self._struct.pack(
            "HHHH",
            self._TERMINAL_ROWS,
            self._TERMINAL_COLS,
            0,
            0,
        )
        self._fcntl.ioctl(slave_fd, self._termios.TIOCSWINSZ, winsize)

        proc = subprocess.Popen(
            argv,
            stdin=subprocess.PIPE,
            stdout=slave_fd,
            stderr=slave_fd,
            env=env,
            cwd=str(self._lazyown_dir),
            start_new_session=True,
        )
        os.close(slave_fd)

        try:
            proc.stdin.write(stdin_payload.encode())
            proc.stdin.close()
        except BrokenPipeError:
            pass

        chunks: List[str] = []
        deadline = time.monotonic() + timeout
        try:
            while True:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    proc.kill()
                    break
                readable, _, _ = self._select.select(
                    [master_fd], [], [], min(remaining, self._POLL_INTERVAL)
                )
                if readable:
                    try:
                        data = os.read(master_fd, self._READ_CHUNK)
                        if data:
                            chunks.append(data.decode("utf-8", errors="replace"))
                    except OSError:
                        break
                elif proc.poll() is not None:
                    self._drain_pty(master_fd, chunks)
                    break
        finally:
            try:
                os.close(master_fd)
            except OSError:
                pass

        returncode = self._wait_or_kill(proc)
        return "".join(chunks), returncode

    def _drain_pty(self, master_fd: int, chunks: List[str]) -> None:
        try:
            while True:
                readable, _, _ = self._select.select([master_fd], [], [], self._POLL_INTERVAL)
                if not readable:
                    break
                data = os.read(master_fd, self._READ_CHUNK)
                if not data:
                    break
                chunks.append(data.decode("utf-8", errors="replace"))
        except OSError:
            pass

    def _execute_with_pipe(
        self,
        argv: List[str],
        stdin_payload: str,
        timeout: int,
        env: Dict[str, str],
    ) -> Tuple[str, int]:
        proc = subprocess.Popen(
            argv,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=env,
            cwd=str(self._lazyown_dir),
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        try:
            stdout, _ = proc.communicate(
                input=stdin_payload, timeout=timeout
            )
        except subprocess.TimeoutExpired:
            proc.kill()
            stdout, _ = proc.communicate(timeout=self._KILL_GRACE_PERIOD)
        return stdout, proc.returncode

    def _wait_or_kill(self, proc: subprocess.Popen) -> int:
        try:
            proc.wait(timeout=self._KILL_GRACE_PERIOD)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=self._KILL_GRACE_PERIOD)
        return proc.returncode


# ---------------------------------------------------------------------------
# LazyOwnOutputSanitizer
# ---------------------------------------------------------------------------


class LazyOwnOutputSanitizer:
    """Cleans raw LazyOwn output for downstream consumption.

    Strips ANSI escape sequences, framework bootstrap noise, and collapses
    redundant blank lines.
    """

    _ANSI_PATTERN = re.compile(
        r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])"
    )
    _BLANK_LINE_PATTERN = re.compile(r"\n\s*\n+")
    _LONG_NON_ALPHA_PATTERN = re.compile(r"^[^a-zA-Z]{80,}\s*$", re.MULTILINE)

    _NOISE_PATTERNS: Tuple[re.Pattern[str], ...] = (
        re.compile(r"Environment Activated\s*"),
        re.compile(r"\[\+\]\s*Command\s+'[^']+'\s+registere?d?.*?\[.\]"),
        re.compile(r"\[-\]\s*Not scan file please run nmap before.*?\[.\]"),
        re.compile(r"\[\+\]\s*LazyOwn framework started.*"),
        re.compile(r"\[\!\]\s*WARNING:.*"),
        re.compile(r"\{\s*\"status\"\s*:\s*\"ok\"\s*\}"),
    )

    def sanitize(self, text: str) -> str:
        """Return a cleaned version of the raw LazyOwn output."""
        cleaned = self._ANSI_PATTERN.sub("", text)
        for pattern in self._NOISE_PATTERNS:
            cleaned = pattern.sub("", cleaned)
        cleaned = self._LONG_NON_ALPHA_PATTERN.sub("", cleaned)
        cleaned = self._BLANK_LINE_PATTERN.sub("\n\n", cleaned)
        return cleaned.strip()


# ---------------------------------------------------------------------------
# LazyOwnBridge
# ---------------------------------------------------------------------------


class LazyOwnBridge:
    """High-level bridge between TopoSwarm and LazyOwn.

    Responsibilities:
      - Discover the LazyOwn installation directory.
      - Read and write payload.json to maintain state across invocations.
      - Build safe command invocations.
      - Execute commands with timeout and cleanup.
      - Sanitize output for downstream processing.

    This class is intentionally thin; all heavy lifting is delegated to the
    composed collaborator classes so that each can be tested in isolation.
    """

    def __init__(self) -> None:
        self._resolver = LazyOwnPathResolver()
        self._lazyown_dir: Optional[Path] = None
        self._payload: Optional[LazyOwnPayloadManager] = None
        self._builder: Optional[LazyOwnCommandBuilder] = None
        self._executor: Optional[LazyOwnProcessExecutor] = None
        self._sanitizer = LazyOwnOutputSanitizer()

    @property
    def lazyown_dir(self) -> Path:
        if self._lazyown_dir is None:
            self._lazyown_dir = self._resolver.resolve()
        return self._lazyown_dir

    @property
    def payload(self) -> LazyOwnPayloadManager:
        if self._payload is None:
            self._payload = LazyOwnPayloadManager(self.lazyown_dir)
        return self._payload

    @property
    def builder(self) -> LazyOwnCommandBuilder:
        if self._builder is None:
            self._builder = LazyOwnCommandBuilder(self.lazyown_dir)
        return self._builder

    @property
    def executor(self) -> LazyOwnProcessExecutor:
        if self._executor is None:
            self._executor = LazyOwnProcessExecutor(self.lazyown_dir)
        return self._executor

    @property
    def available(self) -> bool:
        try:
            return self.lazyown_dir.exists() and (
                (self.lazyown_dir / _FileName.RUN_SCRIPT.value).exists()
                or (self.lazyown_dir / _FileName.PYTHON_SCRIPT.value).exists()
            )
        except FileNotFoundError:
            return False

    def run(self, command: str, timeout: Optional[int] = None) -> ExecutionResult:
        """Execute a LazyOwn command and return a structured result.

        Args:
            command: The command string to send to LazyOwn.
            timeout: Optional timeout override in seconds.

        Returns:
            An ExecutionResult containing raw and cleaned output, return code,
            latency, and a success flag.
        """
        if not self.available:
            return ExecutionResult(
                command=command,
                raw_output="",
                cleaned_output=f"[LazyOwn not found at {self.lazyown_dir}]",
                returncode=-1,
                latency_ms=0.0,
                ok=False,
            )

        argv, stdin_payload = self.builder.build_argv(command)
        raw_output, returncode, latency_ms = self.executor.execute(
            argv, stdin_payload, timeout
        )
        cleaned_output = self._sanitizer.sanitize(raw_output)

        return ExecutionResult(
            command=command,
            raw_output=raw_output,
            cleaned_output=cleaned_output,
            returncode=returncode,
            latency_ms=latency_ms,
            ok=returncode == 0,
        )

    def run_clean(self, command: str, timeout: Optional[int] = None) -> str:
        """Execute a LazyOwn command and return the cleaned output string.

        This is a convenience wrapper over ``run()`` for callers that only need
        the human-readable output.
        """
        return self.run(command, timeout).cleaned_output

    def get_config(self) -> Dict[str, Any]:
        """Return the current LazyOwn configuration from payload.json."""
        return self.payload.read()

    def set_config(self, key: str, value: Any) -> str:
        """Update a single configuration key in payload.json.

        Returns:
            A human-readable confirmation string.
        """
        self.payload.set(key, value)
        return f"Set {key}={value!r} in payload.json"

    def set_target(self, ip: str) -> None:
        """Convenience method to set the remote target host."""
        self.payload.set("rhost", ip)

    def get_target(self) -> Optional[str]:
        """Return the currently configured remote target host."""
        return self.payload.get("rhost")
