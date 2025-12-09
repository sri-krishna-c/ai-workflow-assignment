from __future__ import annotations
from typing import Dict, Any, List
from dataclasses import dataclass, field
import uuid

from .graph_engine import Graph


@dataclass
class RunRecord:
    run_id: str
    graph_id: str
    status: str  # "running" | "completed" | "failed"
    state: Dict[str, Any] = field(default_factory=dict)
    log: List[Dict[str, Any]] = field(default_factory=list)


class InMemoryStore:
    def __init__(self) -> None:
        self.graphs: Dict[str, Graph] = {}
        self.runs: Dict[str, RunRecord] = {}

    def create_graph(self, graph: Graph) -> str:
        graph_id = str(uuid.uuid4())
        self.graphs[graph_id] = graph
        return graph_id

    def get_graph(self, graph_id: str) -> Graph:
        if graph_id not in self.graphs:
            raise KeyError(f"Graph '{graph_id}' not found")
        return self.graphs[graph_id]

    def create_run(self, graph_id: str, initial_state: Dict[str, Any]) -> RunRecord:
        run_id = str(uuid.uuid4())
        record = RunRecord(
            run_id=run_id,
            graph_id=graph_id,
            status="running",
            state=initial_state,
            log=[],
        )
        self.runs[run_id] = record
        return record

    def update_run(self, run_id: str, *, status: str, state: Dict[str, Any], log: List[Dict[str, Any]]) -> None:
        if run_id not in self.runs:
            raise KeyError(f"Run '{run_id}' not found")
        self.runs[run_id].status = status
        self.runs[run_id].state = state
        self.runs[run_id].log = log

    def get_run(self, run_id: str) -> RunRecord:
        if run_id not in self.runs:
            raise KeyError(f"Run '{run_id}' not found")
        return self.runs[run_id]
