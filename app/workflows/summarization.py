# Makes 'app' a Python package
from __future__ import annotations
from typing import Dict, Any, List

from ..graph_engine import ToolRegistry, NodeFunc


def tool_split_text(text: str, chunk_size: int = 50) -> List[str]:
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks


def tool_summarize_chunk(chunk: str) -> str:
    words = chunk.split()
    if len(words) <= 20:
        return chunk
    return " ".join(words[:20]) + " ..."


def tool_merge_summaries(summaries: List[str]) -> str:
    return " ".join(summaries)


def tool_refine_summary(summary: str, max_words: int = 60) -> str:
    words = summary.split()
    if len(words) <= max_words:
        return summary
    return " ".join(words[:max_words]) + " ..."


def node_split_text(state: Dict[str, Any], tools: ToolRegistry) -> Dict[str, Any]:
    text = state.get("text", "")
    chunk_size = state.get("chunk_size", 50)
    split_tool = tools.get("split_text")
    chunks = split_tool(text, chunk_size=chunk_size)
    state = dict(state)
    state["chunks"] = chunks
    return state


def node_generate_summaries(state: Dict[str, Any], tools: ToolRegistry) -> Dict[str, Any]:
    chunks = state.get("chunks", [])
    summarize_tool = tools.get("summarize_chunk")
    summaries = [summarize_tool(chunk) for chunk in chunks]
    state = dict(state)
    state["summaries"] = summaries
    return state


def node_merge_summaries(state: Dict[str, Any], tools: ToolRegistry) -> Dict[str, Any]:
    summaries = state.get("summaries", [])
    merge_tool = tools.get("merge_summaries")
    merged = merge_tool(summaries)
    state = dict(state)
    state["merged_summary"] = merged
    state["summary"] = merged
    return state


def node_refine_summary(state: Dict[str, Any], tools: ToolRegistry) -> Dict[str, Any]:
    summary = state.get("summary", "")
    max_words = state.get("max_summary_words", 60)
    iteration = state.get("refine_iteration", 0)

    refine_tool = tools.get("refine_summary")
    refined = refine_tool(summary, max_words=max_words)

    state = dict(state)
    state["summary"] = refined
    state["refine_iteration"] = iteration + 1

    if len(refined.split()) > max_words and state["refine_iteration"] < state.get("max_refine_loops", 5):
        state["__next__"] = "refine_summary"

    return state


def register_summarization_tools(tool_registry: ToolRegistry) -> None:
    tool_registry.register("split_text", tool_split_text)
    tool_registry.register("summarize_chunk", tool_summarize_chunk)
    tool_registry.register("merge_summaries", tool_merge_summaries)
    tool_registry.register("refine_summary", tool_refine_summary)


def get_summarization_nodes() -> Dict[str, NodeFunc]:
    return {
        "split_text": node_split_text,
        "generate_summaries": node_generate_summaries,
        "merge_summaries": node_merge_summaries,
        "refine_summary": node_refine_summary,
    }
