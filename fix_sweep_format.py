#!/usr/bin/env python3
"""Convert existing sweep data to correct training format."""
import json
from pathlib import Path

in_path = Path("data_toolbench/lazyown_sweep.jsonl")
out_path = Path("data_toolbench/lazyown_sweep_fixed.jsonl")

if not in_path.exists():
    print(f"[fix] {in_path} not found")
    exit(1)

fixed = []
with in_path.open("r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            old = json.loads(line)
            # Parse the old answer JSON
            ans = json.loads(old["answer"])
            tool_name = ans["tool"]
            tool_arg = ans["arg"].replace("\n", " ")[:80]
            
            record = {
                "instruction": old["instruction"],
                "api_list": [
                    {
                        "tool_name": tool_name,
                        "api_name": f"{tool_name}_endpoint",
                        "api_description": f"LazyOwn {tool_name} tool",
                        "required_parameters": [{"name": "arg", "type": "STRING", "description": "tool argument"}],
                        "optional_parameters": [],
                    }
                ],
                "answer": f"[TOOL_CALL: {tool_name}({tool_arg})] [result captured during pentest]",
                "domain": old.get("domain", "Security/RealSuccess"),
            }
            fixed.append(record)
        except Exception as exc:
            print(f"[fix] Skip bad line: {exc}")

with out_path.open("w", encoding="utf-8") as f:
    for r in fixed:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

print(f"[fix] Converted {len(fixed)} records → {out_path}")
print(f"[fix] Sample: {json.dumps(fixed[0], indent=2, ensure_ascii=False)[:200]}")
