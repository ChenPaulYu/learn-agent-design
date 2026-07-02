# mcp hands-on

Minimal server + client using the official Python `mcp` SDK, over stdio transport. One example
of each server-owned primitive (tool, resource, prompt) — see the note in `../docs/` for what
each one means.

```sh
uv run python client.py
```

`client.py` launches `server.py` as a subprocess and exercises `list_tools` / `call_tool` /
`list_resources` / `read_resource` / `list_prompts` / `get_prompt`.
