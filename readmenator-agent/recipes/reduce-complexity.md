# Recipe: Reduce File Complexity

Target hotspot: `topo_swarm_agent.py`
(complexity 0.8, centrality 1.0)

1. Read dependents: `grep -n 'topo_swarm_agent.py' readmenator-agent/ARCHITECTURE*.md`
2. Extract functions/classes into new files in the same subsystem
3. Update imports
4. Regenerate: `readmenator .`
