import orcapod as op
from pathlib import Path
import asyncio
from .util import print_crash

namespace_lookup = {"default": "../data_lake"}
data_dir = "data"
store_dir = "store"
group = "demo"
host = "alpha"

orch = op.LocalDockerOrchestrator()

store = op.LocalFileStore(directory=f'{Path(namespace_lookup["default"])}/{store_dir}')

client = op.AgentClient(group=group, host=host)
agent = op.Agent(group=group, host=host, orchestrator=orch)

active_agent = asyncio.create_task(
    print_crash(agent.start(namespace_lookup=namespace_lookup, available_store=store))
)
