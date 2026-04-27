# TopoSwarm — Operator Guide

You are operating the **TopoSwarm** AI router wired to the **LazyOwn** pentesting framework.

TopoSwarm routes natural-language security goals to the correct LazyOwn tool automatically using a trained quaternionic swarm model. You never need to guess tool names — just describe what you want to do.

---

## STEP 0 — Start every session with a SITREP

```python
toposwarm_query(prompt="generate a campaign sitrep")
# routes → lazyown_campaign_sitrep()
```

---

## Core workflow

### 1. Set target
```python
toposwarm_query(prompt="set target host to 10.10.11.78")
# routes → lazyown_set_config(rhost=10.10.11.78)
```

### 2. Reconnaissance
```python
toposwarm_query(prompt="scan for open ports on 10.10.11.78")
# routes → lazyown_run_command(set rhost 10.10.11.78 \n lazynmap)
```

### 3. Vulnerability analysis
```python
toposwarm_query(prompt="analyze vulnerabilities on 10.10.11.78")
# routes → lazyown_c2_vuln_analysis(10.10.11.78)
```

### 4. Next step recommendation
```python
toposwarm_query(prompt="what should be the next step after initial access?")
# routes → lazyown_recommend_next()
```

### 5. Check credentials
```python
toposwarm_query(prompt="show collected credentials")
# routes → lazyown_credentials()
```

---

## Routing table — natural language → tool

| Say this… | Gets routed to |
|---|---|
| `scan / nmap / enumerate <ip>` | `lazyown_run_command` |
| `set rhost / lhost / lport` | `lazyown_set_config` |
| `show / get config` | `lazyown_get_config` |
| `list modules` | `lazyown_list_modules` |
| `beacons / implants` | `lazyown_get_beacons` |
| `sessions / active sessions` | `lazyown_list_sessions` |
| `c2 status` | `lazyown_c2_status` |
| `add target <ip>` | `lazyown_add_target` |
| `list targets` | `lazyown_list_targets` |
| `vuln / vulnerability / CVE` | `lazyown_c2_vuln_analysis` |
| `search / MITRE / technique` | `lazyown_c2_search_agent` |
| `sitrep / campaign status` | `lazyown_campaign_sitrep` |
| `credentials / creds / loot` | `lazyown_credentials` |
| `recommend / next step` | `lazyown_recommend_next` |
| `report / write report` | `lazyown_report_update` |
| `timeline` | `lazyown_timeline` |
| `ask llm / ask ai` | `lazyown_llm_ask` |
| `run agent / groq / ollama` | `lazyown_run_agent` |
| `adversary / APT / TTP` | `lazyown_c2_adversary` |
| `red op / red team plan` | `lazyown_c2_redop` |

---

## Direct tool access

You can also call any LazyOwn tool directly without going through the NL router:

```python
lazyown_run_command(arg="lazynmap")
lazyown_set_config(arg="rhost=10.10.11.78")
lazyown_c2_vuln_analysis(arg="10.10.11.78")
lazyown_credentials(arg="")
lazyown_campaign_sitrep(arg="")
```

---

## Fine-tuning the router

If the router misroutes a prompt, add it to `_LAZYOWN_TRACES` in `toposwarm_lazyown_orchestrator.py` and run:

```bash
python toposwarm_lazyown_orchestrator.py --gen-dataset
python toposwarm_lazyown_orchestrator.py --finetune
```

---

## Rules of engagement

- Always call `toposwarm_query(prompt="sitrep")` before starting work
- Never run scans against targets not in the approved scope (`lazyown_list_targets`)
- Check `lazyown_policy_status()` before any offensive action
- Log all findings with `lazyown_report_update()`
