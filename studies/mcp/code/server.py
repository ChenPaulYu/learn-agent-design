"""Minimal MCP server exposing one of each server-owned primitive: tool, resource, prompt."""

from pathlib import Path

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("mcp-hands-on")

STUDIES_DIR = Path(__file__).resolve().parents[2]


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b


@mcp.tool()
def word_count(text: str) -> int:
    """Count whitespace-separated words in a string."""
    return len(text.split())


@mcp.resource("studies://topics")
def list_topics() -> str:
    """List the study topic folders in this repo."""
    topics = sorted(p.name for p in STUDIES_DIR.iterdir() if p.is_dir())
    return "\n".join(topics)


@mcp.prompt()
def explain_primitive(name: str) -> str:
    """Build a prompt asking to explain one MCP primitive."""
    return f"Explain the MCP primitive '{name}' in one paragraph, with a concrete example."


if __name__ == "__main__":
    mcp.run()
