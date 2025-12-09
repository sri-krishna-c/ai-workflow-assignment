from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .graph_engine import GraphEngine, ToolRegistry, Graph
from .store import InMemoryStore
from .models import (
    GraphCreateRequest,
    GraphCreateResponse,
    GraphRunRequest,
    GraphRunResponse,
    GraphStateResponse,
    ExecutionStep,
)
from .workflows.summarization import (
    register_summarization_tools,
    get_summarization_nodes,
)


app = FastAPI(title="Minimal Agent Workflow Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

tool_registry = ToolRegistry()
store = InMemoryStore()
engine = GraphEngine(tool_registry=tool_registry)

register_summarization_tools(tool_registry)


@app.post("/graph/create", response_model=GraphCreateResponse)
async def create_graph(payload: GraphCreateRequest):
    available_nodes = get_summarization_nodes()

    for node_name in payload.nodes:
        if node_name not in available_nodes:
            raise HTTPException(
                status_code=400,
                detail=f"Node '{node_name}' is not a supported node for this demo.",
            )

    graph = Graph(
        nodes={name: available_nodes[name] for name in payload.nodes},
        edges=payload.edges,
        start_node=payload.start_node,
    )

    graph_id = store.create_graph(graph)
    return GraphCreateResponse(graph_id=graph_id)


@app.post("/graph/run", response_model=GraphRunResponse)
async def run_graph(payload: GraphRunRequest):
    try:
        graph = store.get_graph(payload.graph_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Graph not found")

    run_record = store.create_run(payload.graph_id, payload.initial_state)

    try:
        result = engine.run(graph, payload.initial_state)
        status = "completed"
    except Exception as e:
        status = "failed"
        result = type("Tmp", (), {})()
        result.final_state = {"error": str(e)}
        result.log = []

    store.update_run(
        run_record.run_id,
        status=status,
        state=result.final_state,
        log=result.log,
    )

    log_models = [
        ExecutionStep(
            step=entry["step"],
            node=entry["node"],
            state_snapshot=entry["state_snapshot"],
        )
        for entry in result.log
    ]

    return GraphRunResponse(
        run_id=run_record.run_id,
        final_state=result.final_state,
        log=log_models,
    )


@app.get("/graph/state/{run_id}", response_model=GraphStateResponse)
async def get_run_state(run_id: str):
    try:
        run = store.get_run(run_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Run not found")

    log_models = [
        ExecutionStep(
            step=entry["step"],
            node=entry["node"],
            state_snapshot=entry["state_snapshot"],
        )
        for entry in run.log
    ]

    return GraphStateResponse(
        run_id=run.run_id,
        graph_id=run.graph_id,
        status=run.status,
        state=run.state,
        log=log_models,
    )
