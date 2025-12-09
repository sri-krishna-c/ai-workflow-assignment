from __future__ import annotations
from typing import Callable, Dict, Any, List, Optional
from dataclasses import dataclass

NodeFunc = Callable[[Dict[str, Any], "ToolRegistry"], Dict[str, Any]]


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: Dict[str, Callable[..., Any]] = {}

    def register(self, name: str, func: Callable[..., Any]) -> None:
        self._tools[name] = func

    def get(self, name: str) -> Callable[..., Any]:
        if name not in self._tools:
            raise KeyError(f"Tool '{name}' not found")
        return self._tools[name]

    def list_tools(self) -> List[str]:
        return list(self._tools.keys())


@dataclass
class Graph:
    nodes: Dict[str, NodeFunc]
    edges: Dict[str, Optional[str]]
    start_node: str


@dataclass
class RunResult:
    final_state: Dict[str, Any]
    log: List[Dict[str, Any]]


class GraphEngine:
    def __init__(self, tool_registry: ToolRegistry, max_steps: int = 100) -> None:
        self.tool_registry = tool_registry
        self.max_steps = max_steps

    def run(self, graph: Graph, initial_state: Dict[str, Any]) -> RunResult:
        state: Dict[str, Any] = dict(initial_state)
        log: List[Dict[str, Any]] = []

        current_node = graph.start_node
        step = 0

        while current_node is not None and step < self.max_steps:
            if current_node not in graph.nodes:
                raise ValueError(f"Node '{current_node}' not defined in graph")

            node_func = graph.nodes[current_node]

            new_state = node_func(state, self.tool_registry)

            explicit_next = new_state.pop("__next__", None)

            state = new_state

            log.append({
                "step": step,
                "node": current_node,
                "state_snapshot": dict(state),
            })

            if explicit_next is not None:
                current_node = explicit_next
            else:
                current_node = graph.edges.get(current_node)

            step += 1

        return RunResult(final_state=state, log=log)
