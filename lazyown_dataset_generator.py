#!/usr/bin/env python3
"""
LazyOwn Dataset Generator for TopoSwarm Continual Learning
===========================================================
Generates a rich ToolBench-format JSONL covering all 79 LazyOwn MCP tools.

Each tool gets 5-10 diverse phrasings across skill levels, languages, and
contexts. Chain examples model realistic multi-step operator workflows.
Disambiguation examples teach the router when NOT to call a tool.

Output format (ToolBench JSONL):
    {
        "instruction": "<natural-language prompt>",
        "api_list": [{
            "tool_name": "<lazyown_tool>",
            "api_name": "<lazyown_tool>_endpoint",
            "api_description": "<short description>",
            "required_parameters": [...],
            "optional_parameters": []
        }],
        "answer": "[TOOL_CALL: <lazyown_tool>(<arg>)] <result_placeholder>",
        "domain": "Security/<category>"
    }

Usage
-----
    python lazyown_dataset_generator.py
    python lazyown_dataset_generator.py --out data_toolbench/lazyown_full.jsonl
    python lazyown_dataset_generator.py --stats
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Dict, List, Tuple

random.seed(42)

# ---------------------------------------------------------------------------
# Tool catalogue  (name, short_description, category, example_arg)
# ---------------------------------------------------------------------------

_TOOLS: List[Tuple[str, str, str, str]] = [
    # ── Core execution ───────────────────────────────────────────────────────
    ("lazyown_run_command",      "Execute LazyOwn shell commands non-interactively via PTY",
     "Execution", "lazynmap"),
    ("lazyown_discover_commands","List commands available for a pentest phase",
     "Execution", "recon"),
    ("lazyown_command_help",     "Full documentation for a specific LazyOwn command",
     "Execution", "lazynmap"),
    ("lazyown_phase_guide",      "Complete operator guide for a pentest phase",
     "Execution", "recon"),
    ("lazyown_bridge_suggest",   "Best command for given phase/service/objective (347 commands)",
     "Execution", "recon smb lateral"),

    # ── Configuration ────────────────────────────────────────────────────────
    ("lazyown_get_config",       "Read current payload.json configuration",
     "Config", ""),
    ("lazyown_set_config",       "Set a key-value pair in payload.json",
     "Config", "rhost=10.10.11.78"),
    ("lazyown_auto_populate",    "Parse nmap XML and auto-fill payload.json fields",
     "Config", ""),
    ("lazyown_session_init",     "SITREP — full situation report at session start",
     "Config", ""),
    ("lazyown_session_state",    "Return aggregated current session state",
     "Config", ""),

    # ── Targets ──────────────────────────────────────────────────────────────
    ("lazyown_add_target",       "Add or update a target in payload.json targets list",
     "Targets", "10.10.11.78"),
    ("lazyown_list_targets",     "List all tracked targets with ports and status",
     "Targets", ""),
    ("lazyown_set_active_target","Set active target — updates rhost/domain in payload.json",
     "Targets", "10.10.11.78"),

    # ── C2 / Sessions ────────────────────────────────────────────────────────
    ("lazyown_get_beacons",      "Query C2 server for connected beacons/implants",
     "C2", ""),
    ("lazyown_c2_command",       "Issue a tasking command to a beacon",
     "C2", "whoami"),
    ("lazyown_c2_status",        "Check if C2 server is reachable and return dashboard",
     "C2", ""),
    ("lazyown_run_api",          "Execute a shell command on C2 host via REST API",
     "C2", "id"),
    ("lazyown_list_sessions",    "List files in LazyOwn sessions directory",
     "C2", ""),
    ("lazyown_read_session_file","Read contents of a session file",
     "C2", "credentials.txt"),
    ("lazyown_c2_profile",       "Show, set or list malleable C2 profiles",
     "C2", "list"),

    # ── Modules / plugins ────────────────────────────────────────────────────
    ("lazyown_list_modules",     "List all modules and scripts in modules/",
     "Modules", ""),
    ("lazyown_list_addons",      "List YAML addons with name, status, description, repo",
     "Modules", ""),
    ("lazyown_list_plugins",     "List Lua plugins with name, status, description",
     "Modules", ""),
    ("lazyown_create_addon",     "Create a YAML addon to integrate any GitHub tool",
     "Modules", "https://github.com/user/tool.git"),

    # ── Intelligence / research ──────────────────────────────────────────────
    ("lazyown_c2_search_agent",  "Delegate research query to Groq AI search agent",
     "Intel", "SMB exploitation techniques"),
    ("lazyown_recommend_next",   "AI recommendation for next 3-5 commands (Groq)",
     "Intel", ""),
    ("lazyown_c2_vuln_analysis", "AI vulnerability/CVE analysis (Groq + C2)",
     "Intel", "CVE-2021-42278"),
    ("lazyown_c2_redop",         "AI red team operation planner (Groq)",
     "Intel", "full compromise 10.10.11.78"),
    ("lazyown_c2_adversary",     "MITRE ATT&CK adversary emulation (Groq)",
     "Intel", "APT29"),
    ("lazyown_c2_script",        "AI exploit/pentest script generator (Groq)",
     "Intel", "SMB relay attack"),
    ("lazyown_threat_model",     "Build MITRE ATT&CK threat model from session data",
     "Intel", ""),
    ("lazyown_playbook_generate","Generate MITRE ATT&CK grounded playbook for target",
     "Intel", "10.10.11.78"),
    ("lazyown_playbook_run",     "Execute a generated playbook against target",
     "Intel", "playbook_10.10.11.78.yaml"),
    ("lazyown_cve_search",       "Search NVD database for CVEs by product/version",
     "Intel", "apache 2.4.49"),
    ("lazyown_searchsploit",     "Multi-source exploit search (MSF, ExploitDB, NVD…)",
     "Intel", "vsftpd 2.3.4"),
    ("lazyown_llm_ask",          "Ask Groq/deepseek-r1 to reason about a goal with tools",
     "Intel", "how to escalate privileges on Linux"),

    # ── Memory / RAG ─────────────────────────────────────────────────────────
    ("lazyown_rag_index",        "Incrementally index sessions/ into ChromaDB",
     "Memory", ""),
    ("lazyown_rag_query",        "Semantic search over indexed session artefacts",
     "Memory", "SMB credentials found"),
    ("lazyown_memory_recall",    "Query episodic memory for past command executions",
     "Memory", "nmap scan results"),
    ("lazyown_memory_store",     "Explicitly save a command execution to episodic memory",
     "Memory", "nmap -sV 10.10.11.78"),

    # ── Reporting / campaign ─────────────────────────────────────────────────
    ("lazyown_campaign_sitrep",  "Master campaign SITREP — all state files in one call",
     "Report", ""),
    ("lazyown_c2_notes",         "Read/append/clear operational notes",
     "Report", "Found SMB signing disabled"),
    ("lazyown_credentials",      "Aggregate ALL captured credentials from every source",
     "Report", ""),
    ("lazyown_report_update",    "Read or update PDF/HTML pentest report data",
     "Report", "Found RCE via CVE-2021-42278"),
    ("lazyown_campaign_lessons", "Read tactical lessons from completed objectives",
     "Report", ""),
    ("lazyown_timeline",         "AI-written red-team timeline narrative (Groq)",
     "Report", ""),
    ("lazyown_generate_report",  "Auto-generate Markdown pentest report from session artefacts",
     "Report", ""),
    ("lazyown_misp_export",      "Export findings as MISP-compatible event JSON",
     "Report", ""),
    ("lazyown_eval_quality",     "LLM decision quality report: success rate, MITRE tactics",
     "Report", ""),
    ("lazyown_collab_publish",   "Broadcast findings to all operators via SSE",
     "Report", "Found domain admin credentials"),

    # ── Events / policy ──────────────────────────────────────────────────────
    ("lazyown_poll_events",      "Read events from LazyOwn Event Engine",
     "Events", ""),
    ("lazyown_ack_event",        "Mark event as processed",
     "Events", "evt_001"),
    ("lazyown_add_rule",         "Add/update an event detection rule",
     "Events", "pattern=RCE event_type=critical"),
    ("lazyown_list_event_rules", "List all active event detection rules",
     "Events", ""),
    ("lazyown_heartbeat_status", "Check if LazyOwn Heartbeat process is running",
     "Events", ""),
    ("lazyown_policy_status",    "Policy engine episode summary and next-action rewards",
     "Events", ""),

    # ── Automation ───────────────────────────────────────────────────────────
    ("lazyown_auto_loop",        "Autonomous attack loop guided by policy engine",
     "Automation", "10.10.11.78"),
    ("lazyown_session_init",     "Init session and return SITREP",
     "Automation", ""),
    ("lazyown_inject_objective", "Inject new attack objective into queue",
     "Automation", "achieve domain admin"),
    ("lazyown_next_objective",   "Return full frontier-model context for next action",
     "Automation", ""),
    ("lazyown_read_prompt",      "Read LazyOwn developer reference (prompt.md)",
     "Automation", ""),
    ("lazyown_soul",             "Read or update agent soul (campaign objective/priority)",
     "Automation", ""),

    # ── Agents ───────────────────────────────────────────────────────────────
    ("lazyown_run_agent",        "Delegate goal to autonomous Groq/Ollama sub-agent",
     "Agents", "enumerate AD on 10.10.11.78"),
    ("lazyown_agent_status",     "Check running sub-agent status and progress",
     "Agents", "agent_001"),
    ("lazyown_agent_result",     "Read full result of a completed sub-agent",
     "Agents", "agent_001"),
    ("lazyown_list_agents",      "List recent sub-agents with status and goal",
     "Agents", ""),
    ("lazyown_groq_agent",       "Spawn Groq/Ollama agent pre-loaded with 21 LazyOwn tools",
     "Agents", "perform recon on 10.10.11.78"),

    # ── Hive mind ────────────────────────────────────────────────────────────
    ("lazyown_hive_spawn",       "Spawn parallel Groq/Ollama drones for a goal",
     "Hive", "enumerate SMB shares on 10.10.11.78"),
    ("lazyown_hive_status",      "Full hive-mind status: drones, ChromaDB, memory",
     "Hive", ""),
    ("lazyown_hive_recall",      "Semantic search over all drone results and sessions",
     "Hive", "domain admin credentials"),
    ("lazyown_hive_plan",        "Decompose goal into drone tasks WITHOUT spawning",
     "Hive", "full domain compromise"),
    ("lazyown_hive_result",      "Get result of a specific hive drone",
     "Hive", "drone_001"),
    ("lazyown_hive_collect",     "Wait for drones and return synthesized summary",
     "Hive", "drone_001,drone_002"),
    ("lazyown_hive_forget",      "Prune hive episodic memory by age or topic",
     "Hive", "24"),
    ("lazyown_hive_recover",     "Re-queue interrupted hive drones after crash",
     "Hive", ""),

    # ── Autonomous daemon ────────────────────────────────────────────────────
    ("lazyown_autonomous_start", "Start autonomous daemon — executes objectives without Claude",
     "Autonomous", "achieve domain admin on 10.10.11.78"),
    ("lazyown_autonomous_stop",  "Stop the autonomous daemon",
     "Autonomous", ""),
    ("lazyown_autonomous_status","Real-time daemon status: phase, objective, steps, drones",
     "Autonomous", ""),
    ("lazyown_autonomous_inject","Inject new objective into autonomous daemon queue",
     "Autonomous", "exfiltrate /etc/passwd"),
    ("lazyown_autonomous_events","Read last N events from autonomous event stream",
     "Autonomous", "20"),

    # ── Tools / objectives ───────────────────────────────────────────────────
    ("lazyown_create_tool",      "Create pwntomate .tool file for automatic service matching",
     "Tools", "vsftpd 2.3.4 exploit"),
]

# Remove duplicate session_init (appears twice in original list)
seen = set()
_TOOLS_DEDUP: List[Tuple[str, str, str, str]] = []
for t in _TOOLS:
    if t[0] not in seen:
        _TOOLS_DEDUP.append(t)
        seen.add(t[0])
_TOOLS = _TOOLS_DEDUP


# ---------------------------------------------------------------------------
# Per-tool phrasings  (instruction templates, {arg} is replaced if present)
# ---------------------------------------------------------------------------

_PHRASINGS: Dict[str, List[Tuple[str, str]]] = {

    # ── Core execution ───────────────────────────────────────────────────────
    "lazyown_run_command": [
        # direct command
        ("Run the lazynmap command against the target",                   "lazynmap"),
        ("Execute 'set rhost 10.10.11.78' then lazynmap",                 "set rhost 10.10.11.78\nlazynmap"),
        ("Run lazyown command: gobuster on the web server",               "set rhost 10.10.11.78\nlazygobuster"),
        ("Ejecuta el escaneo nmap en el objetivo",                        "lazynmap"),
        ("I need to run lazywebscan on the target",                       "lazywebscan"),
        ("Execute enum4linux against 10.10.11.78",                        "set rhost 10.10.11.78\nlazyenum4linux"),
        ("Run the SMB enumeration module",                                "lazysmbscan"),
        ("Use lazyown to run a full port scan",                           "lazynmap"),
        ("Run lazybrute to brute force SSH",                              "lazybrute"),
        ("Ejecuta lazymetasploit para buscar exploits",                   "lazymsf"),
        # question form
        ("How do I run a port scan with LazyOwn?",                        "lazynmap"),
        ("What command scans the target for open ports?",                 "lazynmap"),
        ("How can I enumerate web directories on the target?",            "lazygobuster"),
        # contextual / scenario
        ("Box is up on HTB, time to port scan",                           "lazynmap"),
        ("Just added the target, need to enumerate services",             "lazynmap"),
        ("I found port 80 open, enumerate the web server now",           "lazywebscan"),
        ("After setting rhost, run the full scan suite",                  "lazynmap"),
        ("Target is a Windows box, run SMB enumeration",                  "lazysmbscan"),
        # casual / shorthand
        ("nmap the box",                                                  "lazynmap"),
        ("quick scan target",                                             "lazynmap"),
        ("gobuster it",                                                   "lazygobuster"),
        ("smb enum",                                                      "lazysmbscan"),
        ("brute force ssh on the target",                                 "lazybrute"),
        # expert / CTF
        ("service detection + OS fingerprint on scope host",              "lazynmap"),
        ("full TCP scan then web fuzzing pipeline",                       "lazynmap"),
        ("run enum4linux against the domain controller",                  "lazyenum4linux"),
        # beginner
        ("I need to find what services are running on the target",        "lazynmap"),
        ("Help me see which ports are open",                              "lazynmap"),
    ],
    "lazyown_discover_commands": [
        ("What LazyOwn commands are available for recon?",                "recon"),
        ("Show me all enumeration commands",                              "enum"),
        ("Discover exploit commands for the exploitation phase",          "exploit"),
        ("List available post-exploitation commands",                     "post"),
        ("¿Qué comandos de LazyOwn hay para escalada de privilegios?",    "privesc"),
        ("Show lateral movement commands",                                "lateral"),
        ("What commands help with credential dumping?",                   "creds"),
        ("List all available LazyOwn commands",                           ""),
        ("Which commands does LazyOwn have for AD attacks?",              "lateral"),
        ("Show tools available for web exploitation",                     "exploit"),
        ("¿Qué herramientas hay para post-explotación?",                 "post"),
        ("I want to see all commands grouped by phase",                   ""),
        ("What can LazyOwn do for persistence?",                          "post"),
        ("List exfiltration commands",                                    "post"),
        ("Commands for active directory enumeration?",                    "enum"),
    ],
    "lazyown_command_help": [
        ("How do I use the lazynmap command?",                            "lazynmap"),
        ("Get help for lazygobuster",                                     "lazygobuster"),
        ("What parameters does lazybrute accept?",                        "lazybrute"),
        ("Explain the lazymsf command",                                   "lazymsf"),
        ("Show documentation for lazywebscan",                            "lazywebscan"),
        ("How does the bloodhound command work in lazyown?",              "lazybloodhound"),
        ("What arguments does lazysmb take?",                             "lazysmbscan"),
        ("Explain how lazywpscan works",                                  "lazywpscan"),
        ("How to use lazyenum4linux?",                                    "lazyenum4linux"),
        ("Show me the help for lazyburp",                                 "lazyburp"),
        ("What does lazysniff do?",                                       "lazysniff"),
        ("Usage for lazyreverse command",                                 "lazyreverse"),
        ("Explain lazykerberoast",                                        "lazykerberoast"),
    ],
    "lazyown_phase_guide": [
        ("Guide me through the reconnaissance phase",                     "recon"),
        ("Full operator guide for enumeration",                           "enum"),
        ("How should I approach exploitation?",                           "exploit"),
        ("Post-exploitation phase guide",                                 "post"),
        ("Guía completa para la fase de escalada de privilegios",         "privesc"),
        ("What is the complete workflow for lateral movement?",           "lateral"),
        ("Walk me through credential attacks step by step",               "creds"),
        ("I'm new to HTB, explain the recon phase",                       "recon"),
        ("What do I do first when I start a pentest?",                    "recon"),
        ("Methodology for initial access phase",                          "exploit"),
        ("How to do privilege escalation step by step?",                  "privesc"),
        ("Guide for Active Directory attacks",                            "lateral"),
        ("Pasos para comprometer un dominio de AD",                       "lateral"),
        ("Full kill chain methodology guide",                             "recon"),
        ("What order should I follow: recon, enum, exploit?",             "recon"),
    ],
    "lazyown_bridge_suggest": [
        ("Suggest the best command for SMB enumeration in the recon phase", "recon smb enum"),
        ("What command should I run for privilege escalation on Linux?",    "privesc linux"),
        ("Best command to exploit a web app after finding SQL injection",   "exploit web sqli"),
        ("Recommend a command for lateral movement using captured creds",   "lateral creds"),
        ("Which LazyOwn command handles Kerberoasting?",                    "exploit kerberoasting"),
        ("Best tool for AD enumeration with valid credentials",             "enum ad creds"),
        ("What should I use to test for SMB relay?",                        "exploit smb relay"),
        ("Recommend a command for web directory fuzzing",                   "recon web fuzz"),
        ("Best command for LDAP enumeration on the DC",                     "enum ldap ad"),
        ("Which command dumps credentials from LSASS?",                     "post cred dump"),
        ("What tool does lateral movement via WMI?",                        "lateral wmi"),
        ("Best command for AS-REP roasting?",                               "exploit asrep"),
        ("Suggest a command to find writable SMB shares",                   "recon smb shares"),
        ("What LazyOwn command handles DCSync?",                            "exploit dcsync"),
        ("Recommend tool for web vulnerability scanning",                   "recon web vuln"),
    ],

    # ── Configuration ────────────────────────────────────────────────────────
    "lazyown_get_config": [
        ("Show the current LazyOwn configuration",                        ""),
        ("What is the current payload.json?",                             ""),
        ("Read the LazyOwn settings",                                     ""),
        ("Get current rhost and lhost values",                            ""),
        ("¿Cuál es la configuración actual?",                             ""),
        ("Display all LazyOwn parameters",                                ""),
        ("What is the current target configuration?",                     ""),
        ("Print current payload configuration",                           ""),
        ("Show me what rhost is set to",                                  ""),
        ("What's currently configured in LazyOwn?",                       ""),
        ("Check the current lhost and lport settings",                    ""),
        ("Muéstrame la configuración actual de LazyOwn",                  ""),
        ("What domain is configured?",                                    ""),
        ("Read payload.json",                                             ""),
        ("Show all variables: rhost, lhost, port, user, password",        ""),
    ],
    "lazyown_set_config": [
        ("Set the target host to 10.10.11.78",                            "rhost=10.10.11.78"),
        ("Configure lhost to 10.10.14.2",                                 "lhost=10.10.14.2"),
        ("Set the listening port to 4444",                                "lport=4444"),
        ("Update the domain to corp.local",                               "domain=corp.local"),
        ("Set rport to 445",                                              "rport=445"),
        ("Configure the wordlist path",                                   "wordlist=/usr/share/wordlists/rockyou.txt"),
        ("Establece el host objetivo en 192.168.1.100",                   "rhost=192.168.1.100"),
        ("Set the username to administrator",                             "user=administrator"),
        ("Set the password to Password123",                               "passw=Password123"),
        ("Configure the attack platform as windows",                      "os_id=windows"),
        ("Update rhost to the new target IP",                             "rhost=10.10.11.200"),
        ("Change the listener port to 9001",                              "lport=9001"),
        ("Set target to 10.10.10.5",                                      "rhost=10.10.10.5"),
        ("Configura el puerto de escucha en 443",                         "lport=443"),
        ("Set user to root and passw to toor",                            "user=root"),
        ("Update the callback IP to my VPN address",                      "lhost=10.10.14.5"),
        ("Set domain to htb.local",                                       "domain=htb.local"),
        ("Change the wordlist to seclist passwords",                      "wordlist=/usr/share/seclists/Passwords/Common-Credentials/10k-most-common.txt"),
        ("Configure OS to linux",                                         "os_id=linux"),
        ("rhost 10.10.11.78",                                             "rhost=10.10.11.78"),
    ],
    "lazyown_auto_populate": [
        ("Auto-populate the configuration from the nmap scan",            ""),
        ("Parse nmap XML and fill payload.json automatically",            ""),
        ("Extract services from nmap and configure LazyOwn",              ""),
        ("Auto-fill domain and OS from the scan results",                 ""),
        ("Rellena automáticamente la configuración desde el escaneo",     ""),
        ("Parse the scan results and update config",                      ""),
        ("Automatically configure LazyOwn from nmap XML output",         ""),
        ("Fill in rhost, ports, and OS from the scan",                    ""),
        ("After nmap scan, auto-configure the payload",                   ""),
        ("Detect OS and services from nmap and set config",               ""),
        ("Auto-detect target OS and open ports",                          ""),
        ("Let LazyOwn read the nmap output and configure itself",         ""),
    ],
    "lazyown_session_init": [
        ("Initialize the session and give me a sitrep",                   ""),
        ("Start a new session and show current status",                   ""),
        ("SITREP — what is the current state of the engagement?",        ""),
        ("Init session for target 10.10.11.78",                          ""),
        ("¿Cuál es el estado actual del engagement?",                    ""),
        ("Session start — give me the situation report",                  ""),
        ("What has been discovered so far?",                              ""),
        ("Load session context before starting work",                     ""),
        ("Show me the full situation report",                             ""),
        ("Initialize engagement session and brief me",                    ""),
        ("Morning brief — what is the engagement status?",                ""),
        ("Start the session and give me a full situational overview",     ""),
        ("Beginning shift handover — show me everything discovered",      ""),
        ("Dame el reporte de situación actual",                           ""),
        ("Begin session and show current state of all targets",           ""),
    ],
    "lazyown_session_state": [
        ("What is the current session state?",                            ""),
        ("Show active phase and discovered hosts",                        ""),
        ("Give me the aggregated session context",                        ""),
        ("What ports and creds have been found so far?",                  ""),
        ("Estado actual de la sesión",                                    ""),
        ("Current phase and next objectives?",                            ""),
        ("What stage of the engagement are we in?",                       ""),
        ("Show me everything the session knows right now",                ""),
        ("Session context: hosts, creds, phase",                          ""),
        ("What is the current operational context?",                      ""),
        ("Give me the session snapshot",                                  ""),
    ],

    # ── Targets ──────────────────────────────────────────────────────────────
    "lazyown_add_target": [
        ("Add 10.10.11.78 as a target",                                   "10.10.11.78"),
        ("Register 192.168.1.100 in the target list",                     "192.168.1.100"),
        ("New target: 172.16.0.5 port 445 SMB",                          "172.16.0.5"),
        ("Add domain controller 10.10.11.1 to scope",                    "10.10.11.1"),
        ("Añade 10.10.10.5 a los objetivos",                              "10.10.10.5"),
        ("Track host 10.10.11.78 with tag web",                           "10.10.11.78"),
        ("Add 10.10.11.78 with status active",                            "10.10.11.78"),
        ("Put 192.168.1.50 in my target list",                            "192.168.1.50"),
        ("Track the domain controller at 10.10.11.1",                     "10.10.11.1"),
        ("Add the web server 10.10.11.100 to targets",                    "10.10.11.100"),
        ("Scope in 10.10.11.78",                                          "10.10.11.78"),
        ("New box found: add 172.16.0.10 to target tracking",             "172.16.0.10"),
        ("Register the newly discovered host",                            "10.10.11.78"),
        ("Agrega el servidor web como objetivo",                          "10.10.11.78"),
    ],
    "lazyown_list_targets": [
        ("List all targets in scope",                                     ""),
        ("Show tracked targets with their ports",                         ""),
        ("What hosts are in our target list?",                            ""),
        ("Display all registered targets",                                ""),
        ("¿Qué objetivos tenemos en el scope?",                           ""),
        ("Show all targets and their discovery status",                   ""),
        ("What machines are we tracking?",                                ""),
        ("Give me the full target inventory",                             ""),
        ("Which hosts have we added to scope?",                           ""),
        ("List all IPs in the engagement scope",                          ""),
        ("Show targets with open ports discovered",                       ""),
        ("Muéstrame todos los objetivos registrados",                     ""),
    ],
    "lazyown_set_active_target": [
        ("Set 10.10.11.78 as the active target",                          "10.10.11.78"),
        ("Switch focus to 192.168.1.100",                                 "192.168.1.100"),
        ("Make 10.10.11.1 the current target",                            "10.10.11.1"),
        ("Activate target 10.10.11.78",                                   "10.10.11.78"),
        ("Cambia al objetivo 10.10.10.5",                                 "10.10.10.5"),
        ("Focus on the domain controller now",                            "10.10.11.1"),
        ("Switch to the web server target",                               "10.10.11.78"),
        ("Change the active target to the new box",                       "10.10.11.200"),
        ("Select 10.10.11.78 as the primary target",                      "10.10.11.78"),
        ("Now working on 192.168.1.50",                                   "192.168.1.50"),
        ("Make 10.10.11.1 my current rhost",                              "10.10.11.1"),
        ("I want to attack 10.10.11.78 now",                              "10.10.11.78"),
    ],

    # ── C2 / Sessions ────────────────────────────────────────────────────────
    "lazyown_get_beacons": [
        ("List all connected beacons",                                    ""),
        ("Show active implants on the C2",                                ""),
        ("What beacons are checking in?",                                 ""),
        ("Get connected agents from C2 server",                          ""),
        ("¿Qué implantes están activos?",                                 ""),
        ("Display beacon status",                                         ""),
        ("Which compromised hosts are calling back?",                     ""),
        ("Show me all the active C2 agents",                              ""),
        ("List implants currently connected",                             ""),
        ("How many beacons do we have?",                                  ""),
        ("C2 beacon inventory",                                           ""),
        ("Show connected shells and beacons",                             ""),
        ("¿Cuántos beacons están conectados?",                            ""),
        ("Which machines have an active C2 channel?",                     ""),
    ],
    "lazyown_c2_command": [
        ("Send whoami to all beacons",                                    "whoami"),
        ("Task the beacon to run ipconfig",                               "ipconfig"),
        ("Issue hostname command to connected implants",                  "hostname"),
        ("Run 'net user' on the compromised host via beacon",             "net user"),
        ("Tasking: execute 'cat /etc/passwd' on Linux beacon",           "cat /etc/passwd"),
        ("Send 'systeminfo' to Windows beacon",                           "systeminfo"),
        ("Task beacon to dump local user hashes",                         "hashdump"),
        ("Run id on the beacon",                                          "id"),
        ("Execute uname -a on compromised Linux host",                    "uname -a"),
        ("Run 'net group \"Domain Admins\"' via C2",                      "net group \"Domain Admins\" /domain"),
        ("Task all beacons to run ifconfig",                              "ifconfig"),
        ("Send dir command to Windows implant",                           "dir C:\\"),
        ("Mandar whoami a todos los implantes",                            "whoami"),
        ("Run ps aux on the Linux beacon",                                "ps aux"),
        ("Execute netstat on compromised host",                           "netstat -an"),
    ],
    "lazyown_c2_status": [
        ("Is the C2 server running?",                                     ""),
        ("Check C2 server health",                                        ""),
        ("C2 dashboard status",                                           ""),
        ("Is the command and control infrastructure up?",                 ""),
        ("¿Está funcionando el servidor C2?",                             ""),
        ("Ping the C2 server",                                            ""),
        ("Is the team server online?",                                    ""),
        ("Check if the C2 listener is active",                            ""),
        ("C2 health check",                                               ""),
        ("Is the command server reachable?",                              ""),
        ("Verify C2 connectivity",                                        ""),
        ("¿Está activo el servidor de comando y control?",                ""),
    ],
    "lazyown_run_api": [
        ("Run 'id' on the C2 host via REST API",                          "id"),
        ("Execute 'uname -a' through the C2 API",                        "uname -a"),
        ("Call the LazyOwn API to run a command",                        "whoami"),
        ("Use the REST API to check running processes",                   "ps aux"),
        ("Run a shell command via the LazyOwn REST API",                  "hostname"),
        ("API call to execute command on C2 host",                        "cat /etc/passwd"),
        ("HTTP API: run 'df -h' on server",                               "df -h"),
        ("REST call to check C2 host network config",                     "ip addr"),
        ("Execute via API: netstat -an",                                  "netstat -an"),
        ("Run curl command through LazyOwn API",                         "curl localhost:8080"),
    ],
    "lazyown_list_sessions": [
        ("List all session files",                                        ""),
        ("Show captured data in sessions/",                               ""),
        ("What files are in the sessions directory?",                     ""),
        ("List exfiltrated data and logs",                                ""),
        ("¿Qué hay en la carpeta sessions?",                              ""),
        ("Show me all session artefacts",                                 ""),
        ("List captured outputs in sessions folder",                      ""),
        ("What data has been collected in sessions/?",                    ""),
        ("Show session directory contents",                               ""),
        ("What logs and captures do we have?",                            ""),
        ("List session files from this engagement",                       ""),
    ],
    "lazyown_read_session_file": [
        ("Read the credentials.txt session file",                         "credentials.txt"),
        ("Show contents of nmap scan results",                            "scan_10.10.11.78.nmap"),
        ("Read the latest session log",                                   "session.log"),
        ("Open the captured hash file",                                   "hashes.txt"),
        ("Read the exfiltrated /etc/passwd",                              "etc_passwd.txt"),
        ("Show the contents of the loot file",                            "loot.txt"),
        ("Read the BloodHound output",                                    "bloodhound_output.json"),
        ("Open the Kerb ticket file",                                     "ticket.ccache"),
        ("Read the captured SAM database",                                "sam.txt"),
        ("Show me the web scan results file",                             "gobuster_10.10.11.78.txt"),
    ],
    "lazyown_c2_profile": [
        ("List available C2 profiles",                                    "list"),
        ("Show the current malleable C2 profile",                         "show"),
        ("Set C2 beacon sleep to 30 seconds",                             "set sleep=30"),
        ("Which C2 profiles are available?",                              "list"),
        ("Change beacon jitter to 20%",                                   "set jitter=20"),
        ("Show current beacon configuration",                             "show"),
        ("Select stealthy C2 profile",                                    "set profile=stealthy"),
        ("What malleable profiles are loaded?",                           "list"),
    ],

    # ── Modules / plugins ────────────────────────────────────────────────────
    "lazyown_list_modules": [
        ("List all LazyOwn modules",                                      ""),
        ("What scripts are available in modules/?",                       ""),
        ("Show available exploit modules",                                ""),
        ("¿Qué módulos tiene LazyOwn?",                                   ""),
        ("Display all LazyOwn tools and scripts",                        ""),
        ("What attack scripts are installed?",                            ""),
        ("Show all Python modules in LazyOwn",                            ""),
        ("List every script in the modules folder",                       ""),
        ("What auxiliary modules does LazyOwn have?",                     ""),
        ("Show LazyOwn module list",                                      ""),
        ("¿Cuántos módulos hay disponibles?",                             ""),
        ("I want to see all available LazyOwn modules",                   ""),
    ],
    "lazyown_list_addons": [
        ("List all installed addons",                                     ""),
        ("What addons are available in LazyOwn?",                        ""),
        ("Show enabled addons",                                           ""),
        ("¿Qué addons hay disponibles?",                                  ""),
        ("Show all YAML-defined addons",                                  ""),
        ("Which addons are currently enabled?",                           ""),
        ("List external tool integrations",                               ""),
        ("What third-party tools has LazyOwn integrated?",                ""),
        ("Show addon repository list",                                    ""),
        ("¿Qué herramientas externas están integradas?",                  ""),
    ],
    "lazyown_list_plugins": [
        ("List all Lua plugins",                                          ""),
        ("Show available LazyOwn plugins",                                ""),
        ("What Lua scripts are installed?",                               ""),
        ("¿Qué plugins están disponibles?",                               ""),
        ("Display all LazyOwn Lua extensions",                            ""),
        ("Which plugins are loaded?",                                     ""),
        ("Show plugin inventory",                                         ""),
        ("List available Lua automation scripts",                         ""),
        ("What custom plugins does LazyOwn have?",                        ""),
    ],
    "lazyown_create_addon": [
        ("Create a new addon for impacket from GitHub",                   "https://github.com/fortra/impacket.git"),
        ("Add a new addon for Certipy",                                   "https://github.com/ly4k/Certipy.git"),
        ("Create addon for Responder tool",                               "https://github.com/lgandx/Responder.git"),
        ("Integrate a new tool from GitHub into LazyOwn",                 "https://github.com/user/tool.git"),
        ("Install BloodHound as a LazyOwn addon",                         "https://github.com/BloodHoundAD/BloodHound.git"),
        ("Add ligolo-ng as a new addon",                                  "https://github.com/nicocha30/ligolo-ng.git"),
        ("Wrap this GitHub tool into a LazyOwn addon",                    "https://github.com/dirkjanm/mitm6.git"),
        ("Create addon for CrackMapExec",                                 "https://github.com/Porchetta-Industries/CrackMapExec.git"),
        ("Integrate hashcat as an addon",                                 "https://github.com/hashcat/hashcat.git"),
        ("Add new GitHub tool to LazyOwn tool catalog",                   "https://github.com/skelsec/pypykatz.git"),
    ],

    # ── Intelligence / research ──────────────────────────────────────────────
    "lazyown_c2_search_agent": [
        ("Search for SMB relay attack techniques",                        "SMB relay attack techniques"),
        ("Find MITRE techniques for credential dumping",                  "MITRE credential dumping"),
        ("Research Kerberoasting attack methodology",                     "Kerberoasting"),
        ("OSINT search for CVE-2021-42278",                               "CVE-2021-42278"),
        ("Busca técnicas de escalada de privilegios en Linux",            "Linux privilege escalation"),
        ("Find exploit for vsftpd 2.3.4",                                "vsftpd 2.3.4 exploit"),
        ("Research DCSync attack",                                        "DCSync Active Directory"),
        ("Search for pass-the-hash techniques",                           "pass the hash NTLM"),
        ("Look up BloodHound attack paths",                               "BloodHound attack paths"),
        ("Research golden ticket attack",                                 "golden ticket Kerberos"),
        ("Find info about AS-REP roasting",                               "AS-REP roasting"),
        ("Search for PrintNightmare exploit",                             "PrintNightmare CVE-2021-34527"),
        ("Research LLMNR poisoning methodology",                          "LLMNR NBT-NS poisoning"),
        ("Look up techniques for bypassing AV",                           "AV evasion techniques"),
        ("Busca información sobre ataques de relay NTLM",                 "NTLM relay attack"),
        ("Research how to exploit log4j remotely",                        "log4j RCE CVE-2021-44228"),
        ("Find persistence mechanisms for Windows",                       "Windows persistence techniques"),
        ("Search for lateral movement using WMI",                         "WMI lateral movement"),
    ],
    "lazyown_recommend_next": [
        ("What should be the next step?",                                 ""),
        ("Recommend the best next action",                                ""),
        ("What should I run after the nmap scan?",                        ""),
        ("Next recommended commands for this target",                     ""),
        ("¿Qué hago después del escaneo inicial?",                       ""),
        ("Suggest what to do after finding SMB signing disabled",         ""),
        ("What is the best next move after getting initial access?",      ""),
        ("Recommend next steps after privilege escalation",               ""),
        ("I got a shell, what should I do next?",                         ""),
        ("Found a web server, what do I enumerate next?",                 ""),
        ("Just completed recon phase, what's next?",                      ""),
        ("After finding port 445 open, what to do?",                      ""),
        ("Got domain user creds, recommend next step",                    ""),
        ("Tengo acceso inicial, ¿qué hago ahora?",                       ""),
        ("What's the highest priority action after this finding?",        ""),
        ("Suggest 3 actions based on current session state",              ""),
        ("AI: best move from current engagement state",                   ""),
    ],
    "lazyown_c2_vuln_analysis": [
        ("Analyze vulnerabilities on 10.10.11.78",                        "10.10.11.78"),
        ("What CVEs affect the services on this target?",                 "10.10.11.78"),
        ("Vulnerability analysis for Apache 2.4.49",                     "Apache 2.4.49"),
        ("Analyze CVE-2021-42278",                                        "CVE-2021-42278"),
        ("What exploits exist for SMBv1?",                                "SMBv1"),
        ("Análisis de vulnerabilidades del objetivo",                     "10.10.11.78"),
        ("Check if EternalBlue applies to the target",                    "MS17-010 EternalBlue"),
        ("Assess the attack surface on 10.10.11.78",                     "10.10.11.78"),
        ("Is this OpenSSH version vulnerable?",                           "OpenSSH 7.4"),
        ("Find exploits for the discovered services",                     "10.10.11.78"),
        ("Vuln scan the target and identify attack paths",                "10.10.11.78"),
        ("What weaknesses does this Windows version have?",               "Windows Server 2019"),
        ("Check for known CVEs on port 8080",                             "10.10.11.78:8080"),
        ("Analyze the Samba version for exploits",                        "Samba 4.13.2"),
        ("¿Qué CVEs afectan a esta versión de Apache?",                   "Apache 2.4.49"),
        ("Find attack vectors for the discovered services",               "10.10.11.78"),
    ],
    "lazyown_c2_redop": [
        ("Plan a full red team operation on 10.10.11.78",                 "full compromise 10.10.11.78"),
        ("Create a red team attack plan for the corp.local domain",       "corp.local domain takeover"),
        ("Plan lateral movement after initial access",                    "lateral movement post-access"),
        ("Design a full attack chain for Active Directory",               "AD full compromise"),
        ("Create operation plan: from recon to domain admin",             "recon to domain admin"),
        ("Build an OPSEC-safe attack plan",                               "OPSEC-safe domain compromise"),
        ("Plan multi-phase red team campaign",                            "multi-phase campaign 10.10.11.78"),
        ("Design covert persistent access strategy",                      "persistent covert access"),
        ("Create TTPs for full domain compromise",                        "domain compromise TTPs"),
        ("Plan the operation: initial access, privesc, lateral, exfil",   "full kill chain corp.local"),
        ("Red team operation plan: compromise DC silently",               "stealth DC compromise"),
    ],
    "lazyown_c2_adversary": [
        ("Emulate APT29 adversary techniques",                            "APT29"),
        ("Simulate Lazarus Group TTPs",                                   "Lazarus Group"),
        ("Run MITRE ATT&CK technique T1003 (credential dumping)",         "T1003"),
        ("Emulate ransomware operator TTPs",                              "ransomware operator"),
        ("Apply FIN7 adversary playbook",                                 "FIN7"),
        ("Simulate APT28 attack patterns",                                "APT28"),
        ("Run Cobalt Strike-style TTPs",                                  "Cobalt Strike TTPs"),
        ("Emulate nation-state actor techniques",                         "nation-state APT"),
        ("Apply MITRE ATT&CK T1078 (valid accounts) technique",          "T1078"),
        ("Simulate TA505 financial crime TTPs",                           "TA505"),
        ("Emulate human operators post-breach behavior",                  "post-breach operator"),
    ],
    "lazyown_c2_script": [
        ("Generate a SMB relay exploit script",                           "SMB relay attack"),
        ("Write a PowerShell privilege escalation script",                "PowerShell privesc"),
        ("Generate a Python reverse shell",                               "Python reverse shell"),
        ("Create a Kerberoasting script",                                 "Kerberoasting extraction"),
        ("Write a DCSync script using impacket",                          "DCSync impacket"),
        ("Generate a bash one-liner reverse shell",                       "bash reverse shell"),
        ("Write a Python script to enumerate SMB shares",                 "SMB share enumeration Python"),
        ("Create a PowerShell AMSI bypass script",                        "AMSI bypass PowerShell"),
        ("Generate a credential harvesting script for Windows",           "Windows credential harvesting"),
        ("Write an LDAP enumeration script",                              "LDAP enumeration script"),
        ("Create a BloodHound data collection script",                    "BloodHound collection"),
    ],
    "lazyown_threat_model": [
        ("Build a threat model for the current session",                  ""),
        ("Generate MITRE ATT&CK threat model",                           ""),
        ("Map discovered TTPs to MITRE framework",                        ""),
        ("Create threat model from session data",                         ""),
        ("¿Cuál es el modelo de amenazas del engagement?",               ""),
        ("Produce ATT&CK threat model based on findings",                 ""),
        ("Map our attack to the MITRE ATT&CK matrix",                    ""),
        ("Generate a threat intel report from session",                   ""),
        ("Build adversary profile from discovered TTPs",                  ""),
        ("What MITRE techniques have we used so far?",                    ""),
    ],
    "lazyown_playbook_generate": [
        ("Generate an attack playbook for 10.10.11.78",                   "10.10.11.78"),
        ("Create MITRE ATT&CK grounded playbook",                         "10.10.11.78"),
        ("Build playbook for domain compromise",                          "corp.local"),
        ("Generate pentest playbook for target",                          "10.10.11.78"),
        ("Create step-by-step attack playbook",                           "10.10.11.78"),
        ("Generate operator playbook for this engagement",                "10.10.11.78"),
        ("Build YAML playbook for AD compromise",                         "corp.local"),
        ("Create structured attack plan as playbook",                     "10.10.11.78"),
        ("Generate automated attack playbook",                            "10.10.11.78"),
    ],
    "lazyown_playbook_run": [
        ("Execute the generated playbook",                                "playbook_10.10.11.78.yaml"),
        ("Run the attack playbook step by step",                          "playbook_corp.local.yaml"),
        ("Start playbook execution",                                      "playbook.yaml"),
        ("Run the generated pentest playbook",                            "playbook_10.10.11.78.yaml"),
        ("Execute playbook against the target",                           "playbook.yaml"),
        ("Start automated playbook on 10.10.11.78",                       "playbook_10.10.11.78.yaml"),
        ("Run the AD compromise playbook",                                "playbook_corp.local.yaml"),
    ],
    "lazyown_cve_search": [
        ("Search CVEs for Apache 2.4.49",                                 "apache 2.4.49"),
        ("Find vulnerabilities in OpenSSH 7.4",                          "openssh 7.4"),
        ("CVE lookup for vsftpd 2.3.4",                                   "vsftpd 2.3.4"),
        ("What CVEs affect Samba 4.13?",                                  "samba 4.13"),
        ("Search NVD for Windows 10 vulnerabilities",                     "windows 10"),
        ("Busca CVEs para log4j 2.14",                                    "log4j 2.14"),
        ("NVD lookup: IIS 6.0 vulnerabilities",                           "iis 6.0"),
        ("Search CVE database for PHP 8.0",                               "php 8.0"),
        ("Find CVEs for Tomcat 9.0.0",                                    "tomcat 9.0.0"),
        ("CVE search for MySQL 5.7",                                      "mysql 5.7"),
        ("What vulnerabilities does nginx 1.14 have?",                    "nginx 1.14"),
        ("Search NVD: Drupal 7 vulnerabilities",                          "drupal 7"),
        ("Look up CVEs for ProFTPD 1.3.5",                                "proftpd 1.3.5"),
    ],
    "lazyown_searchsploit": [
        ("Search for vsftpd 2.3.4 exploits",                             "vsftpd 2.3.4"),
        ("Find Metasploit modules for EternalBlue",                       "EternalBlue MS17-010"),
        ("Search exploits for Apache Struts",                             "Apache Struts"),
        ("Look up exploits for Rejetto HFS 2.3",                         "Rejetto HFS 2.3"),
        ("Find exploits for MySQL 5.5",                                   "MySQL 5.5"),
        ("Busca exploits para PHP 5.2",                                   "PHP 5.2"),
        ("Search for SMB exploits in MSF",                                "SMB Windows"),
        ("Find exploit code for ProFTPD",                                 "ProFTPD"),
        ("Search ExploitDB for WordPress plugin vulnerabilities",         "WordPress plugin"),
        ("Find public exploits for OpenSSH 7.2",                         "OpenSSH 7.2"),
        ("Look up Metasploit modules for Samba",                          "Samba"),
        ("Search for Shellshock exploit",                                 "Shellshock bash"),
        ("Find exploit for Drupal 7 (Drupalgeddon)",                      "Drupal 7"),
        ("Search for Struts 2 RCE exploit",                               "Struts 2 RCE"),
        ("Exploit lookup: Tomcat AJP file inclusion",                     "Tomcat AJP"),
    ],
    "lazyown_llm_ask": [
        ("Ask the LLM how to escalate privileges on Linux",               "how to escalate privileges on Linux"),
        ("Use AI to plan the attack on this Windows host",                "plan attack Windows host"),
        ("Ask the LLM to analyze the target's attack surface",           "analyze attack surface 10.10.11.78"),
        ("LLM: how to extract credentials from LSASS?",                  "extract credentials LSASS"),
        ("Pregunta al LLM cómo hacer pass-the-hash",                     "pass-the-hash NTLM"),
        ("Ask AI to reason about the best lateral movement technique",    "best lateral movement technique"),
        ("Use deepseek to find the best exploit path",                    "find best exploit path for 10.10.11.78"),
        ("Ask Groq: how to do AS-REP roasting?",                          "AS-REP roasting Active Directory"),
        ("LLM question: how to bypass UAC on Windows 10?",               "bypass UAC Windows 10"),
        ("Ask the AI: what is the best persistence mechanism for Linux?", "Linux persistence mechanisms"),
        ("Groq: analyze this error message from the target",              "analyze error: permission denied on /etc/shadow"),
        ("Ask AI: how to enumerate LDAP without authentication?",         "unauthenticated LDAP enumeration"),
        ("LLM: explain what this PowerShell one-liner does",             "explain PowerShell command"),
        ("Ask AI about OPSEC considerations for this attack",            "OPSEC for credential dumping"),
    ],

    # ── Memory / RAG ─────────────────────────────────────────────────────────
    "lazyown_rag_index": [
        ("Index all session files into the knowledge base",               ""),
        ("Update the RAG index with new session data",                    ""),
        ("Incrementally index sessions/ into ChromaDB",                   ""),
        ("Re-index all captured data",                                    ""),
        ("Add all session artefacts to the vector database",             ""),
        ("Index new findings into ChromaDB",                              ""),
        ("Update knowledge base with latest session data",                ""),
        ("Sync session files to the RAG database",                        ""),
        ("Index all captured outputs for semantic search",                ""),
        ("Add new loot to the vector store",                              ""),
        ("Rebuild the RAG index from all sessions",                       ""),
    ],
    "lazyown_rag_query": [
        ("Search session data for SMB credentials",                       "SMB credentials"),
        ("Find past nmap results for 10.10.11.78",                       "nmap scan 10.10.11.78"),
        ("Query memory for previous privilege escalation attempts",       "privilege escalation"),
        ("What do we know about domain controllers?",                     "domain controller"),
        ("Search for captured NTLM hashes",                               "NTLM hashes"),
        ("Find any previous findings on port 445",                        "port 445 SMB"),
        ("Search session memory for admin credentials",                   "admin credentials"),
        ("Have we found any database passwords?",                         "database passwords"),
        ("What did we discover about the web server?",                    "web server findings"),
        ("Search memory for Kerberos tickets",                            "Kerberos tickets"),
        ("Find all SMB share enumeration results",                        "SMB shares"),
        ("Query vector store for previous domain findings",               "domain findings"),
    ],
    "lazyown_memory_recall": [
        ("Recall past commands run against 10.10.11.78",                  "10.10.11.78"),
        ("What commands have been executed previously?",                  "previous commands"),
        ("Show episodic memory for nmap scans",                           "nmap"),
        ("Recall credential dumping results",                             "credential dumping"),
        ("What happened during the last session?",                        "last session"),
        ("Show me all past actions on the target",                        "10.10.11.78"),
        ("Recall previous web enumeration results",                       "web enumeration"),
        ("What scans did we run before?",                                 "previous scans"),
        ("Show history of commands run on the target",                    "command history"),
        ("What tools have been used so far?",                             "tool usage history"),
    ],
    "lazyown_memory_store": [
        ("Save this nmap result to episodic memory",                      "nmap -sV 10.10.11.78 → ports 22,80,443"),
        ("Store the discovered SMB credentials",                          "Found credentials admin:Password123"),
        ("Add this finding to memory: RCE via log4j",                    "RCE via log4j on 10.10.11.78"),
        ("Save finding to memory: domain admin hash found",               "Domain admin NTLM hash: aad3b..."),
        ("Store this SQL injection finding in memory",                    "SQLi on /login.php parameter id"),
        ("Save privilege escalation path to memory",                      "SUID binary /usr/bin/python3"),
        ("Remember this lateral movement path",                           "Pass-the-hash to DC via SMB"),
    ],

    # ── Reporting ────────────────────────────────────────────────────────────
    "lazyown_campaign_sitrep": [
        ("Generate a full campaign situation report",                     ""),
        ("Give me the master SITREP",                                     ""),
        ("Show me everything about the current campaign",                 ""),
        ("Campaign overview — all state files",                           ""),
        ("¿Cuál es el estado completo del campaign?",                    ""),
        ("Full operational briefing",                                     ""),
        ("Aggregate all campaign data into one report",                   ""),
        ("What has been accomplished in this engagement?",                ""),
        ("Full status dump: all objectives, findings, creds",             ""),
        ("Brief me on everything discovered in this campaign",            ""),
        ("Master report from all campaign state files",                   ""),
        ("Campaign summary: from recon to current state",                 ""),
        ("Resumen completo de la campaña de pentesting",                  ""),
        ("What is the current engagement progress?",                      ""),
        ("Full campaign intelligence dump",                               ""),
    ],
    "lazyown_c2_notes": [
        ("Add a note: found SMB signing disabled",                        "Found SMB signing disabled on 10.10.11.78"),
        ("Read the operational notes",                                    ""),
        ("Append to notes: domain admin achieved",                       "Domain admin achieved via DCSync"),
        ("Show all operator notes",                                       ""),
        ("Clear old notes",                                               "clear"),
        ("Add finding to ops notes: open port 2049 NFS",                 "NFS port 2049 open on 10.10.11.78"),
        ("Write note: found writable SMB share",                          "Writable share: //10.10.11.78/data"),
        ("Read the current operational log",                              ""),
        ("Note: BloodHound found DA path via AS-REP roasting",           "AS-REP → DA path via corp.local"),
        ("Update notes with this critical finding",                       "RCE on web server via deserialization"),
    ],
    "lazyown_credentials": [
        ("Show all captured credentials",                                 ""),
        ("List all found passwords and hashes",                           ""),
        ("What credentials have been collected?",                         ""),
        ("Display the credential dump",                                   ""),
        ("¿Qué credenciales hemos capturado?",                           ""),
        ("Show NTLM hashes from the session",                             ""),
        ("List all found usernames and passwords",                        ""),
        ("Give me the loot: all creds and hashes",                        ""),
        ("What passwords have we recovered?",                             ""),
        ("Show me all the usernames and hashes found",                    ""),
        ("List captured service account credentials",                     ""),
        ("What logins have we compromised?",                              ""),
        ("Show all clear-text passwords found",                           ""),
        ("Credential inventory from all captures",                        ""),
        ("¿Qué hashes y contraseñas tenemos?",                           ""),
        ("Display all found credentials from session",                    ""),
    ],
    "lazyown_report_update": [
        ("Update the pentest report with new findings",                   "RCE via log4j on 10.10.11.78:8080"),
        ("Add domain admin finding to the report",                        "Achieved domain admin via DCSync"),
        ("Write up the credential dumping finding",                       "Dumped NTLM hashes via secretsdump"),
        ("Update report: found EternalBlue vulnerable host",              "MS17-010 vulnerable: 10.10.11.78"),
        ("Add SMB relay attack to report",                               "SMB relay → NTLM capture"),
        ("Document this critical finding in the report",                  "RCE on Apache 2.4.49"),
        ("Add privilege escalation to report",                            "SUID escalation to root via python3"),
        ("Update pentest report with lateral movement finding",           "Pass-the-hash to 10.10.11.1"),
        ("Write finding: unauthenticated RCE on port 8080",              "Unauthenticated RCE: CVE-2021-41773"),
        ("Add this to the deliverable report",                            "Domain admin achieved 14:32 UTC"),
        ("Update final report with persistence finding",                  "Persistence via scheduled task"),
    ],
    "lazyown_campaign_lessons": [
        ("Show lessons learned from this campaign",                       ""),
        ("What tactical insights were captured?",                         ""),
        ("Read the campaign lessons",                                     ""),
        ("Show retrospective findings",                                   ""),
        ("¿Qué lecciones aprendimos en esta campaña?",                   ""),
        ("What worked and what didn't in this engagement?",               ""),
        ("Campaign retrospective: top findings",                          ""),
        ("What should we do differently next time?",                      ""),
        ("Show tactical lessons from this operation",                     ""),
        ("Read the post-engagement lessons",                              ""),
    ],
    "lazyown_timeline": [
        ("Generate the attack timeline",                                  ""),
        ("Show the red team timeline narrative",                          ""),
        ("Create a chronological account of the attack",                  ""),
        ("Timeline of the engagement",                                    ""),
        ("¿Cuál es la línea de tiempo del ataque?",                      ""),
        ("Give me a timestamp-ordered account of the attack",             ""),
        ("Generate narrative timeline for the report",                    ""),
        ("Create attack timeline from initial recon to domain admin",     ""),
        ("Chronological event log of the engagement",                     ""),
        ("Show what happened and when during the campaign",               ""),
        ("Build a timeline for the executive report",                     ""),
    ],
    "lazyown_generate_report": [
        ("Auto-generate the pentest report",                              ""),
        ("Generate a full Markdown pentest report",                       ""),
        ("Create report from session artefacts",                          ""),
        ("Build the final engagement report",                             ""),
        ("Generate the final deliverable report",                         ""),
        ("Create a professional pentest report",                          ""),
        ("Write the full report from all collected data",                 ""),
        ("Auto-build the engagement report",                              ""),
        ("Generate executive summary + technical report",                 ""),
        ("Produce final pentest deliverable",                             ""),
    ],
    "lazyown_misp_export": [
        ("Export findings as a MISP event",                               ""),
        ("Generate MISP-compatible threat intelligence",                  ""),
        ("Export IoCs and TTPs to MISP format",                           ""),
        ("Create MISP event from campaign findings",                      ""),
        ("Export threat intel to MISP",                                   ""),
        ("Generate MISP-compatible IoC export",                           ""),
        ("Share findings via MISP event",                                 ""),
        ("Export TTPs and indicators to MISP platform",                   ""),
    ],
    "lazyown_eval_quality": [
        ("Show LLM decision quality report",                              ""),
        ("How accurate has the AI routing been?",                         ""),
        ("Display success rate and MITRE tactic coverage",                ""),
        ("Evaluate the quality of previous AI decisions",                 ""),
        ("Rate the AI agent's decision quality",                          ""),
        ("Show me how well the routing decisions have worked",            ""),
        ("Quality metrics for AI-assisted decisions",                     ""),
        ("How many AI recommendations were correct?",                     ""),
        ("Show routing and decision accuracy report",                     ""),
    ],
    "lazyown_collab_publish": [
        ("Broadcast: found domain admin credentials",                     "Found domain admin credentials"),
        ("Share finding with all operators: RCE on port 8080",           "RCE found on port 8080"),
        ("Publish alert: EternalBlue vulnerable host discovered",         "EternalBlue vulnerable: 10.10.11.78"),
        ("Send finding to team: NTLM hashes captured",                   "NTLM hashes captured from 10.10.11.78"),
        ("Notify all operators of this critical finding",                 "Admin credentials found"),
        ("Broadcast to team: got domain admin",                           "Domain admin achieved at 15:42"),
        ("Share this with all operators via SSE",                         "New target discovered: 10.10.11.100"),
        ("Push finding to all team members",                              "SQLi on login page"),
        ("Broadcast alert: got foothold on target",                       "Foothold via log4j on 10.10.11.78"),
        ("Announce to team: captured DA hash",                            "DA hash captured via DCSync"),
    ],

    # ── Events / policy ──────────────────────────────────────────────────────
    "lazyown_poll_events": [
        ("Check for new security events",                                 ""),
        ("Poll the event engine for alerts",                              ""),
        ("Are there any pending events?",                                 ""),
        ("Show latest detection events",                                  ""),
        ("¿Hay eventos nuevos de detección?",                             ""),
        ("Get new alerts from the event engine",                          ""),
        ("Check if any detections have fired",                            ""),
        ("Read the latest events",                                        ""),
        ("Poll for new alerts",                                           ""),
        ("Any new triggers or alerts?",                                   ""),
        ("Show me the pending event queue",                               ""),
        ("Check detection engine for new events",                         ""),
    ],
    "lazyown_ack_event": [
        ("Acknowledge event evt_001",                                     "evt_001"),
        ("Mark event 42 as processed",                                    "42"),
        ("Dismiss the RCE alert",                                         "evt_rce_001"),
        ("Acknowledge all pending events",                                "all"),
        ("Mark the privilege escalation alert as handled",                "evt_privesc_001"),
        ("Dismiss false positive event",                                  "evt_002"),
        ("Acknowledge and close event 15",                                "15"),
        ("Mark event as resolved",                                        "evt_003"),
    ],
    "lazyown_add_rule": [
        ("Add detection rule for RCE events",                             "pattern=shell event_type=critical"),
        ("Create rule: trigger alert on privilege escalation commands",   "pattern=sudo event_type=high"),
        ("Add event rule for credential access",                          "pattern=mimikatz event_type=critical"),
        ("Create detection for lateral movement",                         "pattern=psexec event_type=high"),
        ("Add rule to detect Kerberoasting",                              "pattern=kerberoast event_type=critical"),
        ("Create alert rule for BloodHound usage",                        "pattern=bloodhound event_type=high"),
        ("Add detection for DCSync activity",                             "pattern=dcsync event_type=critical"),
        ("Create rule: alert on new beacon check-in",                     "pattern=beacon event_type=medium"),
    ],
    "lazyown_list_event_rules": [
        ("List all detection rules",                                      ""),
        ("Show active event rules",                                       ""),
        ("What detection rules are configured?",                          ""),
        ("Display all event detection policies",                          ""),
        ("Show all configured alerts",                                    ""),
        ("What rules are active in the event engine?",                    ""),
        ("List detection policies",                                       ""),
        ("Show me all the alerting rules",                                ""),
        ("Display rule catalog",                                          ""),
    ],
    "lazyown_heartbeat_status": [
        ("Is the LazyOwn heartbeat running?",                             ""),
        ("Check if the heartbeat process is alive",                       ""),
        ("Heartbeat health check",                                        ""),
        ("Is the event engine online?",                                   ""),
        ("Is the daemon process alive?",                                  ""),
        ("Check LazyOwn process health",                                  ""),
        ("Is the background process running?",                            ""),
        ("Heartbeat ping",                                                ""),
        ("¿Está vivo el proceso de heartbeat?",                          ""),
        ("Health check for LazyOwn services",                             ""),
    ],
    "lazyown_policy_status": [
        ("Show policy engine status",                                     ""),
        ("What is the current policy reward summary?",                    ""),
        ("Display rules of engagement compliance",                        ""),
        ("Policy engine: next recommended actions",                       ""),
        ("¿Cuál es el estado de la política de ataque?",                 ""),
        ("Show ROE policy status",                                        ""),
        ("Policy summary: what is allowed?",                              ""),
        ("What actions are currently authorized by policy?",              ""),
        ("Display engagement policy constraints",                         ""),
        ("Show the policy engine recommendations",                        ""),
        ("What does the ROE allow me to do now?",                         ""),
    ],

    # ── Automation ───────────────────────────────────────────────────────────
    "lazyown_auto_loop": [
        ("Start the autonomous attack loop on 10.10.11.78",               "10.10.11.78"),
        ("Begin automated enumeration and exploitation",                  "10.10.11.78"),
        ("Run the auto-loop until domain admin is achieved",              "10.10.11.78"),
        ("Start continuous automated attack",                             "10.10.11.78"),
        ("Inicia el bucle de ataque automático",                          "10.10.11.78"),
        ("Launch auto-loop targeting 192.168.1.100",                      "192.168.1.100"),
        ("Enable the autonomous attack automation",                       "10.10.11.78"),
        ("Start the policy-guided attack loop",                           "10.10.11.78"),
        ("Run LazyOwn on autopilot against the target",                   "10.10.11.78"),
        ("Begin automated pentest loop",                                  "10.10.11.78"),
        ("Start autonomous operation against this host",                  "10.10.11.78"),
        ("Turn on auto-attack mode",                                      "10.10.11.78"),
        ("Pon en marcha el modo autónomo contra el objetivo",             "10.10.11.78"),
    ],
    "lazyown_inject_objective": [
        ("Inject objective: achieve domain admin",                        "achieve domain admin on corp.local"),
        ("Add new objective: exfiltrate /etc/shadow",                     "exfiltrate /etc/shadow"),
        ("Inject goal: find and exploit SQLi on web app",                "find and exploit SQL injection"),
        ("New objective: dump all NTLM hashes",                           "dump all NTLM hashes"),
        ("Inyecta objetivo: escalar privilegios a root",                  "escalate privileges to root"),
        ("Add task: establish persistence on 10.10.11.78",               "establish persistence on 10.10.11.78"),
        ("Inject new mission: exfiltrate sensitive documents",            "exfiltrate sensitive documents"),
        ("Add objective: compromise the mail server",                     "compromise mail server 10.10.11.50"),
        ("New goal for daemon: move laterally to the DC",                 "lateral movement to domain controller"),
        ("Inject: disable Windows Defender on target",                    "disable Windows Defender"),
        ("New objective: find database credentials",                      "find and extract database credentials"),
    ],
    "lazyown_next_objective": [
        ("What is the next objective to work on?",                        ""),
        ("Show the current frontier-model context",                       ""),
        ("Get the next pending attack objective",                         ""),
        ("What objective should be tackled next?",                        ""),
        ("¿Cuál es el próximo objetivo?",                                 ""),
        ("What is the highest priority task?",                            ""),
        ("Show pending objectives queue",                                 ""),
        ("What should the daemon attack next?",                           ""),
        ("Next mission in the objective queue",                           ""),
        ("What is the current priority objective?",                       ""),
        ("Display next objective from the queue",                         ""),
    ],
    "lazyown_read_prompt": [
        ("Read the LazyOwn developer reference",                          ""),
        ("Show the LazyOwn architecture reference",                       ""),
        ("Load the prompt.md documentation",                              ""),
        ("Get the full tool and command reference",                       ""),
        ("Show me the LazyOwn command catalog",                           ""),
        ("Read the full tool documentation",                              ""),
        ("Display the prompt reference file",                             ""),
        ("What does prompt.md contain?",                                  ""),
        ("Load developer documentation",                                  ""),
    ],
    "lazyown_soul": [
        ("Read the agent soul and campaign objectives",                   ""),
        ("Show the agent persona and priorities",                         ""),
        ("Update agent soul with new campaign objective",                 "achieve stealth domain admin"),
        ("What are the hard stops in the soul file?",                     ""),
        ("¿Cuál es el alma del agente?",                                  ""),
        ("Show the agent's mission, values, and hard limits",             ""),
        ("Read current soul configuration",                               ""),
        ("What is the agent's primary directive?",                        ""),
        ("Show agent soul: identity, mission, constraints",               ""),
        ("Update soul: new campaign is financial crime simulation",       "financial crime simulation"),
        ("What are the agent's red lines?",                               ""),
    ],

    # ── Agents ───────────────────────────────────────────────────────────────
    "lazyown_run_agent": [
        ("Run an AI agent to enumerate Active Directory",                 "enumerate Active Directory on 10.10.11.78"),
        ("Delegate SMB exploitation to an autonomous agent",              "exploit SMB on 10.10.11.78"),
        ("Start a Groq agent to perform recon",                           "recon 10.10.11.78 with nmap and gobuster"),
        ("Run Ollama agent to find privilege escalation paths",           "find privilege escalation paths"),
        ("Delegate web application testing to AI agent",                 "test web application on 10.10.11.78:80"),
        ("Launch autonomous agent for credential dumping",               "dump credentials from 10.10.11.78"),
        ("Run agent to perform full recon and report",                    "full recon and report on 10.10.11.78"),
        ("Send an AI sub-agent to test for SQLi",                         "test for SQL injection on 10.10.11.78"),
        ("Delegate BloodHound enumeration to an agent",                  "BloodHound AD enumeration on corp.local"),
        ("Run a sub-agent to brute force the login page",                 "brute force login on 10.10.11.78:80"),
        ("Launch agent to test for command injection",                    "test command injection on web app"),
        ("Start AI agent for full web application scan",                  "full web scan on 10.10.11.78:443"),
        ("Delegate kerberoasting to autonomous agent",                    "Kerberoast accounts in corp.local"),
        ("Run agent: find all paths to domain admin",                     "find domain admin paths in corp.local"),
        ("Let an agent handle the privilege escalation",                  "find and exploit privesc on 10.10.11.78"),
    ],
    "lazyown_agent_status": [
        ("Check the status of agent agent_001",                           "agent_001"),
        ("Is the running agent done?",                                    ""),
        ("Show agent progress and current action",                        ""),
        ("How many iterations has the agent completed?",                  ""),
        ("¿Cómo va el agente autónomo?",                                  ""),
        ("Is the sub-agent finished yet?",                                ""),
        ("Show the current step of the running agent",                    ""),
        ("How far along is the agent?",                                   ""),
        ("Agent progress report",                                         ""),
        ("Is agent_001 still working?",                                   "agent_001"),
        ("Check if the web testing agent has finished",                   ""),
        ("What is the agent currently doing?",                            ""),
    ],
    "lazyown_agent_result": [
        ("Get the result from agent agent_001",                           "agent_001"),
        ("Read the agent's final answer",                                 ""),
        ("Show what the agent discovered",                                ""),
        ("Agent output: what did it find?",                               ""),
        ("Get findings from the completed agent",                         ""),
        ("Read the agent report",                                         ""),
        ("Show me what the sub-agent found",                              ""),
        ("Agent is done — show the results",                              ""),
        ("Retrieve the agent's output",                                   ""),
        ("What did agent_001 discover?",                                  "agent_001"),
    ],
    "lazyown_list_agents": [
        ("List all running and completed agents",                         ""),
        ("Show recent sub-agents",                                        ""),
        ("What agents are active?",                                       ""),
        ("¿Qué agentes están corriendo?",                                 ""),
        ("Show the agent inventory",                                      ""),
        ("List all sub-agents and their status",                          ""),
        ("What AI agents have been spawned?",                             ""),
        ("Show me all running and past agents",                           ""),
        ("Agent registry: who is running what?",                          ""),
        ("List active and completed sub-agents",                          ""),
    ],
    "lazyown_groq_agent": [
        ("Spawn a Groq agent for Active Directory enumeration",           "enumerate Active Directory"),
        ("Run a Groq agent with all LazyOwn tools",                       "full recon and exploit 10.10.11.78"),
        ("Start Ollama agent for privilege escalation",                   "find and exploit privesc paths"),
        ("Launch Groq agent to enumerate SMB shares",                     "enumerate SMB shares on 10.10.11.78"),
        ("Start a Groq-powered AI agent",                                 "full pentest of 10.10.11.78"),
        ("Spawn Groq agent with full tool access",                        "recon and exploit 10.10.11.78"),
        ("Run deepseek-r1 agent on the target",                           "find vulnerabilities on 10.10.11.78"),
        ("Launch AI agent backed by Groq LLM",                           "enumerate and compromise 10.10.11.78"),
        ("Start Groq agent to analyze the AD environment",                "Active Directory enumeration corp.local"),
        ("Spawn an Ollama agent for local inference",                     "full offline pentest of 10.10.11.78"),
        ("Use Groq to run an autonomous pentest",                         "autonomous pentest 10.10.11.78"),
    ],

    # ── Hive mind ────────────────────────────────────────────────────────────
    "lazyown_hive_spawn": [
        ("Spawn 3 drones to enumerate SMB on 10.10.11.78",               "enumerate SMB shares on 10.10.11.78"),
        ("Spawn parallel drones for full AD enumeration",                 "full Active Directory enumeration"),
        ("Spawn recon and exploit drones in parallel",                    "recon and exploit 10.10.11.78"),
        ("Create a hive with 5 drones for domain compromise",             "domain compromise corp.local"),
        ("Spawn drones: recon, creds, lateral movement",                  "parallel pentest 10.10.11.78"),
        ("Use the hive to enumerate all services in parallel",            "enumerate all services on 10.10.11.78"),
        ("Deploy multiple drones in parallel against the target",         "parallel attack 10.10.11.78"),
        ("Hive spawn: web, SMB, and LDAP enumeration drones",            "web SMB LDAP parallel enum"),
        ("Launch parallel drone swarm for recon",                         "parallel recon 10.10.11.78"),
        ("Spawn drones to simultaneously scan and exploit",               "simultaneous recon and exploit"),
        ("Create drone army to attack AD from multiple angles",           "multi-vector AD attack corp.local"),
        ("Hive attack: launch 4 parallel drones",                         "parallel pentest 10.10.11.78"),
        ("Deploy the hive mind against the target",                       "full hive pentest 10.10.11.78"),
        ("Start multi-drone operation",                                   "multi-drone attack 10.10.11.78"),
        ("¡Lanza el enjambre de drones contra el objetivo!",             "enjambre 10.10.11.78"),
    ],
    "lazyown_hive_status": [
        ("Show hive-mind status",                                         ""),
        ("How many drones are active?",                                   ""),
        ("Hive status: drones and memory",                                ""),
        ("What is the queen doing?",                                      ""),
        ("¿Cuál es el estado de la mente colmena?",                      ""),
        ("How many drones are running?",                                  ""),
        ("Hive intelligence report",                                      ""),
        ("Status of the distributed drone swarm",                         ""),
        ("Show drone swarm status",                                       ""),
        ("How is the hive performing?",                                   ""),
        ("Hive overview: active drones and collected data",               ""),
        ("Show me all drone statuses",                                    ""),
    ],
    "lazyown_hive_recall": [
        ("Search hive memory for domain admin credentials",               "domain admin credentials"),
        ("Recall all drone results about SMB",                            "SMB enumeration"),
        ("Hive memory: what do we know about the DC?",                    "domain controller"),
        ("Search drone findings for NTLM hashes",                        "NTLM hashes"),
        ("What did the drones find about the web server?",                "web server"),
        ("Search collective memory for privilege escalation paths",       "privilege escalation"),
        ("Query hive mind for AD enumeration results",                    "Active Directory"),
        ("What has the swarm discovered about port 445?",                 "SMB port 445"),
        ("Recall drone findings about Kerberos",                          "Kerberos"),
        ("Search hive memory for lateral movement opportunities",         "lateral movement"),
        ("¿Qué encontró el enjambre sobre el dominio?",                  "dominio Active Directory"),
    ],
    "lazyown_hive_plan": [
        ("Plan a domain compromise without spawning drones",              "full domain compromise"),
        ("Decompose AD enumeration into drone tasks",                     "Active Directory enumeration"),
        ("Plan the attack: recon → exploit → privesc → lateral",         "full attack chain"),
        ("Generate task decomposition for this engagement",               "10.10.11.78 pentest"),
        ("Break down the domain compromise into drone tasks",             "domain compromise corp.local"),
        ("Plan a multi-drone parallel attack strategy",                   "parallel attack 10.10.11.78"),
        ("Decompose this goal into parallel tasks",                       "compromise 10.10.11.78"),
        ("Task planning: split the engagement across drones",             "AD enumeration and exploitation"),
        ("Create a work breakdown for the hive",                          "full kill chain 10.10.11.78"),
        ("Design parallel attack plan for hive",                          "corp.local domain compromise"),
    ],
    "lazyown_hive_result": [
        ("Get drone_001 result",                                          "drone_001"),
        ("Read the output from drone 2",                                  "drone_002"),
        ("Show what the recon drone found",                               "drone_recon_001"),
        ("Retrieve drone_001 findings",                                   "drone_001"),
        ("What did the SMB drone discover?",                              "drone_smb_001"),
        ("Show output from the web testing drone",                        "drone_web_001"),
        ("Read the lateral movement drone result",                        "drone_lateral_001"),
        ("Get findings from recon drone",                                 "drone_recon_001"),
    ],
    "lazyown_hive_collect": [
        ("Wait for drones and summarize results",                         "drone_001,drone_002"),
        ("Collect and synthesize all drone outputs",                      "drone_001,drone_002,drone_003"),
        ("Queen: summarize what the drones found",                        "drone_001,drone_002"),
        ("Aggregate drone results into a unified report",                 "drone_001,drone_002,drone_003"),
        ("Collect all drone findings and create a summary",               "drone_001,drone_002"),
        ("Synthesize drone outputs into actionable intelligence",         "drone_001,drone_002"),
        ("Merge drone results and identify next steps",                   "drone_001,drone_002"),
        ("Get the combined output from all finished drones",              "drone_001,drone_002,drone_003"),
    ],
    "lazyown_hive_forget": [
        ("Prune hive memory older than 24 hours",                         "24"),
        ("Clear old drone results from memory",                           "48"),
        ("Forget hive memory about the test environment",                 "72"),
        ("Clean up stale drone memories",                                 "24"),
        ("Delete old hive entries",                                       "48"),
        ("Purge hive memory older than 2 days",                           "48"),
        ("Clear hive memory to free space",                               "24"),
        ("Remove outdated drone results",                                 "72"),
    ],
    "lazyown_hive_recover": [
        ("Recover interrupted hive drones",                               ""),
        ("Re-queue drones after crash",                                   ""),
        ("Restore hive state after restart",                              ""),
        ("Resume interrupted drone tasks",                                ""),
        ("Recover failed drones and restart them",                        ""),
        ("Hive recovery: restart crashed drones",                         ""),
        ("Restore the swarm after a system restart",                      ""),
        ("Re-launch drones that were interrupted",                        ""),
    ],

    # ── Autonomous daemon ────────────────────────────────────────────────────
    "lazyown_autonomous_start": [
        ("Start autonomous mode targeting 10.10.11.78",                   "achieve domain admin on 10.10.11.78"),
        ("Begin fully autonomous attack on corp.local",                   "compromise corp.local domain"),
        ("Start the autonomous daemon with objective: get root",          "escalate to root on 10.10.11.78"),
        ("Run autonomous agent to find and exploit vulnerabilities",      "find and exploit all vulns on 10.10.11.78"),
        ("Inicia el daemon autónomo para comprometer el objetivo",        "comprometer 10.10.11.78"),
        ("Launch the autonomous attack daemon",                           "full compromise 10.10.11.78"),
        ("Start self-directed pentest against the target",                "autonomous pentest 10.10.11.78"),
        ("Begin autonomous operation — no Claude Code needed",            "full autonomous attack 10.10.11.78"),
        ("Start the fallback autonomous brain",                           "attack 10.10.11.78 autonomously"),
        ("Run without Claude: start autonomous daemon",                   "autonomous compromise 10.10.11.78"),
        ("Launch fully autonomous attack mode",                           "full attack 10.10.11.78"),
        ("Start background autonomous pentest",                           "pentest 10.10.11.78 autonomously"),
        ("Modo autónomo: comprometer el objetivo sin supervisión",        "comprometer 10.10.11.78"),
        ("Kickoff autonomous attack loop",                                "autonomous attack 10.10.11.78"),
    ],
    "lazyown_autonomous_stop": [
        ("Stop the autonomous daemon",                                    ""),
        ("Halt the autonomous attack loop",                               ""),
        ("Stop automated exploitation",                                   ""),
        ("¡Para el daemon autónomo!",                                     ""),
        ("Kill the autonomous daemon process",                            ""),
        ("Pause the autonomous attack",                                   ""),
        ("Stop autonomous mode",                                          ""),
        ("Terminate the background daemon",                               ""),
        ("Abort autonomous operation",                                    ""),
        ("Halt self-directed attack",                                     ""),
        ("Stop the fallback brain",                                       ""),
        ("Detén el ataque autónomo",                                      ""),
    ],
    "lazyown_autonomous_status": [
        ("What is the autonomous daemon doing?",                          ""),
        ("Autonomous daemon status",                                      ""),
        ("How many steps has the daemon completed?",                      ""),
        ("Show the current autonomous objective",                         ""),
        ("¿Cómo va el daemon autónomo?",                                  ""),
        ("What phase is the daemon in?",                                  ""),
        ("Show autonomous operation progress",                            ""),
        ("How far along is the autonomous attack?",                       ""),
        ("Daemon status: current phase, steps, objectives",               ""),
        ("What has the autonomous daemon accomplished?",                  ""),
        ("Check the self-directed attack status",                         ""),
        ("Show me what the daemon is doing right now",                    ""),
    ],
    "lazyown_autonomous_inject": [
        ("Inject new objective into autonomous daemon: dump credentials", "dump all credentials from 10.10.11.78"),
        ("Add objective to daemon: exfiltrate sensitive files",           "exfiltrate /etc/shadow"),
        ("Tell the daemon to focus on lateral movement now",              "perform lateral movement to 10.10.11.100"),
        ("Inject priority task: find the domain controller",              "locate and enumerate domain controller"),
        ("New mission for autonomous daemon: pivot to internal network",  "pivot to 192.168.0.0/16"),
        ("Add urgent objective: disable EDR on target",                   "disable EDR on 10.10.11.78"),
        ("Inject: the target changed to 10.10.11.200",                   "switch target to 10.10.11.200"),
        ("New priority: establish persistence before moving on",          "establish persistence on 10.10.11.78"),
        ("Tell daemon: skip recon, go straight to exploitation",          "skip to exploitation phase"),
        ("Add objective to daemon: escalate to SYSTEM",                   "escalate to SYSTEM on Windows target"),
    ],
    "lazyown_autonomous_events": [
        ("Show the last 20 autonomous events",                            "20"),
        ("Read the autonomous event stream",                              ""),
        ("Show recent daemon activity",                                   ""),
        ("What has the autonomous daemon done so far?",                   ""),
        ("Daemon log: last 50 events",                                    "50"),
        ("Show autonomous attack history",                                ""),
        ("What actions has the daemon taken?",                            ""),
        ("Event stream from the autonomous attack",                       ""),
        ("Show last N steps from the daemon",                             "30"),
        ("Autonomous activity log",                                       ""),
        ("What did the daemon do in the last hour?",                      ""),
    ],

    # ── Tools / objectives ───────────────────────────────────────────────────
    "lazyown_create_tool": [
        ("Create a pwntomate tool for vsftpd 2.3.4",                      "vsftpd 2.3.4"),
        ("Add a tool file for automatic Apache exploit",                  "apache 2.4.49"),
        ("Create a pwntomate rule for SMB vulnerabilities",               "SMB Windows"),
        ("New tool file for MySQL 5.5 exploitation",                      "mysql 5.5"),
        ("Create a .tool file for log4j exploitation",                    "log4j RCE"),
        ("Add pwntomate entry for Drupal 7",                              "Drupal 7"),
        ("Create automation rule for ProFTPD exploit",                    "ProFTPD 1.3.5"),
        ("New tool definition for vsftpd backdoor",                       "vsftpd 2.3.4 backdoor"),
        ("Create tool file for Rejetto HFS exploit",                      "HFS 2.3"),
        ("Add new tool to LazyOwn tool catalog",                          "new exploit service"),
    ],
}

# ---------------------------------------------------------------------------
# Chain examples — multi-step realistic workflows
# ---------------------------------------------------------------------------

_CHAINS: List[Dict] = [
    # Recon chain
    {
        "instruction": "Start a new session, show sitrep, then set target to 10.10.11.78",
        "tool": "lazyown_session_init", "arg": "",
        "domain": "Security/Recon",
        "note": "multi-step: session_init → set_config → lazynmap"
    },
    {
        "instruction": "After the nmap scan completes, auto-populate the configuration",
        "tool": "lazyown_auto_populate", "arg": "",
        "domain": "Security/Recon",
        "note": "post-scan config update"
    },
    {
        "instruction": "Scan completed, recommend what to do next",
        "tool": "lazyown_recommend_next", "arg": "",
        "domain": "Security/Intel",
        "note": "post-scan recommendation"
    },
    # Exploitation chain
    {
        "instruction": "I found vsftpd 2.3.4 running, search for exploits",
        "tool": "lazyown_searchsploit", "arg": "vsftpd 2.3.4",
        "domain": "Security/Exploit",
        "note": "exploit search after service discovery"
    },
    {
        "instruction": "vsftpd exploit worked, I have a shell — dump credentials",
        "tool": "lazyown_credentials", "arg": "",
        "domain": "Security/Exploit",
        "note": "post-exploitation credential harvest"
    },
    {
        "instruction": "Got credentials admin:Password123 — update the config",
        "tool": "lazyown_set_config", "arg": "user=admin",
        "domain": "Security/Config",
        "note": "update config after credential capture"
    },
    # AD chain
    {
        "instruction": "We have domain credentials, spawn hive drones to enumerate AD",
        "tool": "lazyown_hive_spawn", "arg": "enumerate Active Directory corp.local",
        "domain": "Security/Hive",
        "note": "hive spawn after credential capture"
    },
    {
        "instruction": "Hive found Kerberoastable accounts — inject DCSync objective",
        "tool": "lazyown_inject_objective", "arg": "perform DCSync against corp.local",
        "domain": "Security/Autonomous",
        "note": "objective injection after discovery"
    },
    {
        "instruction": "Domain admin achieved — generate the full pentest report",
        "tool": "lazyown_generate_report", "arg": "",
        "domain": "Security/Report",
        "note": "report generation at end of engagement"
    },
    # Monitoring chain
    {
        "instruction": "Poll for events, then acknowledge the RCE alert",
        "tool": "lazyown_poll_events", "arg": "",
        "domain": "Security/Events",
        "note": "event monitoring workflow"
    },
    {
        "instruction": "Broadcast finding to team: found domain admin hash",
        "tool": "lazyown_collab_publish", "arg": "Found domain admin NTLM hash",
        "domain": "Security/Report",
        "note": "team collaboration after finding"
    },

    # ── Additional workflow chains ────────────────────────────────────────────
    # Recon chains
    {"instruction": "HTB box is live — port scan it",
     "tool": "lazyown_run_command", "arg": "lazynmap", "domain": "Security/Execution"},
    {"instruction": "Nmap done, now enumerate web directories",
     "tool": "lazyown_run_command", "arg": "lazygobuster", "domain": "Security/Execution"},
    {"instruction": "Found open ports — auto-populate config from scan",
     "tool": "lazyown_auto_populate", "arg": "", "domain": "Security/Config"},
    {"instruction": "Config updated — what should I do now?",
     "tool": "lazyown_recommend_next", "arg": "", "domain": "Security/Intel"},
    # Initial access chains
    {"instruction": "Port 21 running vsftpd 2.3.4 — find exploits",
     "tool": "lazyown_searchsploit", "arg": "vsftpd 2.3.4", "domain": "Security/Intel"},
    {"instruction": "Got RCE — now look for privesc paths",
     "tool": "lazyown_c2_vuln_analysis", "arg": "privilege escalation", "domain": "Security/Intel"},
    {"instruction": "Shell obtained — recommend next action",
     "tool": "lazyown_recommend_next", "arg": "", "domain": "Security/Intel"},
    # Post-exploitation chains
    {"instruction": "Got user shell, escalate to root now",
     "tool": "lazyown_run_command", "arg": "lazyown_privesc", "domain": "Security/Execution"},
    {"instruction": "Root achieved — dump all credentials",
     "tool": "lazyown_credentials", "arg": "", "domain": "Security/Report"},
    {"instruction": "Credentials captured — update report",
     "tool": "lazyown_report_update", "arg": "Root access and credential dump on 10.10.11.78", "domain": "Security/Report"},
    # C2 chains
    {"instruction": "Deployed beacon — check if it checked in",
     "tool": "lazyown_get_beacons", "arg": "", "domain": "Security/C2"},
    {"instruction": "Beacon connected — task it with whoami",
     "tool": "lazyown_c2_command", "arg": "whoami", "domain": "Security/C2"},
    {"instruction": "C2 shell active — run systeminfo to fingerprint",
     "tool": "lazyown_c2_command", "arg": "systeminfo", "domain": "Security/C2"},
    # AD attack chains
    {"instruction": "Have domain creds — enumerate with BloodHound via agent",
     "tool": "lazyown_run_agent", "arg": "BloodHound enumeration corp.local", "domain": "Security/Agents"},
    {"instruction": "BloodHound found DA path — plan the operation",
     "tool": "lazyown_c2_redop", "arg": "domain admin via Kerberoasting", "domain": "Security/Intel"},
    {"instruction": "Operation planned — inject it as daemon objective",
     "tool": "lazyown_autonomous_inject", "arg": "Kerberoast accounts then DCSync", "domain": "Security/Autonomous"},
    {"instruction": "Daemon running — check its current status",
     "tool": "lazyown_autonomous_status", "arg": "", "domain": "Security/Autonomous"},
    # Hive chains
    {"instruction": "Large network — deploy hive drones to enumerate in parallel",
     "tool": "lazyown_hive_spawn", "arg": "parallel recon on 10.10.11.0/24", "domain": "Security/Hive"},
    {"instruction": "Drones deployed — check hive status",
     "tool": "lazyown_hive_status", "arg": "", "domain": "Security/Hive"},
    {"instruction": "Drones finished — collect all their results",
     "tool": "lazyown_hive_collect", "arg": "drone_001,drone_002,drone_003", "domain": "Security/Hive"},
    # Intel chains
    {"instruction": "Found log4j on the server — CVE analysis",
     "tool": "lazyown_c2_vuln_analysis", "arg": "log4j CVE-2021-44228", "domain": "Security/Intel"},
    {"instruction": "Confirmed log4j RCE — generate exploit script",
     "tool": "lazyown_c2_script", "arg": "log4j JNDI RCE exploit", "domain": "Security/Intel"},
    {"instruction": "Engagement done — produce final pentest report",
     "tool": "lazyown_generate_report", "arg": "", "domain": "Security/Report"},
    {"instruction": "Report ready — export threat intel to MISP",
     "tool": "lazyown_misp_export", "arg": "", "domain": "Security/Report"},
    # Campaign close
    {"instruction": "End of engagement — lessons learned?",
     "tool": "lazyown_campaign_lessons", "arg": "", "domain": "Security/Report"},
    {"instruction": "New shift starting — show full campaign SITREP",
     "tool": "lazyown_campaign_sitrep", "arg": "", "domain": "Security/Report"},
    {"instruction": "Shift handover — what is the session state?",
     "tool": "lazyown_session_state", "arg": "", "domain": "Security/Config"},
]

# ---------------------------------------------------------------------------
# Dataset builder
# ---------------------------------------------------------------------------

def _make_record(tool_name: str, desc: str, category: str, instruction: str, arg: str) -> Dict:
    return {
        "instruction": instruction,
        "api_list": [{
            "tool_name":            tool_name,
            "api_name":             f"{tool_name}_endpoint",
            "api_description":      desc,
            "required_parameters":  [{"name": "arg", "type": "STRING",
                                       "description": "tool argument"}],
            "optional_parameters":  [],
        }],
        "answer":  f"[TOOL_CALL: {tool_name}({arg})] [result captured during pentest]",
        "domain":  f"Security/{category}",
    }


_IP_SUBS = [
    ("10.10.11.78",  "10.10.10.5"),
    ("10.10.11.78",  "192.168.1.100"),
    ("10.10.11.78",  "172.16.0.50"),
    ("10.10.11.1",   "10.10.11.200"),
    ("192.168.1.100","10.10.11.50"),
]

_PREFIXES_EN = [
    "I need to {}", "Let me {}", "Can you {}?", "Please {}",
    "Help me {}", "I want to {}", "Time to {}", "Go ahead and {}",
]
_PREFIXES_ES = [
    "Necesito {}", "Quiero {}", "Por favor {}",
    "Ayúdame a {}", "Vamos a {}",
]

_CMD_VERBS = [
    ("Run ", "Execute "), ("Run ", "Launch "), ("Run ", "Start "),
    ("Show ", "Display "), ("Show ", "Print "), ("Show ", "List "),
    ("Check ", "Verify "), ("Check ", "Inspect "), ("Check ", "Test "),
    ("Get ", "Fetch "), ("Get ", "Retrieve "), ("Get ", "Read "),
]


def _expand(tool_name: str, phrasings: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
    """Generate additional phrasings via IP substitution, prefix injection, and verb swap."""
    result = list(phrasings)
    seen = {p[0].lower() for p in phrasings}

    # 1. IP substitution — vary the target IP in existing phrasings
    for instr, arg in phrasings:
        for old_ip, new_ip in _IP_SUBS:
            if old_ip in instr:
                new_instr = instr.replace(old_ip, new_ip)
                new_arg   = arg.replace(old_ip, new_ip)
                if new_instr.lower() not in seen:
                    seen.add(new_instr.lower())
                    result.append((new_instr, new_arg))
                    break  # one substitution per source phrasing

    # 2. Prefix injection — only on short imperative phrasings starting with an action verb
    _ACTION_VERBS = {
        "run", "show", "get", "list", "check", "generate", "create", "add",
        "set", "start", "stop", "read", "search", "find", "execute", "display",
        "launch", "spawn", "inject", "update", "build", "export", "poll",
        "broadcast", "send", "scan", "enumerate", "analyze", "deploy",
    }
    imperatives = [
        (i, a) for i, a in phrasings
        if len(i) <= 55 and "?" not in i and "→" not in i and "—" not in i
        and (i.split()[0].lower() if i.split() else "") in _ACTION_VERBS
    ]
    random.shuffle(imperatives)
    en_used = es_used = 0
    for instr, arg in imperatives:
        verb = instr.split()[0]
        rest = instr[len(verb):].lstrip()
        lowered_instr = verb.lower() + (" " + rest if rest else "")
        if en_used < 3:
            new_instr = _PREFIXES_EN[en_used % len(_PREFIXES_EN)].format(lowered_instr)
            if new_instr.lower() not in seen:
                seen.add(new_instr.lower())
                result.append((new_instr, arg))
                en_used += 1
        if es_used < 2:
            new_instr = _PREFIXES_ES[es_used % len(_PREFIXES_ES)].format(lowered_instr)
            if new_instr.lower() not in seen:
                seen.add(new_instr.lower())
                result.append((new_instr, arg))
                es_used += 1

    # 3. Verb synonym swap (Run→Execute, Show→Display, etc.)
    for instr, arg in phrasings:
        for old_v, new_v in _CMD_VERBS:
            if instr.startswith(old_v):
                new_instr = new_v + instr[len(old_v):]
                if new_instr.lower() not in seen:
                    seen.add(new_instr.lower())
                    result.append((new_instr, arg))
                    break

    return result


def build_dataset() -> List[Dict]:
    records: List[Dict] = []

    for (tool_name, desc, category, _default_arg) in _TOOLS:
        phrasings = _PHRASINGS.get(tool_name, [])
        if not phrasings:
            continue
        expanded = _expand(tool_name, phrasings)
        for instruction, arg in expanded:
            records.append(_make_record(tool_name, desc, category, instruction, arg))

    # Chain examples
    tool_map = {t[0]: (t[1], t[2]) for t in _TOOLS}
    for chain in _CHAINS:
        tname = chain["tool"]
        desc, cat = tool_map.get(tname, ("LazyOwn tool", "Security"))
        records.append(_make_record(tname, desc, cat, chain["instruction"], chain["arg"]))

    random.shuffle(records)
    return records


def write_jsonl(records: List[Dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def print_stats(records: List[Dict]) -> None:
    from collections import Counter
    tool_counts = Counter(r["api_list"][0]["tool_name"] for r in records)
    domain_counts = Counter(r["domain"] for r in records)
    print(f"\nTotal examples : {len(records)}")
    print(f"Unique tools   : {len(tool_counts)}")
    print(f"\nBy domain:")
    for domain, count in sorted(domain_counts.items(), key=lambda x: -x[1]):
        print(f"  {domain:<35s} {count:3d}")
    print(f"\nTop 10 tools by example count:")
    for tool, count in tool_counts.most_common(10):
        print(f"  {tool:<45s} {count:3d}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate rich LazyOwn ToolBench dataset for TopoSwarm continual learning"
    )
    parser.add_argument("--out", default="data_toolbench/lazyown_full.jsonl",
                        help="Output JSONL path")
    parser.add_argument("--stats", action="store_true",
                        help="Print dataset statistics and exit")
    args = parser.parse_args()

    records = build_dataset()
    out_path = Path(args.out)
    write_jsonl(records, out_path)
    print(f"[dataset] Wrote {len(records)} examples → {out_path}")

    if args.stats:
        print_stats(records)


if __name__ == "__main__":
    main()
