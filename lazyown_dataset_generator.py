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
    ],
    "lazyown_command_help": [
        ("How do I use the lazynmap command?",                            "lazynmap"),
        ("Get help for lazygobuster",                                     "lazygobuster"),
        ("What parameters does lazybrute accept?",                        "lazybrute"),
        ("Explain the lazymsf command",                                   "lazymsf"),
        ("Show documentation for lazywebscan",                            "lazywebscan"),
        ("How does the bloodhound command work in lazyown?",              "lazybloodhound"),
    ],
    "lazyown_phase_guide": [
        ("Guide me through the reconnaissance phase",                     "recon"),
        ("Full operator guide for enumeration",                           "enum"),
        ("How should I approach exploitation?",                           "exploit"),
        ("Post-exploitation phase guide",                                 "post"),
        ("Guía completa para la fase de escalada de privilegios",         "privesc"),
        ("What is the complete workflow for lateral movement?",           "lateral"),
        ("Walk me through credential attacks step by step",               "creds"),
    ],
    "lazyown_bridge_suggest": [
        ("Suggest the best command for SMB enumeration in the recon phase", "recon smb enum"),
        ("What command should I run for privilege escalation on Linux?",    "privesc linux"),
        ("Best command to exploit a web app after finding SQL injection",   "exploit web sqli"),
        ("Recommend a command for lateral movement using captured creds",   "lateral creds"),
        ("Which LazyOwn command handles Kerberoasting?",                    "exploit kerberoasting"),
        ("Best tool for AD enumeration with valid credentials",             "enum ad creds"),
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
    ],
    "lazyown_auto_populate": [
        ("Auto-populate the configuration from the nmap scan",            ""),
        ("Parse nmap XML and fill payload.json automatically",            ""),
        ("Extract services from nmap and configure LazyOwn",              ""),
        ("Auto-fill domain and OS from the scan results",                 ""),
        ("Rellena automáticamente la configuración desde el escaneo",     ""),
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
    ],
    "lazyown_session_state": [
        ("What is the current session state?",                            ""),
        ("Show active phase and discovered hosts",                        ""),
        ("Give me the aggregated session context",                        ""),
        ("What ports and creds have been found so far?",                  ""),
        ("Estado actual de la sesión",                                    ""),
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
    ],
    "lazyown_list_targets": [
        ("List all targets in scope",                                     ""),
        ("Show tracked targets with their ports",                         ""),
        ("What hosts are in our target list?",                            ""),
        ("Display all registered targets",                                ""),
        ("¿Qué objetivos tenemos en el scope?",                           ""),
        ("Show all targets and their discovery status",                   ""),
    ],
    "lazyown_set_active_target": [
        ("Set 10.10.11.78 as the active target",                          "10.10.11.78"),
        ("Switch focus to 192.168.1.100",                                 "192.168.1.100"),
        ("Make 10.10.11.1 the current target",                            "10.10.11.1"),
        ("Activate target 10.10.11.78",                                   "10.10.11.78"),
        ("Cambia al objetivo 10.10.10.5",                                 "10.10.10.5"),
    ],

    # ── C2 / Sessions ────────────────────────────────────────────────────────
    "lazyown_get_beacons": [
        ("List all connected beacons",                                    ""),
        ("Show active implants on the C2",                                ""),
        ("What beacons are checking in?",                                 ""),
        ("Get connected agents from C2 server",                          ""),
        ("¿Qué implantes están activos?",                                 ""),
        ("Display beacon status",                                         ""),
    ],
    "lazyown_c2_command": [
        ("Send whoami to all beacons",                                    "whoami"),
        ("Task the beacon to run ipconfig",                               "ipconfig"),
        ("Issue hostname command to connected implants",                  "hostname"),
        ("Run 'net user' on the compromised host via beacon",             "net user"),
        ("Tasking: execute 'cat /etc/passwd' on Linux beacon",           "cat /etc/passwd"),
        ("Send 'systeminfo' to Windows beacon",                           "systeminfo"),
        ("Task beacon to dump local user hashes",                         "hashdump"),
    ],
    "lazyown_c2_status": [
        ("Is the C2 server running?",                                     ""),
        ("Check C2 server health",                                        ""),
        ("C2 dashboard status",                                           ""),
        ("Is the command and control infrastructure up?",                 ""),
        ("¿Está funcionando el servidor C2?",                             ""),
    ],
    "lazyown_run_api": [
        ("Run 'id' on the C2 host via REST API",                          "id"),
        ("Execute 'uname -a' through the C2 API",                        "uname -a"),
        ("Call the LazyOwn API to run a command",                        "whoami"),
        ("Use the REST API to check running processes",                   "ps aux"),
    ],
    "lazyown_list_sessions": [
        ("List all session files",                                        ""),
        ("Show captured data in sessions/",                               ""),
        ("What files are in the sessions directory?",                     ""),
        ("List exfiltrated data and logs",                                ""),
        ("¿Qué hay en la carpeta sessions?",                              ""),
    ],
    "lazyown_read_session_file": [
        ("Read the credentials.txt session file",                         "credentials.txt"),
        ("Show contents of nmap scan results",                            "scan_10.10.11.78.nmap"),
        ("Read the latest session log",                                   "session.log"),
        ("Open the captured hash file",                                   "hashes.txt"),
        ("Read the exfiltrated /etc/passwd",                              "etc_passwd.txt"),
    ],
    "lazyown_c2_profile": [
        ("List available C2 profiles",                                    "list"),
        ("Show the current malleable C2 profile",                         "show"),
        ("Set C2 beacon sleep to 30 seconds",                             "set sleep=30"),
        ("Which C2 profiles are available?",                              "list"),
    ],

    # ── Modules / plugins ────────────────────────────────────────────────────
    "lazyown_list_modules": [
        ("List all LazyOwn modules",                                      ""),
        ("What scripts are available in modules/?",                       ""),
        ("Show available exploit modules",                                ""),
        ("¿Qué módulos tiene LazyOwn?",                                   ""),
        ("Display all LazyOwn tools and scripts",                        ""),
    ],
    "lazyown_list_addons": [
        ("List all installed addons",                                     ""),
        ("What addons are available in LazyOwn?",                        ""),
        ("Show enabled addons",                                           ""),
        ("¿Qué addons hay disponibles?",                                  ""),
    ],
    "lazyown_list_plugins": [
        ("List all Lua plugins",                                          ""),
        ("Show available LazyOwn plugins",                                ""),
        ("What Lua scripts are installed?",                               ""),
        ("¿Qué plugins están disponibles?",                               ""),
    ],
    "lazyown_create_addon": [
        ("Create a new addon for impacket from GitHub",                   "https://github.com/fortra/impacket.git"),
        ("Add a new addon for Certipy",                                   "https://github.com/ly4k/Certipy.git"),
        ("Create addon for Responder tool",                               "https://github.com/lgandx/Responder.git"),
        ("Integrate a new tool from GitHub into LazyOwn",                 "https://github.com/user/tool.git"),
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
    ],
    "lazyown_c2_redop": [
        ("Plan a full red team operation on 10.10.11.78",                 "full compromise 10.10.11.78"),
        ("Create a red team attack plan for the corp.local domain",       "corp.local domain takeover"),
        ("Plan lateral movement after initial access",                    "lateral movement post-access"),
        ("Design a full attack chain for Active Directory",               "AD full compromise"),
        ("Create operation plan: from recon to domain admin",             "recon to domain admin"),
    ],
    "lazyown_c2_adversary": [
        ("Emulate APT29 adversary techniques",                            "APT29"),
        ("Simulate Lazarus Group TTPs",                                   "Lazarus Group"),
        ("Run MITRE ATT&CK technique T1003 (credential dumping)",         "T1003"),
        ("Emulate ransomware operator TTPs",                              "ransomware operator"),
        ("Apply FIN7 adversary playbook",                                 "FIN7"),
    ],
    "lazyown_c2_script": [
        ("Generate a SMB relay exploit script",                           "SMB relay attack"),
        ("Write a PowerShell privilege escalation script",                "PowerShell privesc"),
        ("Generate a Python reverse shell",                               "Python reverse shell"),
        ("Create a Kerberoasting script",                                 "Kerberoasting extraction"),
        ("Write a DCSync script using impacket",                          "DCSync impacket"),
    ],
    "lazyown_threat_model": [
        ("Build a threat model for the current session",                  ""),
        ("Generate MITRE ATT&CK threat model",                           ""),
        ("Map discovered TTPs to MITRE framework",                        ""),
        ("Create threat model from session data",                         ""),
        ("¿Cuál es el modelo de amenazas del engagement?",               ""),
    ],
    "lazyown_playbook_generate": [
        ("Generate an attack playbook for 10.10.11.78",                   "10.10.11.78"),
        ("Create MITRE ATT&CK grounded playbook",                         "10.10.11.78"),
        ("Build playbook for domain compromise",                          "corp.local"),
        ("Generate pentest playbook for target",                          "10.10.11.78"),
    ],
    "lazyown_playbook_run": [
        ("Execute the generated playbook",                                "playbook_10.10.11.78.yaml"),
        ("Run the attack playbook step by step",                          "playbook_corp.local.yaml"),
        ("Start playbook execution",                                      "playbook.yaml"),
    ],
    "lazyown_cve_search": [
        ("Search CVEs for Apache 2.4.49",                                 "apache 2.4.49"),
        ("Find vulnerabilities in OpenSSH 7.4",                          "openssh 7.4"),
        ("CVE lookup for vsftpd 2.3.4",                                   "vsftpd 2.3.4"),
        ("What CVEs affect Samba 4.13?",                                  "samba 4.13"),
        ("Search NVD for Windows 10 vulnerabilities",                     "windows 10"),
        ("Busca CVEs para log4j 2.14",                                    "log4j 2.14"),
    ],
    "lazyown_searchsploit": [
        ("Search for vsftpd 2.3.4 exploits",                             "vsftpd 2.3.4"),
        ("Find Metasploit modules for EternalBlue",                       "EternalBlue MS17-010"),
        ("Search exploits for Apache Struts",                             "Apache Struts"),
        ("Look up exploits for Rejetto HFS 2.3",                         "Rejetto HFS 2.3"),
        ("Find exploits for MySQL 5.5",                                   "MySQL 5.5"),
        ("Busca exploits para PHP 5.2",                                   "PHP 5.2"),
        ("Search for SMB exploits in MSF",                                "SMB Windows"),
    ],
    "lazyown_llm_ask": [
        ("Ask the LLM how to escalate privileges on Linux",               "how to escalate privileges on Linux"),
        ("Use AI to plan the attack on this Windows host",                "plan attack Windows host"),
        ("Ask the LLM to analyze the target's attack surface",           "analyze attack surface 10.10.11.78"),
        ("LLM: how to extract credentials from LSASS?",                  "extract credentials LSASS"),
        ("Pregunta al LLM cómo hacer pass-the-hash",                     "pass-the-hash NTLM"),
        ("Ask AI to reason about the best lateral movement technique",    "best lateral movement technique"),
    ],

    # ── Memory / RAG ─────────────────────────────────────────────────────────
    "lazyown_rag_index": [
        ("Index all session files into the knowledge base",               ""),
        ("Update the RAG index with new session data",                    ""),
        ("Incrementally index sessions/ into ChromaDB",                   ""),
        ("Re-index all captured data",                                    ""),
    ],
    "lazyown_rag_query": [
        ("Search session data for SMB credentials",                       "SMB credentials"),
        ("Find past nmap results for 10.10.11.78",                       "nmap scan 10.10.11.78"),
        ("Query memory for previous privilege escalation attempts",       "privilege escalation"),
        ("What do we know about domain controllers?",                     "domain controller"),
        ("Search for captured NTLM hashes",                               "NTLM hashes"),
        ("Find any previous findings on port 445",                        "port 445 SMB"),
    ],
    "lazyown_memory_recall": [
        ("Recall past commands run against 10.10.11.78",                  "10.10.11.78"),
        ("What commands have been executed previously?",                  "previous commands"),
        ("Show episodic memory for nmap scans",                           "nmap"),
        ("Recall credential dumping results",                             "credential dumping"),
    ],
    "lazyown_memory_store": [
        ("Save this nmap result to episodic memory",                      "nmap -sV 10.10.11.78 → ports 22,80,443"),
        ("Store the discovered SMB credentials",                          "Found credentials admin:Password123"),
        ("Add this finding to memory: RCE via log4j",                    "RCE via log4j on 10.10.11.78"),
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
    ],
    "lazyown_c2_notes": [
        ("Add a note: found SMB signing disabled",                        "Found SMB signing disabled on 10.10.11.78"),
        ("Read the operational notes",                                    ""),
        ("Append to notes: domain admin achieved",                       "Domain admin achieved via DCSync"),
        ("Show all operator notes",                                       ""),
        ("Clear old notes",                                               "clear"),
    ],
    "lazyown_credentials": [
        ("Show all captured credentials",                                 ""),
        ("List all found passwords and hashes",                           ""),
        ("What credentials have been collected?",                         ""),
        ("Display the credential dump",                                   ""),
        ("¿Qué credenciales hemos capturado?",                           ""),
        ("Show NTLM hashes from the session",                             ""),
        ("List all found usernames and passwords",                        ""),
    ],
    "lazyown_report_update": [
        ("Update the pentest report with new findings",                   "RCE via log4j on 10.10.11.78:8080"),
        ("Add domain admin finding to the report",                        "Achieved domain admin via DCSync"),
        ("Write up the credential dumping finding",                       "Dumped NTLM hashes via secretsdump"),
        ("Update report: found EternalBlue vulnerable host",              "MS17-010 vulnerable: 10.10.11.78"),
        ("Add SMB relay attack to report",                               "SMB relay → NTLM capture"),
    ],
    "lazyown_campaign_lessons": [
        ("Show lessons learned from this campaign",                       ""),
        ("What tactical insights were captured?",                         ""),
        ("Read the campaign lessons",                                     ""),
        ("Show retrospective findings",                                   ""),
        ("¿Qué lecciones aprendimos en esta campaña?",                   ""),
    ],
    "lazyown_timeline": [
        ("Generate the attack timeline",                                  ""),
        ("Show the red team timeline narrative",                          ""),
        ("Create a chronological account of the attack",                  ""),
        ("Timeline of the engagement",                                    ""),
        ("¿Cuál es la línea de tiempo del ataque?",                      ""),
    ],
    "lazyown_generate_report": [
        ("Auto-generate the pentest report",                              ""),
        ("Generate a full Markdown pentest report",                       ""),
        ("Create report from session artefacts",                          ""),
        ("Build the final engagement report",                             ""),
    ],
    "lazyown_misp_export": [
        ("Export findings as a MISP event",                               ""),
        ("Generate MISP-compatible threat intelligence",                  ""),
        ("Export IoCs and TTPs to MISP format",                           ""),
    ],
    "lazyown_eval_quality": [
        ("Show LLM decision quality report",                              ""),
        ("How accurate has the AI routing been?",                         ""),
        ("Display success rate and MITRE tactic coverage",                ""),
        ("Evaluate the quality of previous AI decisions",                 ""),
    ],
    "lazyown_collab_publish": [
        ("Broadcast: found domain admin credentials",                     "Found domain admin credentials"),
        ("Share finding with all operators: RCE on port 8080",           "RCE found on port 8080"),
        ("Publish alert: EternalBlue vulnerable host discovered",         "EternalBlue vulnerable: 10.10.11.78"),
        ("Send finding to team: NTLM hashes captured",                   "NTLM hashes captured from 10.10.11.78"),
    ],

    # ── Events / policy ──────────────────────────────────────────────────────
    "lazyown_poll_events": [
        ("Check for new security events",                                 ""),
        ("Poll the event engine for alerts",                              ""),
        ("Are there any pending events?",                                 ""),
        ("Show latest detection events",                                  ""),
        ("¿Hay eventos nuevos de detección?",                             ""),
    ],
    "lazyown_ack_event": [
        ("Acknowledge event evt_001",                                     "evt_001"),
        ("Mark event 42 as processed",                                    "42"),
        ("Dismiss the RCE alert",                                         "evt_rce_001"),
    ],
    "lazyown_add_rule": [
        ("Add detection rule for RCE events",                             "pattern=shell event_type=critical"),
        ("Create rule: trigger alert on privilege escalation commands",   "pattern=sudo event_type=high"),
        ("Add event rule for credential access",                          "pattern=mimikatz event_type=critical"),
        ("Create detection for lateral movement",                         "pattern=psexec event_type=high"),
    ],
    "lazyown_list_event_rules": [
        ("List all detection rules",                                      ""),
        ("Show active event rules",                                       ""),
        ("What detection rules are configured?",                          ""),
        ("Display all event detection policies",                          ""),
    ],
    "lazyown_heartbeat_status": [
        ("Is the LazyOwn heartbeat running?",                             ""),
        ("Check if the heartbeat process is alive",                       ""),
        ("Heartbeat health check",                                        ""),
        ("Is the event engine online?",                                   ""),
    ],
    "lazyown_policy_status": [
        ("Show policy engine status",                                     ""),
        ("What is the current policy reward summary?",                    ""),
        ("Display rules of engagement compliance",                        ""),
        ("Policy engine: next recommended actions",                       ""),
        ("¿Cuál es el estado de la política de ataque?",                 ""),
    ],

    # ── Automation ───────────────────────────────────────────────────────────
    "lazyown_auto_loop": [
        ("Start the autonomous attack loop on 10.10.11.78",               "10.10.11.78"),
        ("Begin automated enumeration and exploitation",                  "10.10.11.78"),
        ("Run the auto-loop until domain admin is achieved",              "10.10.11.78"),
        ("Start continuous automated attack",                             "10.10.11.78"),
        ("Inicia el bucle de ataque automático",                          "10.10.11.78"),
    ],
    "lazyown_inject_objective": [
        ("Inject objective: achieve domain admin",                        "achieve domain admin on corp.local"),
        ("Add new objective: exfiltrate /etc/shadow",                     "exfiltrate /etc/shadow"),
        ("Inject goal: find and exploit SQLi on web app",                "find and exploit SQL injection"),
        ("New objective: dump all NTLM hashes",                           "dump all NTLM hashes"),
        ("Inyecta objetivo: escalar privilegios a root",                  "escalate privileges to root"),
    ],
    "lazyown_next_objective": [
        ("What is the next objective to work on?",                        ""),
        ("Show the current frontier-model context",                       ""),
        ("Get the next pending attack objective",                         ""),
        ("What objective should be tackled next?",                        ""),
        ("¿Cuál es el próximo objetivo?",                                 ""),
    ],
    "lazyown_read_prompt": [
        ("Read the LazyOwn developer reference",                          ""),
        ("Show the LazyOwn architecture reference",                       ""),
        ("Load the prompt.md documentation",                              ""),
        ("Get the full tool and command reference",                       ""),
    ],
    "lazyown_soul": [
        ("Read the agent soul and campaign objectives",                   ""),
        ("Show the agent persona and priorities",                         ""),
        ("Update agent soul with new campaign objective",                 "achieve stealth domain admin"),
        ("What are the hard stops in the soul file?",                     ""),
        ("¿Cuál es el alma del agente?",                                  ""),
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
    ],
    "lazyown_agent_status": [
        ("Check the status of agent agent_001",                           "agent_001"),
        ("Is the running agent done?",                                    ""),
        ("Show agent progress and current action",                        ""),
        ("How many iterations has the agent completed?",                  ""),
        ("¿Cómo va el agente autónomo?",                                  ""),
    ],
    "lazyown_agent_result": [
        ("Get the result from agent agent_001",                           "agent_001"),
        ("Read the agent's final answer",                                 ""),
        ("Show what the agent discovered",                                ""),
        ("Agent output: what did it find?",                               ""),
    ],
    "lazyown_list_agents": [
        ("List all running and completed agents",                         ""),
        ("Show recent sub-agents",                                        ""),
        ("What agents are active?",                                       ""),
        ("¿Qué agentes están corriendo?",                                 ""),
    ],
    "lazyown_groq_agent": [
        ("Spawn a Groq agent for Active Directory enumeration",           "enumerate Active Directory"),
        ("Run a Groq agent with all LazyOwn tools",                       "full recon and exploit 10.10.11.78"),
        ("Start Ollama agent for privilege escalation",                   "find and exploit privesc paths"),
        ("Launch Groq agent to enumerate SMB shares",                     "enumerate SMB shares on 10.10.11.78"),
    ],

    # ── Hive mind ────────────────────────────────────────────────────────────
    "lazyown_hive_spawn": [
        ("Spawn 3 drones to enumerate SMB on 10.10.11.78",               "enumerate SMB shares on 10.10.11.78"),
        ("Spawn parallel drones for full AD enumeration",                 "full Active Directory enumeration"),
        ("Spawn recon and exploit drones in parallel",                    "recon and exploit 10.10.11.78"),
        ("Create a hive with 5 drones for domain compromise",             "domain compromise corp.local"),
        ("Spawn drones: recon, creds, lateral movement",                  "parallel pentest 10.10.11.78"),
        ("Use the hive to enumerate all services in parallel",            "enumerate all services on 10.10.11.78"),
    ],
    "lazyown_hive_status": [
        ("Show hive-mind status",                                         ""),
        ("How many drones are active?",                                   ""),
        ("Hive status: drones and memory",                                ""),
        ("What is the queen doing?",                                      ""),
        ("¿Cuál es el estado de la mente colmena?",                      ""),
    ],
    "lazyown_hive_recall": [
        ("Search hive memory for domain admin credentials",               "domain admin credentials"),
        ("Recall all drone results about SMB",                            "SMB enumeration"),
        ("Hive memory: what do we know about the DC?",                    "domain controller"),
        ("Search drone findings for NTLM hashes",                        "NTLM hashes"),
    ],
    "lazyown_hive_plan": [
        ("Plan a domain compromise without spawning drones",              "full domain compromise"),
        ("Decompose AD enumeration into drone tasks",                     "Active Directory enumeration"),
        ("Plan the attack: recon → exploit → privesc → lateral",         "full attack chain"),
        ("Generate task decomposition for this engagement",               "10.10.11.78 pentest"),
    ],
    "lazyown_hive_result": [
        ("Get drone_001 result",                                          "drone_001"),
        ("Read the output from drone 2",                                  "drone_002"),
        ("Show what the recon drone found",                               "drone_recon_001"),
    ],
    "lazyown_hive_collect": [
        ("Wait for drones and summarize results",                         "drone_001,drone_002"),
        ("Collect and synthesize all drone outputs",                      "drone_001,drone_002,drone_003"),
        ("Queen: summarize what the drones found",                        "drone_001,drone_002"),
    ],
    "lazyown_hive_forget": [
        ("Prune hive memory older than 24 hours",                         "24"),
        ("Clear old drone results from memory",                           "48"),
        ("Forget hive memory about the test environment",                 "72"),
    ],
    "lazyown_hive_recover": [
        ("Recover interrupted hive drones",                               ""),
        ("Re-queue drones after crash",                                   ""),
        ("Restore hive state after restart",                              ""),
    ],

    # ── Autonomous daemon ────────────────────────────────────────────────────
    "lazyown_autonomous_start": [
        ("Start autonomous mode targeting 10.10.11.78",                   "achieve domain admin on 10.10.11.78"),
        ("Begin fully autonomous attack on corp.local",                   "compromise corp.local domain"),
        ("Start the autonomous daemon with objective: get root",          "escalate to root on 10.10.11.78"),
        ("Run autonomous agent to find and exploit vulnerabilities",      "find and exploit all vulns on 10.10.11.78"),
        ("Inicia el daemon autónomo para comprometer el objetivo",        "comprometer 10.10.11.78"),
    ],
    "lazyown_autonomous_stop": [
        ("Stop the autonomous daemon",                                    ""),
        ("Halt the autonomous attack loop",                               ""),
        ("Stop automated exploitation",                                   ""),
        ("¡Para el daemon autónomo!",                                     ""),
    ],
    "lazyown_autonomous_status": [
        ("What is the autonomous daemon doing?",                          ""),
        ("Autonomous daemon status",                                      ""),
        ("How many steps has the daemon completed?",                      ""),
        ("Show the current autonomous objective",                         ""),
        ("¿Cómo va el daemon autónomo?",                                  ""),
    ],
    "lazyown_autonomous_inject": [
        ("Inject new objective into autonomous daemon: dump credentials", "dump all credentials from 10.10.11.78"),
        ("Add objective to daemon: exfiltrate sensitive files",           "exfiltrate /etc/shadow"),
        ("Tell the daemon to focus on lateral movement now",              "perform lateral movement to 10.10.11.100"),
    ],
    "lazyown_autonomous_events": [
        ("Show the last 20 autonomous events",                            "20"),
        ("Read the autonomous event stream",                              ""),
        ("Show recent daemon activity",                                   ""),
        ("What has the autonomous daemon done so far?",                   ""),
    ],

    # ── Tools / objectives ───────────────────────────────────────────────────
    "lazyown_create_tool": [
        ("Create a pwntomate tool for vsftpd 2.3.4",                      "vsftpd 2.3.4"),
        ("Add a tool file for automatic Apache exploit",                  "apache 2.4.49"),
        ("Create a pwntomate rule for SMB vulnerabilities",               "SMB Windows"),
        ("New tool file for MySQL 5.5 exploitation",                      "mysql 5.5"),
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


def build_dataset() -> List[Dict]:
    records: List[Dict] = []

    for (tool_name, desc, category, _default_arg) in _TOOLS:
        phrasings = _PHRASINGS.get(tool_name, [])
        if not phrasings:
            continue
        for instruction, arg in phrasings:
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
