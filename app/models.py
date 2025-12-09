from typing import Dict, Any, List, Optional
from pydantic import BaseModel


class GraphCreateRequest(BaseModel):
    nodes: List[str]
    edges: Dict[str, Optional[str]]  # e.g. {"split_text": "generate_summaries", ...}
    start_node: str


class GraphCreateResponse(BaseModel):
    graph_id: str


class GraphRunRequest(BaseModel):
    graph_id: str
    initial_state: Dict[str, Any]


class ExecutionStep(BaseModel):
    step: int
    node: str
    state_snapshot: Dict[str, Any]


class GraphRunResponse(BaseModel):
    run_id: str
    final_state: Dict[str, Any]
    log: List[ExecutionStep]


class GraphStateResponse(BaseModel):
    run_id: str
    graph_id: str
    status: str
    state: Dict[str, Any]
    log: List[ExecutionStep]
