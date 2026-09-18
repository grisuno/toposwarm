# Recipe: Reduce File Complexity

Target hotspot: `toposwarm_lazyown_orchestrator.py`
(complexity 0.7, centrality 1.0)

1. Read dependents: `grep -n 'toposwarm_lazyown_orchestrator.py' readmenator-agent/ARCHITECTURE.md`
2. Extract functions/classes into new files in the same subsystem
3. Update imports
4. Regenerate: `readmenator .`
