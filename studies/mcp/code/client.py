"""Minimal MCP client: launches server.py over stdio and exercises each primitive."""

import asyncio
from pathlib import Path

from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

SERVER_SCRIPT = Path(__file__).resolve().parent / "server.py"


async def main() -> None:
    params = StdioServerParameters(command="python", args=[str(SERVER_SCRIPT)])

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("tools:", [t.name for t in tools.tools])

            result = await session.call_tool("add", {"a": 2, "b": 3})
            print("add(2, 3) ->", result.content[0].text)

            resources = await session.list_resources()
            print("resources:", [str(r.uri) for r in resources.resources])

            topics = await session.read_resource("studies://topics")
            print("studies://topics ->", topics.contents[0].text)

            prompts = await session.list_prompts()
            print("prompts:", [p.name for p in prompts.prompts])

            prompt = await session.get_prompt("explain_primitive", {"name": "Sampling"})
            print("explain_primitive(Sampling) ->", prompt.messages[0].content.text)


if __name__ == "__main__":
    asyncio.run(main())
