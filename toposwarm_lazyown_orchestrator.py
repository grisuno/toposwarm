#!/usr/bin/env python3
"""
TopoSwarm → LazyOwn MCP Orchestrator
======================================
Uses the trained TopoSwarm router as the brain for LazyOwn's pentesting MCP.

Architecture
------------
    User prompt (NL)
         ↓
  TopoSwarm Router  ←── loaded from checkpoints_toposwarm/
  (keyword + model)
         ↓  (tool_name, tool_arg)
  LazyOwn Bridge    ←── calls LazyOwn via PTY subprocess
         ↓  (raw output)
  Template / Pass-2 answer
         ↓
  Final answer (printed or returned to MCP caller)

The file is also a proper MCP server: run it with stdio transport so
Claude Code / Claude Web can connect and invoke all LazyOwn tools through
the TopoSwarm router.

Modes
-----
  python toposwarm_lazyown_orchestrator.py --prompt "scan 10.10.11.78"
  python toposwarm_lazyown_orchestrator.py --mcp           # stdio MCP server
  python toposwarm_lazyown_orchestrator.py --gen-dataset   # build finetune JSONL
  python toposwarm_lazyown_orchestrator.py --finetune      # retrain on LazyOwn traces

Author: Gris Iscomeback  —  GPL v3
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import logging
import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Resolve paths  ( LazyOwn directory discovery )
# ---------------------------------------------------------------------------

_HERE = Path(__file__).parent.resolve()


def _resolve_lazyown_dir() -> Path:
    """
    Discover LazyOwn installation directory.

    Priority:
      1. LAZYOWN_DIR environment variable (expanded ~).
      2. Default relative to this script: <repo>/LazyOwn.
      3. User home directory: ~/LazyOwn.
      4. Return the relative default anyway (caller will see available=False).
    """
    # 1. Explicit env variable
    env_dir = os.environ.get("LAZYOWN_DIR", "")
    if env_dir:
        p = Path(env_dir).expanduser().resolve()
        if p.exists():
            return p

    # 2. Default relative to script location
    rel = (_HERE.parent.parent / "LazyOwn").resolve()
    if rel.exists():
        return rel

    # 3. Fallback to user's home directory
    home = (Path.home() / "LazyOwn").resolve()
    if home.exists():
        return home

    # 4. Final fallback (may not exist, but consistent)
    return rel


_LAZYOWN_DIR = _resolve_lazyown_dir()

# ---------------------------------------------------------------------------
# Import toposwarm_infer from the same directory
# ---------------------------------------------------------------------------

def _import_infer() -> Any:
    candidates = [_HERE / "toposwarm_infer.py", Path.cwd() / "toposwarm_infer.py"]
    for c in candidates:
        if c.exists():
            spec = importlib.util.spec_from_file_location("toposwarm_infer", c)
            mod  = importlib.util.module_from_spec(spec)
            sys.modules["toposwarm_infer"] = mod
            spec.loader.exec_module(mod)
            return mod
    raise FileNotFoundError("toposwarm_infer.py not found next to this script")

_infer = _import_infer()
InferenceEngine  = _infer.InferenceEngine
InferenceConfig  = _infer.InferenceConfig
InferenceResult  = _infer.InferenceResult
ToolRegistry     = _infer.ToolRegistry
ToolResult       = _infer.ToolResult
ToolCallParser   = _infer.ToolCallParser

# We also need SwarmConfig + training helpers for fine-tune mode
def _import_agent() -> Any:
    candidates = [_HERE / "topo_swarm_agent.py", Path.cwd() / "topo_swarm_agent.py"]
    for c in candidates:
        if c.exists():
            spec = importlib.util.spec_from_file_location("topo_swarm_agent", c)
            mod  = importlib.util.module_from_spec(spec)
            sys.modules["topo_swarm_agent"] = mod
            spec.loader.exec_module(mod)
            return mod
    raise FileNotFoundError("topo_swarm_agent.py not found")

# ---------------------------------------------------------------------------
# Import Meta-Harness module
# ---------------------------------------------------------------------------

def _import_meta_harness() -> Any:
    candidates = [_HERE / "toposwarm_meta_harness.py", Path.cwd() / "toposwarm_meta_harness.py"]
    for c in candidates:
        if c.exists():
            spec = importlib.util.spec_from_file_location("toposwarm_meta_harness", c)
            mod  = importlib.util.module_from_spec(spec)
            sys.modules["toposwarm_meta_harness"] = mod
            spec.loader.exec_module(mod)
            return mod
    return None

_meta = _import_meta_harness()

_agent = _import_agent()
SwarmConfig = _agent.SwarmConfig

# ---------------------------------------------------------------------------
# Optional RoutingHead import (from continual trainer)
# ---------------------------------------------------------------------------
def _import_routing_head() -> Optional[Any]:
    candidates = [
        _HERE / "toposwarm_continual_trainer.py",
        Path.cwd() / "toposwarm_continual_trainer.py",
    ]
    for c in candidates:
        if c.exists():
            spec = importlib.util.spec_from_file_location("toposwarm_continual_trainer", c)
            mod = importlib.util.module_from_spec(spec)
            sys.modules["toposwarm_continual_trainer"] = mod
            spec.loader.exec_module(mod)
            return getattr(mod, "RoutingHead", None)
    return None

_RoutingHeadCls = _import_routing_head()


# ===========================================================================
# Session Context — multi-turn persistent memory
# ===========================================================================


@dataclass
class SessionContext:
    """Persistent session state across multiple prompts."""

    target_ip: Optional[str] = None
    current_phase: str = "recon"
    findings: List[str] = field(default_factory=list)
    last_tool: Optional[str] = None
    last_arg: Optional[str] = None
    history: List[Dict[str, Any]] = field(default_factory=list)
    turn_count: int = 0

    def to_prompt_prefix(self) -> str:
        """Compact context block injected before the user prompt."""
        parts: List[str] = []
        if self.target_ip:
            parts.append(f"Target: {self.target_ip}")
        if self.last_tool:
            parts.append(f"Last action: {self.last_tool}({self.last_arg or ''})")
        if self.findings:
            parts.append(f"Findings: {'; '.join(self.findings[-3:])}")
        if not parts:
            return ""
        parts.append(f"Phase: {self.current_phase}")
        return "[Context] " + " | ".join(parts) + "\n\n"

    def update(self, tool_name: str, arg: str, output: str, ok: bool) -> None:
        self.last_tool = tool_name
        self.last_arg = arg
        self.turn_count += 1
        self.history.append(
            {
                "turn": self.turn_count,
                "tool": tool_name,
                "arg": arg,
                "ok": ok,
                "output_preview": output[:200],
            }
        )
        # Auto-extract target IP from arguments
        ip_m = re.search(r"\b(\d{1,3}(?:\.\d{1,3}){3}(?:/\d+)?)\b", arg)
        if ip_m and not self.target_ip:
            self.target_ip = ip_m.group(1)
        # Simple phase progression heuristics
        if ok and tool_name in ("lazyown_run_command", "lazyown_add_target"):
            if self.current_phase == "recon":
                self.current_phase = "exploit"
        if "credential" in output.lower() or "password" in output.lower():
            self.findings.append("credentials found")
        if "root" in output.lower() or "admin" in output.lower() or "nt authority" in output.lower():
            self.findings.append("privilege escalation possible")


# ===========================================================================
# LazyOwn Bridge — PTY subprocess executor
# ===========================================================================


class LazyOwnBridge:
    """
    Thin wrapper around LazyOwn's _run_lazyown_command logic.

    Calls LazyOwn non-interactively via a PTY subprocess so the terminal-size
    ioctl does not crash.  Strips ANSI codes from output.

    All heavy imports (pty, fcntl, termios, select, struct) are lazy so the
    bridge can be imported on non-Linux systems for dataset generation.
    """

    _ANSI = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    # Strip noisy LazyOwn bootstrap spam (activation banners, Lua/YAML registration, etc.)
    _NOISE_PATTERNS = [
        re.compile(r"Environment Activated\s*"),
        re.compile(r"\[\+\]\s*Command\s+'[^']+'\s+registere?d?.*?\[.\]"),
        re.compile(r"\[-\]\s*Not scan file please run nmap before.*?\[.\]"),
        re.compile(r"\[\+\]\s*LazyOwn framework started.*"),
        re.compile(r"\[\!\]\s*WARNING:.*"),
        re.compile(r"\{\s*\"status\"\s*:\s*\"ok\"\s*\}"),
        # Strip very long lines with no alphabetic characters (banner art, dividers)
        re.compile(r"^[^a-zA-Z]{80,}\s*$", re.MULTILINE),
    ]

    def __init__(self, lazyown_dir: Path = _LAZYOWN_DIR, default_timeout: int = 30) -> None:
        self.lazyown_dir    = lazyown_dir
        self.default_timeout = default_timeout
        self._available: Optional[bool] = None

    @property
    def available(self) -> bool:
        if self._available is None:
            self._available = self.lazyown_dir.exists() and (
                (self.lazyown_dir / "lazyown.py").exists()
                or (self.lazyown_dir / "run").exists()
            )
        return self._available

    def run(self, command: str, timeout: Optional[int] = None) -> str:
        """Execute a LazyOwn shell command and return cleaned output."""
        if not self.available:
            return f"[LazyOwn not found at {self.lazyown_dir}]"
        timeout = timeout or self.default_timeout
        try:
            import fcntl, pty, select, struct, termios
        except ImportError:
            return "[PTY not available on this platform]"

        cmd_input = (command.strip() + "\nexit\n").encode()
        run_script = self.lazyown_dir / "run"
        argv = (
            ["bash", str(run_script)]
            if run_script.is_file()
            else [sys.executable, "-W", "ignore", str(self.lazyown_dir / "lazyown.py")]
        )
        env = {**os.environ, "TERM": "xterm-256color"}

        master_fd, slave_fd = pty.openpty()
        fcntl.ioctl(slave_fd, termios.TIOCSWINSZ, struct.pack("HHHH", 50, 220, 0, 0))
        try:
            proc = subprocess.Popen(
                argv, stdin=subprocess.PIPE, stdout=slave_fd, stderr=slave_fd,
                env=env, cwd=str(self.lazyown_dir), start_new_session=True,
            )
            os.close(slave_fd)
            try:
                proc.stdin.write(cmd_input)
                proc.stdin.close()
            except BrokenPipeError:
                pass

            chunks: List[str] = []
            deadline = time.monotonic() + timeout
            while True:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    proc.kill()
                    break
                r, _, _ = select.select([master_fd], [], [], min(remaining, 0.5))
                if r:
                    try:
                        data = os.read(master_fd, 4096)
                        if data:
                            chunks.append(data.decode("utf-8", errors="replace"))
                    except OSError:
                        break
                elif proc.poll() is not None:
                    try:
                        while True:
                            r2, _, _ = select.select([master_fd], [], [], 0.1)
                            if not r2:
                                break
                            data = os.read(master_fd, 4096)
                            if not data:
                                break
                            chunks.append(data.decode("utf-8", errors="replace"))
                    except OSError:
                        pass
                    break
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
        finally:
            try:
                os.close(master_fd)
            except OSError:
                pass

        raw = "".join(chunks)
        cleaned = self._ANSI.sub("", raw)
        for pat in self._NOISE_PATTERNS:
            cleaned = pat.sub("", cleaned)
        # Collapse multiple blank lines to a single blank line
        cleaned = re.sub(r"\n\s*\n+", "\n\n", cleaned)
        return cleaned.strip()

    def get_config(self) -> Dict[str, Any]:
        payload_path = self.lazyown_dir / "payload.json"
        if payload_path.exists():
            try:
                return json.loads(payload_path.read_text())
            except Exception:
                pass
        return {}

    def set_config(self, key: str, value: str) -> str:
        payload_path = self.lazyown_dir / "payload.json"
        data = self.get_config()
        try:
            data[key] = int(value)
        except ValueError:
            try:
                data[key] = float(value)
            except ValueError:
                data[key] = value
        payload_path.write_text(json.dumps(data, indent=2))
        return f"Set {key}={value!r} in payload.json"


# ===========================================================================
# LazyOwn Tool Registry
# ===========================================================================


class LazyOwnToolRegistry(ToolRegistry):
    """
    Extends TopoSwarm's ToolRegistry with all LazyOwn MCP tools.

    Each tool is a thin wrapper that calls LazyOwnBridge.run() with the
    appropriate LazyOwn shell command or payload manipulation.

    Tools are grouped by category so keyword routing maps naturally.
    """

    # Keyword clusters used by the router to pick a tool
    _KEYWORD_MAP: Dict[str, List[str]] = {
        # Reconnaissance
        "lazyown_run_command":       ["nmap", "scan", "enumerate", "lazymsfconsole",
                                      "lazynmap", "execute", "run", "command", "shell"],
        "lazyown_list_modules":      ["module", "modules", "list modules", "available"],
        "lazyown_discover_commands": ["discover", "commands", "help", "what can"],
        # Targets
        "lazyown_add_target":        ["add target", "new target", "target add"],
        "lazyown_list_targets":      ["list target", "targets", "scope", "hosts"],
        "lazyown_set_active_target": ["active target", "select target", "set target"],
        # Configuration
        "lazyown_get_config":        ["get config", "show config", "payload", "configuration"],
        "lazyown_set_config":        ["set config", "configure", "set rhost", "set lhost",
                                      "set port", "set domain", "update config"],
        # C2 / Sessions
        "lazyown_get_beacons":       ["beacon", "beacons", "implant", "agent list"],
        "lazyown_list_sessions":     ["session", "sessions", "active sessions"],
        "lazyown_c2_command":        ["c2", "command and control", "remote command", "c2 cmd"],
        "lazyown_c2_status":         ["c2 status", "server status", "is c2 up"],
        # Agents
        "lazyown_run_agent":         ["run agent", "start agent", "launch agent",
                                      "groq", "ollama", "delegate"],
        "lazyown_agent_status":      ["agent status", "agent progress", "check agent"],
        "lazyown_agent_result":      ["agent result", "agent output", "agent done"],
        "lazyown_list_agents":       ["list agents", "active agents", "agents running"],
        # Intelligence / research
        "lazyown_c2_search_agent":   ["search", "find technique", "mitre", "osint",
                                      "look up", "research", "query knowledge"],
        "lazyown_recommend_next":    ["recommend", "next step", "what next", "suggest"],
        "lazyown_phase_guide":       ["phase", "kill chain", "methodology", "step by step"],
        "lazyown_campaign_sitrep":   ["sitrep", "status", "overview", "campaign status",
                                      "report status"],
        # Vulnerability / exploitation
        "lazyown_c2_vuln_analysis":  ["vuln", "vulnerability", "cve", "exploit",
                                      "weakness", "attack surface"],
        "lazyown_c2_redop":          ["red op", "red team", "attack plan", "operation"],
        "lazyown_c2_adversary":      ["adversary", "threat actor", "ttp", "mitre att&ck"],
        # Events / rules
        "lazyown_poll_events":       ["event", "events", "alert", "trigger"],
        "lazyown_ack_event":         ["ack event", "acknowledge", "dismiss event"],
        "lazyown_add_rule":          ["add rule", "new rule", "detection rule"],
        "lazyown_list_event_rules":  ["list rules", "show rules", "detection rules"],
        "lazyown_heartbeat_status":  ["heartbeat", "health check", "alive"],
        # Reporting
        "lazyown_report_update":     ["report", "write report", "update report"],
        "lazyown_campaign_lessons":  ["lessons", "lessons learned", "retrospective"],
        "lazyown_c2_notes":          ["note", "notes", "observation", "finding"],
        "lazyown_credentials":       ["credential", "creds", "password", "hash", "loot"],
        "lazyown_timeline":          ["timeline", "history", "chronology", "events log"],
        # Automation
        "lazyown_auto_loop":         ["auto loop", "automate", "automation", "loop mode"],
        "lazyown_auto_populate":     ["auto populate", "fill config", "auto config"],
        "lazyown_session_init":      ["init session", "start session", "new session"],
        "lazyown_session_state":     ["session state", "current state", "context"],
        # LLM / AI
        "lazyown_llm_ask":           ["ask llm", "ask ai", "llm", "gpt", "language model"],
        "lazyown_create_tool":       ["create tool", "new tool", "add tool", "tool file"],
        "lazyown_inject_objective":  ["inject objective", "add objective", "objective"],
        "lazyown_next_objective":    ["next objective", "current objective", "what objective"],
        "lazyown_read_prompt":       ["read prompt", "prompt file", "system prompt"],
        # Addons / plugins
        "lazyown_create_addon":      ["create addon", "new addon", "add addon", "github tool"],
        "lazyown_list_addons":       ["list addons", "addons", "extensions"],
        "lazyown_list_plugins":      ["list plugins", "plugins"],
        # Sessions / files
        "lazyown_read_session_file": ["read file", "session file", "output file"],
        "lazyown_run_api":           ["api", "rest api", "curl", "http request"],
        "lazyown_c2_script":         ["script", "run script", "automation script"],
        "lazyown_policy_status":     ["policy", "compliance", "rules of engagement"],
        "lazyown_command_help":      ["command help", "explain command", "how to use"],
    }

    def __init__(self, cfg: InferenceConfig, bridge: LazyOwnBridge) -> None:
        super().__init__(cfg)
        self.bridge = bridge
        self._register_lazyown_tools()

    def _register_lazyown_tools(self) -> None:
        """Register every LazyOwn MCP tool as a ToolRegistry callable."""
        b = self.bridge

        # ── Core command execution ────────────────────────────────────────
        @self.register("lazyown_run_command", "lazyown_cmd", "lazyown_exec")
        def run_command(arg: str) -> str:
            return b.run(arg)

        @self.register("lazyown_get_config", "lazyown_config", "lazyown_payload")
        def get_config(_: str) -> str:
            data = b.get_config()
            return json.dumps(data, indent=2)[:self.cfg.MAX_RESULT_CHARS]

        @self.register("lazyown_set_config")
        def set_config(arg: str) -> str:
            # Accept "key=value" or "key value"
            parts = arg.split("=", 1) if "=" in arg else arg.split(None, 1)
            if len(parts) == 2:
                return b.set_config(parts[0].strip(), parts[1].strip())
            return f"Usage: lazyown_set_config key=value  (got: {arg!r})"

        @self.register("lazyown_list_modules")
        def list_modules(_: str) -> str:
            return b.run("list")

        @self.register("lazyown_get_beacons", "lazyown_beacons")
        def get_beacons(_: str) -> str:
            return b.run("beacons")

        @self.register("lazyown_c2_command", "lazyown_c2")
        def c2_command(arg: str) -> str:
            return b.run(f"c2 {arg}")

        @self.register("lazyown_run_api", "lazyown_api")
        def run_api(arg: str) -> str:
            return b.run(f"lazyapiattack {arg}")

        @self.register("lazyown_list_sessions", "lazyown_sessions")
        def list_sessions(_: str) -> str:
            sessions_dir = b.lazyown_dir / "sessions"
            if not sessions_dir.exists():
                return "No sessions directory found"
            entries = [p.name for p in sessions_dir.iterdir() if p.is_dir()]
            return "\n".join(entries) or "No sessions found"

        @self.register("lazyown_read_session_file")
        def read_session_file(arg: str) -> str:
            p = b.lazyown_dir / "sessions" / arg
            if p.exists():
                return p.read_text()[:self.cfg.MAX_RESULT_CHARS]
            return f"File not found: {arg}"

        @self.register("lazyown_c2_status", "lazyown_status")
        def c2_status(_: str) -> str:
            return b.run("status")

        @self.register("lazyown_create_addon", "lazyown_addon")
        def create_addon(arg: str) -> str:
            return b.run(f"createaddon {arg}")

        @self.register("lazyown_list_addons")
        def list_addons(_: str) -> str:
            addons_dir = b.lazyown_dir / "lazyaddons"
            if not addons_dir.exists():
                return "No addons directory"
            return "\n".join(p.name for p in addons_dir.iterdir())

        @self.register("lazyown_list_plugins")
        def list_plugins(_: str) -> str:
            plugins_dir = b.lazyown_dir / "plugins"
            if not plugins_dir.exists():
                return "No plugins directory"
            return "\n".join(p.name for p in plugins_dir.iterdir())

        @self.register("lazyown_poll_events", "lazyown_events")
        def poll_events(_: str) -> str:
            return b.run("events")

        @self.register("lazyown_ack_event")
        def ack_event(arg: str) -> str:
            return b.run(f"ackevent {arg}")

        @self.register("lazyown_add_rule", "lazyown_rule")
        def add_rule(arg: str) -> str:
            return b.run(f"addrule {arg}")

        @self.register("lazyown_list_event_rules", "lazyown_rules")
        def list_event_rules(_: str) -> str:
            return b.run("listrules")

        @self.register("lazyown_heartbeat_status", "lazyown_heartbeat")
        def heartbeat_status(_: str) -> str:
            return b.run("heartbeat")

        @self.register("lazyown_session_init", "lazyown_init")
        def session_init(arg: str) -> str:
            return b.run(f"sessioninit {arg}")

        @self.register("lazyown_discover_commands", "lazyown_discover")
        def discover_commands(arg: str) -> str:
            return b.run("help")

        @self.register("lazyown_phase_guide", "lazyown_phase")
        def phase_guide(arg: str) -> str:
            return b.run(f"phase {arg}")

        @self.register("lazyown_command_help", "lazyown_help")
        def command_help(arg: str) -> str:
            return b.run(f"help {arg}")

        @self.register("lazyown_add_target", "lazyown_target")
        def add_target(arg: str) -> str:
            parts = arg.split()
            cmd = f"addtarget {' '.join(parts)}"
            return b.run(cmd)

        @self.register("lazyown_list_targets", "lazyown_targets")
        def list_targets(_: str) -> str:
            return b.run("targets")

        @self.register("lazyown_run_agent", "lazyown_agent")
        def run_agent(arg: str) -> str:
            return b.run(f"runagent {arg}")

        @self.register("lazyown_agent_status")
        def agent_status(arg: str) -> str:
            return b.run(f"agentstatus {arg}")

        @self.register("lazyown_agent_result")
        def agent_result(arg: str) -> str:
            return b.run(f"agentresult {arg}")

        @self.register("lazyown_list_agents")
        def list_agents(_: str) -> str:
            return b.run("listagents")

        @self.register("lazyown_set_active_target")
        def set_active_target(arg: str) -> str:
            return b.run(f"settarget {arg}")

        @self.register("lazyown_campaign_sitrep", "lazyown_sitrep")
        def campaign_sitrep(_: str) -> str:
            return b.run("sitrep")

        @self.register("lazyown_c2_notes", "lazyown_notes")
        def c2_notes(arg: str) -> str:
            return b.run(f"notes {arg}")

        @self.register("lazyown_credentials", "lazyown_creds")
        def credentials(_: str) -> str:
            return b.run("creds")

        @self.register("lazyown_report_update", "lazyown_report")
        def report_update(arg: str) -> str:
            return b.run(f"report {arg}")

        @self.register("lazyown_campaign_lessons", "lazyown_lessons")
        def campaign_lessons(_: str) -> str:
            return b.run("lessons")

        @self.register("lazyown_auto_populate", "lazyown_autofill")
        def auto_populate(_: str) -> str:
            return b.run("autopopulate")

        @self.register("lazyown_session_state")
        def session_state(_: str) -> str:
            return b.run("sessionstate")

        @self.register("lazyown_recommend_next", "lazyown_recommend")
        def recommend_next(_: str) -> str:
            return b.run("recommend")

        @self.register("lazyown_timeline")
        def timeline(_: str) -> str:
            return b.run("timeline")

        @self.register("lazyown_c2_vuln_analysis", "lazyown_vulns")
        def c2_vuln_analysis(arg: str) -> str:
            return b.run(f"vulnanalysis {arg}")

        @self.register("lazyown_c2_redop", "lazyown_redop")
        def c2_redop(arg: str) -> str:
            return b.run(f"redop {arg}")

        @self.register("lazyown_c2_search_agent", "lazyown_search")
        def c2_search_agent(arg: str) -> str:
            return b.run(f"search {arg}")

        @self.register("lazyown_c2_script", "lazyown_script")
        def c2_script(arg: str) -> str:
            return b.run(f"runscript {arg}")

        @self.register("lazyown_c2_adversary", "lazyown_adversary")
        def c2_adversary(arg: str) -> str:
            return b.run(f"adversary {arg}")

        @self.register("lazyown_policy_status", "lazyown_policy")
        def policy_status(_: str) -> str:
            return b.run("policy")

        @self.register("lazyown_auto_loop", "lazyown_loop")
        def auto_loop(arg: str) -> str:
            return b.run(f"autoloop {arg}")

        @self.register("lazyown_create_tool", "lazyown_newtool")
        def create_tool(arg: str) -> str:
            return b.run(f"createtool {arg}")

        @self.register("lazyown_llm_ask", "lazyown_llm")
        def llm_ask(arg: str) -> str:
            return b.run(f"llmask {arg}")

        @self.register("lazyown_inject_objective", "lazyown_objective")
        def inject_objective(arg: str) -> str:
            return b.run(f"injectobjective {arg}")

        @self.register("lazyown_next_objective")
        def next_objective(_: str) -> str:
            return b.run("nextobjective")

        @self.register("lazyown_read_prompt", "lazyown_prompt")
        def read_prompt(arg: str) -> str:
            return b.run(f"readprompt {arg}")


# ===========================================================================
# Security keyword router
# ===========================================================================


def infer_lazyown_tool(prompt: str) -> Tuple[str, str]:
    """
    Map a natural-language security prompt to a (tool_name, tool_arg) pair.

    Priority: explicit LazyOwn keywords → security domain keywords → fallback.
    The returned tool_arg is the most useful sub-string to pass to that tool.
    """
    pl = prompt.lower()

    # ── Explicit tool name in prompt ──────────────────────────────────────
    for tool_name, keywords in LazyOwnToolRegistry._KEYWORD_MAP.items():
        if any(kw in pl for kw in keywords):
            arg = _extract_arg(prompt, tool_name)
            return tool_name, arg

    # ── IP / host patterns → nmap scan ───────────────────────────────────
    ip_match = re.search(r"\b(\d{1,3}(?:\.\d{1,3}){3}(?:/\d+)?)\b", prompt)
    if ip_match:
        ip = ip_match.group(1)
        return "lazyown_run_command", f"set rhost {ip}\nlazynmap"

    # ── Default: search agent ─────────────────────────────────────────────
    return "lazyown_c2_search_agent", prompt


def _extract_arg(prompt: str, tool_name: str) -> str:
    """Extract the most useful argument string for each tool category."""
    pl = prompt.lower()

    # IP address extraction
    ip_m = re.search(r"\b(\d{1,3}(?:\.\d{1,3}){3}(?:/\d+)?)\b", prompt)
    ip   = ip_m.group(1) if ip_m else ""

    if tool_name == "lazyown_run_command":
        # Try to extract a concrete shell command or build one from context
        cmd_m = re.search(
            r"(?:run|execute|use|launch)\s+['\"]?([a-z][a-z0-9_\-\s]+)['\"]?",
            pl
        )
        if cmd_m:
            return cmd_m.group(1).strip()
        if ip:
            return f"set rhost {ip}\nlazynmap"
        return prompt

    if tool_name in ("lazyown_set_config",):
        # "set rhost 10.10.11.1"  →  "rhost=10.10.11.1"
        m = re.search(r"\bset\s+(\w+)\s+(\S+)", pl)
        if m:
            return f"{m.group(1)}={m.group(2)}"
        if ip:
            return f"rhost={ip}"
        return prompt

    if tool_name in ("lazyown_add_target",):
        return ip or prompt

    if tool_name in ("lazyown_c2_search_agent", "lazyown_llm_ask"):
        return prompt

    if tool_name in ("lazyown_phase_guide",):
        # Extract phase name / number
        m = re.search(r"\bphase\s+(\w+)", pl)
        return m.group(1) if m else prompt

    return prompt


# ===========================================================================
# LazyOwn Orchestrator (main entry point for agentic inference)
# ===========================================================================


class LazyOwnOrchestrator:
    """
    Combines TopoSwarm router with LazyOwn tool execution.

    InferenceEngine is loaded only when needed (lazy) so the orchestrator
    can be used for dataset generation without a GPU.

    Meta-Harness integration (2026-05):
    - Filesystem experience store: every execution is logged with code,
      traces, and scores for future proposer diagnosis.
    - Environment bootstrap: gathers a LazyOwn sandbox snapshot before the
      first turn to eliminate wasted exploratory commands.
    - Draft-verification routing: retrieves confirmers/challengers from
      prior episodes to verify or revise the keyword router's draft.
    """

    def __init__(
        self,
        cfg: InferenceConfig,
        agent_cfg: SwarmConfig,
        bridge: LazyOwnBridge,
        logger: logging.Logger,
        load_model: bool = True,
        meta_cfg: Optional[Any] = None,
    ) -> None:
        self.cfg       = cfg
        self.agent_cfg = agent_cfg
        self.bridge    = bridge
        self.logger    = logger
        self._engine: Optional[InferenceEngine] = None
        self.registry  = LazyOwnToolRegistry(cfg, bridge)

        if load_model:
            self._engine = InferenceEngine(cfg, agent_cfg, logger)
            # Patch in our expanded registry
            self._engine.registry = self.registry

        # --- Neural Router (RoutingHead) -------------------------------------
        self._routing_head: Optional[Any] = None
        if _RoutingHeadCls is not None:
            self._routing_head = self._load_routing_head()

        # --- Session Context (multi-turn memory) -----------------------------
        self.session = SessionContext()

        # --- Meta-Harness ----------------------------------------------------
        self._mh: Optional[Any] = None
        self._snapshot_text: str = ""
        if _meta is not None:
            mh_cfg = meta_cfg or _meta.MetaHarnessConfig()
            self._mh = _meta.MetaHarnessOptimizer(mh_cfg)
            self._mh.set_router(infer_lazyown_tool)
            if mh_cfg.BOOTSTRAP_ENABLED and bridge.available:
                try:
                    snap = self._mh.bootstrap.gather_snapshot(bridge)
                    self._snapshot_text = self._mh.bootstrap.format_snapshot(snap)
                    self.logger.info("Meta-Harness env bootstrap gathered (%d chars)",
                                     len(self._snapshot_text))
                except Exception as exc:
                    self.logger.warning("Meta-Harness bootstrap failed: %s", exc)

    def _load_routing_head(self) -> Optional[Any]:
        """Load the trained RoutingHead if a checkpoint exists."""
        head_path = Path(self.agent_cfg.CHECKPOINT_DIR) / "routing_head.pt"
        if not head_path.exists():
            self.logger.info("No routing_head.pt found — neural routing disabled")
            return None
        try:
            head = _RoutingHeadCls.load(self.agent_cfg.D_MODEL, str(head_path))
            device = self.agent_cfg.DEVICE
            if "cuda" in device and __import__("torch").cuda.is_available():
                head = head.to(device)
            self.logger.info(
                "RoutingHead loaded: %d tools → %d classes on %s",
                head.n_tools,
                head.n_tools,
                device,
            )
            return head
        except Exception as exc:
            self.logger.warning("Failed to load RoutingHead: %s", exc)
            return None

    def _neural_route(self, prompt: str) -> Optional[Tuple[str, str]]:
        """
        Use the TopoSwarm model + RoutingHead to predict the LazyOwn tool.
        Returns (tool_name, tool_arg) or None if unavailable / uncertain.
        """
        if self._engine is None or self._routing_head is None:
            return None
        try:
            import torch
        except ImportError:
            return None
        tok = self._engine.tokenizer
        device = self.agent_cfg.DEVICE
        ids = torch.tensor([tok.encode(prompt)], dtype=torch.long, device=device)
        hidden_states: List[torch.Tensor] = []

        def _hook(module: Any, inp: Any, out: torch.Tensor) -> None:
            hidden_states.append(out)

        handle = self._engine.model.norm_out.register_forward_hook(_hook)
        try:
            with torch.no_grad():
                self._engine.model(ids)
        finally:
            handle.remove()
        if not hidden_states:
            return None
        # last token hidden state [1, D_MODEL]
        h = hidden_states[0][:, -1, :]
        logits = self._routing_head(h)
        probs = torch.softmax(logits, dim=-1)
        conf, idx = probs.max(dim=-1)
        if conf.item() < 0.5:
            self.logger.debug("Neural route confidence %.2f < 0.5 — falling back", conf.item())
            return None
        tool_name = self._routing_head.tool_names[idx.item()]
        arg = _extract_arg(prompt, tool_name)
        self.logger.info("Neural router → %s(%r) conf=%.2f", tool_name, arg[:80], conf.item())
        return tool_name, arg

    def run(self, prompt: str) -> InferenceResult:
        """Route prompt → LazyOwn tool → answer."""
        # --- Inject session context into prompt --------------------------------
        contextual_prompt = self.session.to_prompt_prefix() + prompt
        result = InferenceResult(prompt=contextual_prompt)
        t0 = time.monotonic()

        # --- Neural routing (primary) ------------------------------------------
        neural = self._neural_route(contextual_prompt)
        if neural is not None:
            tool_name, tool_arg = neural
        else:
            # --- Meta-Harness routing: draft-verify or fallback keyword ------
            if self._mh and self._mh.draft_verifier is not None:
                try:
                    tool_name, tool_arg, confidence = self._mh.draft_verifier.route(
                        contextual_prompt, self._snapshot_text
                    )
                    self.logger.info("Meta-Harness router → %s(%r) conf=%.2f",
                                     tool_name, tool_arg[:80], confidence)
                except Exception as exc:
                    self.logger.warning("Meta-Harness draft-verify failed (%s), falling back", exc)
                    tool_name, tool_arg = infer_lazyown_tool(contextual_prompt)
            else:
                tool_name, tool_arg = infer_lazyown_tool(contextual_prompt)
        result.tool_name = tool_name
        result.tool_arg  = tool_arg

        # Execute tool
        tool_result = self.registry.execute(tool_name, tool_arg)
        result.tool_result = tool_result
        result.tool_used   = True
        latency_ms = (time.monotonic() - t0) * 1000
        self.logger.info("Tool output (%d chars, %.1f ms)", len(tool_result.output), latency_ms)

        # Generate answer: use model pass-2 when available, else template
        if self._engine is not None:
            try:
                result.final_answer = self._engine._template_answer(
                    tool_name, tool_arg, tool_result
                )
            except Exception as exc:
                self.logger.warning("Pass-2 fallback: %s", exc)
                result.final_answer = f"{tool_name} result:\n{tool_result.output}"
        else:
            result.final_answer = f"{tool_name} result:\n{tool_result.output}"

        # --- Meta-Harness: log run to filesystem experience store ------------
        if self._mh is not None:
            try:
                harness_cfg = {
                    "orchestrator_version": "lazyown_mh_2026_05",
                    "tool_name": tool_name,
                    "bootstrap_len": len(self._snapshot_text),
                    "model_loaded": self._engine is not None,
                }
                trace_steps = [
                    {
                        "step": 1,
                        "prompt": prompt,
                        "tool": tool_name,
                        "arg": tool_arg,
                        "output": tool_result.output[:500],
                        "ok": tool_result.ok,
                        "t_ms": latency_ms,
                    }
                ]
                score = {
                    "prompt": prompt,
                    "success": tool_result.ok,
                    "latency_ms": latency_ms,
                    "context_chars": len(prompt) + len(self._snapshot_text) + len(tool_arg),
                    "output_chars": len(tool_result.output),
                }
                self._mh.log_run(harness_cfg, trace_steps, score)
            except Exception as exc:
                self.logger.debug("Meta-Harness log_run failed: %s", exc)

        # --- Update session context --------------------------------------------
        self.session.update(tool_name, tool_arg, tool_result.output, tool_result.ok)

        return result


# ===========================================================================
# Fine-tuning dataset generator
# ===========================================================================


_LAZYOWN_TRACES: List[Dict[str, Any]] = [
    # Reconnaissance
    {"instruction": "Scan for open ports on 10.10.11.78",
     "tool": "lazyown_run_command", "arg": "set rhost 10.10.11.78\nlazynmap",
     "domain": "Recon"},
    {"instruction": "Run a full nmap scan on 192.168.1.100",
     "tool": "lazyown_run_command", "arg": "set rhost 192.168.1.100\nlazynmap",
     "domain": "Recon"},
    {"instruction": "Enumerate services on target 172.16.0.5",
     "tool": "lazyown_run_command", "arg": "set rhost 172.16.0.5\nlazynmap",
     "domain": "Recon"},
    {"instruction": "List all available LazyOwn modules",
     "tool": "lazyown_list_modules", "arg": "",
     "domain": "Framework"},
    {"instruction": "What LazyOwn commands are available?",
     "tool": "lazyown_discover_commands", "arg": "",
     "domain": "Framework"},
    # Configuration
    {"instruction": "Set the target host to 10.10.11.50",
     "tool": "lazyown_set_config", "arg": "rhost=10.10.11.50",
     "domain": "Config"},
    {"instruction": "Configure lhost to 10.10.14.2",
     "tool": "lazyown_set_config", "arg": "lhost=10.10.14.2",
     "domain": "Config"},
    {"instruction": "Show the current LazyOwn configuration",
     "tool": "lazyown_get_config", "arg": "",
     "domain": "Config"},
    {"instruction": "Set the listening port to 4444",
     "tool": "lazyown_set_config", "arg": "lport=4444",
     "domain": "Config"},
    # Targets
    {"instruction": "Add 10.10.11.78 as a target in the campaign",
     "tool": "lazyown_add_target", "arg": "10.10.11.78",
     "domain": "Campaign"},
    {"instruction": "List all targets in scope",
     "tool": "lazyown_list_targets", "arg": "",
     "domain": "Campaign"},
    {"instruction": "Set 10.10.11.50 as the active target",
     "tool": "lazyown_set_active_target", "arg": "10.10.11.50",
     "domain": "Campaign"},
    # Sessions / C2
    {"instruction": "Show all active sessions",
     "tool": "lazyown_list_sessions", "arg": "",
     "domain": "C2"},
    {"instruction": "List connected beacons",
     "tool": "lazyown_get_beacons", "arg": "",
     "domain": "C2"},
    {"instruction": "Check C2 server status",
     "tool": "lazyown_c2_status", "arg": "",
     "domain": "C2"},
    {"instruction": "Send a command to all beacons: whoami",
     "tool": "lazyown_c2_command", "arg": "whoami",
     "domain": "C2"},
    # Vulnerability analysis
    {"instruction": "Analyze vulnerabilities found on 10.10.11.78",
     "tool": "lazyown_c2_vuln_analysis", "arg": "10.10.11.78",
     "domain": "Exploit"},
    {"instruction": "What CVEs affect the target services?",
     "tool": "lazyown_c2_vuln_analysis", "arg": "",
     "domain": "Exploit"},
    {"instruction": "Run adversary emulation for APT29",
     "tool": "lazyown_c2_adversary", "arg": "APT29",
     "domain": "Exploit"},
    # Intelligence
    {"instruction": "Search for SMB exploitation techniques",
     "tool": "lazyown_c2_search_agent", "arg": "SMB exploitation techniques",
     "domain": "Intel"},
    {"instruction": "Find MITRE techniques for lateral movement",
     "tool": "lazyown_c2_search_agent", "arg": "lateral movement MITRE ATT&CK",
     "domain": "Intel"},
    {"instruction": "What should be the next step after initial access?",
     "tool": "lazyown_recommend_next", "arg": "",
     "domain": "Intel"},
    {"instruction": "Guide me through the reconnaissance phase",
     "tool": "lazyown_phase_guide", "arg": "recon",
     "domain": "Intel"},
    # Reporting
    {"instruction": "Generate a campaign situation report",
     "tool": "lazyown_campaign_sitrep", "arg": "",
     "domain": "Report"},
    {"instruction": "Show collected credentials",
     "tool": "lazyown_credentials", "arg": "",
     "domain": "Report"},
    {"instruction": "Update the campaign report with new findings",
     "tool": "lazyown_report_update", "arg": "new findings",
     "domain": "Report"},
    {"instruction": "Show the attack timeline",
     "tool": "lazyown_timeline", "arg": "",
     "domain": "Report"},
    # Agents / AI
    {"instruction": "Ask the LLM agent to analyze the target",
     "tool": "lazyown_llm_ask", "arg": "analyze target 10.10.11.78",
     "domain": "AI"},
    {"instruction": "Run an AI agent to plan the attack on 10.10.11.78",
     "tool": "lazyown_run_agent", "arg": "plan attack 10.10.11.78",
     "domain": "AI"},
    {"instruction": "Check the status of the running agent",
     "tool": "lazyown_agent_status", "arg": "",
     "domain": "AI"},
    # Events / policy
    {"instruction": "Poll for new security events",
     "tool": "lazyown_poll_events", "arg": "",
     "domain": "Events"},
    {"instruction": "Show current policy and rules of engagement",
     "tool": "lazyown_policy_status", "arg": "",
     "domain": "Policy"},
    # Automation
    {"instruction": "Auto-populate the configuration from target scan",
     "tool": "lazyown_auto_populate", "arg": "",
     "domain": "Automation"},
    {"instruction": "Start the auto-loop for continuous enumeration",
     "tool": "lazyown_auto_loop", "arg": "",
     "domain": "Automation"},
]


def generate_dataset(output_path: Path, bridge: Optional[LazyOwnBridge] = None) -> int:
    """
    Generate a rich ToolBench-format JSONL for fine-tuning the TopoSwarm router.

    Uses lazyown_dataset_generator.py (80 tools × 5-10 phrasings + chain examples)
    for ~420 high-quality training examples covering every LazyOwn MCP tool.
    If LazyOwn is live, a random sample of tools are actually executed and their
    real output replaces the placeholder in the `answer` field.

    Returns the number of examples written.
    """
    # ── Load the rich generator ───────────────────────────────────────────────
    gen_mod = None
    for candidate in [_HERE / "lazyown_dataset_generator.py",
                      Path.cwd() / "lazyown_dataset_generator.py"]:
        if candidate.exists():
            import importlib.util as _ilu
            spec = _ilu.spec_from_file_location("lazyown_dataset_gen", candidate)
            gen_mod = _ilu.module_from_spec(spec)
            spec.loader.exec_module(gen_mod)
            break

    if gen_mod is None:
        # Fallback to built-in traces if generator not found
        print("[dataset] WARNING: lazyown_dataset_generator.py not found, "
              "falling back to built-in traces (35 examples).")
        records: List[Dict[str, Any]] = []
        for trace in _LAZYOWN_TRACES:
            records.append({
                "instruction": trace["instruction"],
                "api_list": [{"tool_name": trace["tool"],
                              "api_name": f"{trace['tool']}_endpoint",
                              "api_description": trace["tool"].replace("lazyown_", "").replace("_", " "),
                              "required_parameters": [{"name": "arg", "type": "STRING"}],
                              "optional_parameters": []}],
                "answer": f"[TOOL_CALL: {trace['tool']}({trace['arg']})] "
                          "[real output captured during actual pentest]",
                "domain": f"Security/{trace['domain']}",
            })
    else:
        records = gen_mod.build_dataset()

    # ── Optionally enrich answers with live LazyOwn output ───────────────────
    if bridge and bridge.available:
        import random as _rnd
        sample = _rnd.sample(range(len(records)), min(40, len(records)))
        enriched = 0
        for i in sample:
            r   = records[i]
            arg = r["api_list"][0].get("required_parameters", [{}])[0].get("description", "")
            # Extract arg from answer field: [TOOL_CALL: tool(arg)]
            m = re.search(r"\[TOOL_CALL:[^\(]+\(([^)]*)\)\]", r["answer"])
            cmd = m.group(1).strip() if m else ""
            if cmd:
                try:
                    raw = bridge.run(cmd, timeout=10)
                    if raw:
                        r["answer"] = re.sub(
                            r"\[real output[^\]]*\]", raw[:300], r["answer"]
                        )
                        enriched += 1
                except Exception:
                    pass
        if enriched:
            print(f"[dataset] Enriched {enriched} records with live LazyOwn output.")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"[dataset] Wrote {len(records)} LazyOwn examples → {output_path}")
    gen_mod and gen_mod.print_stats(records)
    return len(records)


# ===========================================================================
# Fine-tuning entry point
# ===========================================================================


def finetune_on_lazyown(dataset_path: Path, agent_cfg: SwarmConfig, logger: logging.Logger) -> None:
    """
    Fine-tune the TopoSwarm router on the full LazyOwn tool dataset using
    EWC + Experience Replay to prevent catastrophic forgetting.

    Pipeline (delegated to toposwarm_continual_trainer.py):
      1. Load the 420-example lazyown_full.jsonl.
      2. Compute / load Fisher Information diagonal on any available ToolBench
         data (anchors critical weights so general routing is preserved).
      3. Build a ToolBench replay buffer (20 % of every mini-batch).
      4. Fine-tune with combined loss: L_task + λ/2 · Σ F_i(θ_i − θ*_i)²
      5. Evaluate routing accuracy on held-out LazyOwn + ToolBench samples.
      6. Print final checkpoint stats (epoch, step, task_loss, ewc_lambda).
    """
    if not dataset_path.exists():
        logger.error("Dataset not found: %s — run --gen-dataset first", dataset_path)
        return

    logger.info("Fine-tuning with EWC+Replay on: %s", dataset_path)

    # ── Load the continual trainer ────────────────────────────────────────────
    ct_mod = None
    for candidate in [_HERE / "toposwarm_continual_trainer.py",
                      Path.cwd() / "toposwarm_continual_trainer.py"]:
        if candidate.exists():
            import importlib.util as _ilu
            spec   = _ilu.spec_from_file_location("toposwarm_continual_trainer", candidate)
            ct_mod = _ilu.module_from_spec(spec)
            sys.modules["toposwarm_continual_trainer"] = ct_mod  # must be before exec_module (dataclasses)
            spec.loader.exec_module(ct_mod)
            break

    if ct_mod is None:
        logger.error("toposwarm_continual_trainer.py not found — cannot use EWC+Replay")
        return

    try:
        cl_cfg = ct_mod.ContinualConfig(
            LAZYOWN_DATASET  = str(dataset_path),
            CHECKPOINT_DIR   = agent_cfg.CHECKPOINT_DIR,
            FISHER_PATH      = str(Path(agent_cfg.CHECKPOINT_DIR) / "fisher.pt"),
            EPOCHS           = 20,      # up to 20 epochs; early stopping (patience=5) guards overfit
            LEARNING_RATE    = 2e-5,    # 15× below original pre-training LR
            BATCH_SIZE       = 4,
            GRAD_ACCUM_STEPS = 4,
            LOG_INTERVAL     = 10,
            EVAL_INTERVAL    = 50,
            EWC_LAMBDA       = 10.0,    # reduced from 400 — high lambda was freezing weights
            REPLAY_RATIO     = 0.20,    # 20 % of each batch from ToolBench replay
        )
        ct_logger = ct_mod._setup_logger(cl_cfg.LOG_LEVEL)
        ct_mod.run_full_pipeline(cl_cfg, ct_logger)

        # ── Final checkpoint report ───────────────────────────────────────────
        meta_path = Path(agent_cfg.CHECKPOINT_DIR) / "latest" / "meta.json"
        if meta_path.exists():
            import json as _json
            meta = _json.loads(meta_path.read_text())
            logger.info(
                "Final checkpoint — epoch=%s step=%s task_loss=%s ewc_lambda=%s",
                meta.get("epoch", "?"),
                meta.get("step", "?"),
                f"{float(meta['task_loss']):.4f}" if "task_loss" in meta else "?",
                meta.get("ewc_lambda", "?"),
            )
        else:
            logger.warning("meta.json not found — checkpoint may not have been saved")

    except Exception as exc:
        logger.error("Continual fine-tuning failed: %s", exc, exc_info=True)


# ===========================================================================
# MCP server mode
# ===========================================================================


def run_mcp_server(orchestrator: LazyOwnOrchestrator) -> None:
    """
    Expose the TopoSwarm→LazyOwn orchestrator as an MCP stdio server.

    Tools exposed:
      toposwarm_query   — NL prompt → routed LazyOwn tool → answer
      lazyown_*         — direct passthrough to every registered tool
    """
    try:
        from mcp.server import Server
        from mcp.server.stdio import stdio_server
        from mcp import types
        import asyncio
    except ImportError:
        print(
            "[MCP] mcp package not installed. Install with: pip install mcp",
            file=sys.stderr,
        )
        sys.exit(1)

    server = Server("toposwarm-lazyown")

    @server.list_tools()
    async def list_tools() -> list:
        tools = [
            types.Tool(
                name="toposwarm_query",
                description=(
                    "Route a natural-language pentesting prompt through the TopoSwarm AI router "
                    "and execute the matched LazyOwn tool automatically."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "prompt": {"type": "string", "description": "Natural language pentesting goal"},
                    },
                    "required": ["prompt"],
                },
            )
        ]
        # Expose each registered tool directly
        for name in sorted(orchestrator.registry._tools):
            if name.startswith("lazyown"):
                tools.append(types.Tool(
                    name=name,
                    description=f"LazyOwn tool: {name.replace('lazyown_', '').replace('_', ' ')}",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "arg": {"type": "string", "description": "Argument for the tool"},
                        },
                        "required": [],
                    },
                ))
        return tools

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list:
        if name == "toposwarm_query":
            prompt = arguments.get("prompt", "")
            result = orchestrator.run(prompt)
            return [types.TextContent(type="text", text=result.final_answer)]

        arg = arguments.get("arg", "")
        tool_result = orchestrator.registry.execute(name, arg)
        return [types.TextContent(type="text", text=tool_result.output)]

    async def _serve():
        async with stdio_server() as streams:
            await server.run(streams[0], streams[1], server.create_initialization_options())

    asyncio.run(_serve())


# ===========================================================================
# Logging
# ===========================================================================


def _setup_logger(level: str = "INFO") -> logging.Logger:
    logger = logging.getLogger("TopoSwarmLazyOwn")
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    if not logger.handlers:
        h = logging.StreamHandler(sys.stdout)
        h.setFormatter(logging.Formatter(
            "%(asctime)s %(name)-24s %(levelname)-8s %(message)s"
        ))
        logger.addHandler(h)
    return logger


# ===========================================================================
# CLI entry point
# ===========================================================================


def main() -> None:
    parser = argparse.ArgumentParser(
        description="TopoSwarm orchestrator for LazyOwn MCP — routes NL prompts to pentesting tools"
    )
    parser.add_argument("--prompt",      type=str, default="",
                        help="Natural language pentesting prompt")
    parser.add_argument("--mcp",         action="store_true",
                        help="Run as MCP stdio server")
    parser.add_argument("--gen-dataset", action="store_true",
                        help="Generate LazyOwn fine-tuning JSONL and exit")
    parser.add_argument("--finetune",    action="store_true",
                        help="Fine-tune the router on LazyOwn traces (1 epoch)")
    parser.add_argument("--dataset-out", type=str,
                        default="data_toolbench/lazyown_full.jsonl",
                        help="Path for generated dataset JSONL")
    parser.add_argument("--lazyown-dir", type=str, default="",
                        help="Override path to LazyOwn repo root")
    parser.add_argument("--checkpoint",  type=str, default="checkpoints_toposwarm",
                        help="TopoSwarm checkpoint directory")
    parser.add_argument("--no-model",    action="store_true",
                        help="Skip model loading (routing only)")
    parser.add_argument("--device",      type=str, default="",
                        help="Force cpu or cuda")
    parser.add_argument("--list-tools",  action="store_true",
                        help="List all registered LazyOwn tools and exit")
    parser.add_argument("--log-level",   type=str, default="INFO")
    args = parser.parse_args()

    logger = _setup_logger(args.log_level)

    lazyown_dir = Path(args.lazyown_dir).expanduser().resolve() if args.lazyown_dir else _LAZYOWN_DIR
    bridge      = LazyOwnBridge(lazyown_dir)
    logger.info("LazyOwn dir: %s (available=%s)", bridge.lazyown_dir, bridge.available)

    dataset_path = Path(args.dataset_out)

    # ── Dataset generation ────────────────────────────────────────────────
    if args.gen_dataset:
        generate_dataset(dataset_path, bridge if bridge.available else None)
        return

    # ── Tool listing ──────────────────────────────────────────────────────
    if args.list_tools:
        cfg_tmp  = InferenceConfig()
        reg_tmp  = LazyOwnToolRegistry(cfg_tmp, bridge)
        print("Registered LazyOwn tools:")
        for name in sorted(reg_tmp._tools):
            print(f"  {name}")
        return

    # ── Build configs ─────────────────────────────────────────────────────
    cfg       = InferenceConfig(CHECKPOINT_DIR=args.checkpoint)
    agent_cfg = SwarmConfig()
    agent_cfg.CHECKPOINT_DIR = args.checkpoint
    if args.device:
        agent_cfg.DEVICE = args.device

    # ── Fine-tuning ───────────────────────────────────────────────────────
    if args.finetune:
        if not dataset_path.exists():
            logger.info("Dataset missing — generating %s first…", dataset_path)
            generate_dataset(dataset_path, bridge if bridge.available else None)
        n_examples = sum(1 for _ in dataset_path.open())
        logger.info("Dataset: %d examples in %s", n_examples, dataset_path)
        finetune_on_lazyown(dataset_path, agent_cfg, logger)
        return

    # ── Build orchestrator ────────────────────────────────────────────────
    load_model = not args.no_model and not args.mcp
    orchestrator = LazyOwnOrchestrator(
        cfg, agent_cfg, bridge, logger, load_model=load_model
    )

    # ── MCP server ────────────────────────────────────────────────────────
    if args.mcp:
        logger.info("Starting MCP stdio server…")
        run_mcp_server(orchestrator)
        return

    # ── Single prompt ─────────────────────────────────────────────────────
    prompt = args.prompt or "List all available LazyOwn modules"
    result = orchestrator.run(prompt)
    print(result.pretty() if hasattr(result, "pretty") else result.final_answer)


if __name__ == "__main__":
    main()
