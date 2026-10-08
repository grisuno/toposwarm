# Architecture

## Internal Dependencies

- `debug_routing.py` -> `topo_swarm_agent.py`
- `debug_routing.py` -> `ts_utils.py`
- `diagnose_accuracy.py` -> `topo_swarm_agent.py`
- `diagnose_accuracy.py` -> `ts_utils.py`
- `meta_harness_proposer.py` -> `toposwarm_meta_harness.py`
- `tests/test_orchestrator.py` -> `toposwarm_lazyown_orchestrator.py`
- `topo_swarm_agent.py` -> `ts_utils.py`
- `toposwarm_coevolve.py` -> `topo_swarm_agent.py`
- `toposwarm_coevolve.py` -> `toposwarm_infer.py`
- `toposwarm_coevolve.py` -> `toposwarm_lazyown_orchestrator.py`
- `toposwarm_coevolve.py` -> `toposwarm_meta_harness.py`
- `toposwarm_continual_trainer.py` -> `ts_utils.py`
- `toposwarm_lazyown_sweep.py` -> `topo_swarm_agent.py`
- `toposwarm_lazyown_sweep.py` -> `toposwarm_lazyown_orchestrator.py`

## External Imports

- `debug_routing.py` -> json, pathlib, safetensors.torch, sys, torch
- `diagnose_accuracy.py` -> json, pathlib, safetensors.torch, sys, torch
- `fix_sweep_format.py` -> json, pathlib
- `lazyown_bridge.py` -> __future__, dataclasses, enum, fcntl, json, os, pathlib, pty, re, select, shutil, struct, subprocess, termios, time, typing
- `lazyown_dataset_enhancer.py` -> __future__, argparse, json, pathlib, random, re, typing
- `lazyown_dataset_generator.py` -> __future__, argparse, collections, json, pathlib, random, re, typing
- `meta_harness_proposer.py` -> __future__, argparse, dataclasses, json, logging, os, pathlib, py_compile, re, sys, tempfile, time, typing, urllib.request
- `neurologos_tricameral_loss2.7.py` -> PIL, collections, functools, google.colab, kagglehub, numpy, os, pathlib, shutil, soundfile, subprocess, time, torch, torch.nn, torch.nn.functional, torch.utils.data, torchaudio, torchaudio.transforms, torchvision, torchvision.models, tqdm, urllib.request, warnings, zipfile
- `test_full_pipeline.py` -> argparse, json, os, pathlib, subprocess, sys
- `tests/test_dataset_enhancer.py` -> importlib.util, pathlib, sys
- `tests/test_dataset_generator.py` -> importlib.util, pathlib, sys
- `tests/test_model_config.py` -> importlib.util, pathlib, sys
- `tests/test_orchestrator.py` -> importlib, pathlib, pytest, sys, torch, unittest.mock
- `topo_swarm_agent.py` -> __future__, argparse, collections, contextlib, dataclasses, datasets, hashlib, json, logging, math, numpy, os, pathlib, safetensors.torch, sys, threading, tiktoken, time, torch, torch.nn, torch.nn.functional, torch.utils.checkpoint, typing, warnings
- `topogpt2_1.py` -> argparse, collections, dataclasses, datasets, datetime, hashlib, json, logging, math, numpy, os, safetensors.torch, shutil, sys, tiktoken, time, torch, torch.nn, torch.nn.functional, torch.utils.checkpoint, typing, warnings
- `toposwarm_coevolve.py` -> __future__, argparse, copy, dataclasses, importlib.util, json, logging, os, pathlib, random, subprocess, sys, time, typing
- `toposwarm_continual_trainer.py` -> __future__, argparse, dataclasses, importlib.util, json, logging, math, os, pathlib, random, sys, torch, torch.nn, torch.nn.functional, typing
- `toposwarm_hybrid.py` -> __future__, argparse, ast, dataclasses, datetime, importlib.util, inspect, json, langdetect, logging, operator, os, pathlib, re, safetensors.torch, sys, torch, torch.nn.functional, transformers, typing, urllib.parse, urllib.request
- `toposwarm_infer.py` -> __future__, argparse, ast, dataclasses, datetime, importlib.util, json, langdetect, logging, math, operator, os, pathlib, re, sys, torch, torch.nn.functional, types, typing, urllib.error, urllib.parse, urllib.request
- `toposwarm_lazyown_orchestrator.py` -> __future__, argparse, asyncio, dataclasses, importlib.util, json, logging, mcp, mcp.server, mcp.server.stdio, os, pathlib, random, re, subprocess, sys, time, torch, typing
- `toposwarm_lazyown_sweep.py` -> __future__, argparse, json, logging, pathlib, random, subprocess, sys, time, typing
- `toposwarm_meta_harness.py` -> __future__, collections, dataclasses, hashlib, json, logging, math, numpy, os, pathlib, psutil, re, sentence_transformers, shutil, sklearn.feature_extraction.text, sklearn.metrics.pairwise, subprocess, sys, time, typing
- `ts_utils.py` -> __future__, ast, functools, importlib.util, logging, pathlib, sys, typing
