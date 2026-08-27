# Client setup

Travel Animator MCP is a **stdio** server. There is no port and no network auth on the channel
— the OS process boundary is the boundary.

Whichever client you use, log in once first, in your own terminal:

```bash
uvx travel-animator login      # or: travel-animator login
```

The server can't prompt you itself. On a stdio server, stdin is the JSON-RPC channel.

## Claude Code

```bash
claude mcp add travel-animator -e TADA_SOURCE=docs -- uvx --from "travel-animator[mcp]" travel-animator mcp
```

## Claude Desktop

`~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or
`%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "travel-animator": {
      "command": "uvx",
      "args": ["--from", "travel-animator[mcp]", "travel-animator", "mcp"],
      "env": { "TADA_SOURCE": "docs" }
    }
  }
}
```

Restart the app. **If it fails to start, use an absolute path for `command`** — see
[PATH](#the-path-problem) below.

## Cursor

`~/.cursor/mcp.json`, or `.cursor/mcp.json` in a project — same JSON shape as Claude Desktop.

## VS Code

`.vscode/mcp.json`:

```json
{
  "servers": {
    "travel-animator": {
      "type": "stdio",
      "command": "uvx",
      "args": ["--from", "travel-animator[mcp]", "travel-animator", "mcp"],
      "env": { "TADA_SOURCE": "docs" }
    }
  }
}
```

## Codex CLI

`~/.codex/config.toml`:

```toml
[mcp_servers.travel-animator]
command = "uvx"
args = ["--from", "travel-animator[mcp]", "travel-animator", "mcp"]
env = { TADA_SOURCE = "docs" }
```

## Any other stdio client

Command `uvx`, args `--from travel-animator[mcp] travel-animator mcp`, and env
`TADA_SOURCE=docs`. Or install the package and run `travel-animator mcp` directly.

`TADA_SOURCE` tells us which instructions you followed. Optional — delete it if you like.

---

## Pinning the version

`uvx --from "travel-animator[mcp]@latest"` resolves the newest release on every launch. Drop
`@latest`, or pin explicitly, to stay put:

```json
"args": ["--from", "travel-animator[mcp]==1.0.0", "travel-animator", "mcp"]
```

A pip-installed `travel-animator` used directly as `command` is also fixed until you upgrade it.
Note that a CLI command upgrades itself to a newer release after finishing and says so on
stderr; `TADA_AUTO_UPGRADE=0` keeps the notice without installing, `TADA_UPDATE_CHECK=0` turns
off both.

## The PATH problem

Applications launched from Finder, the Dock or the Windows Start menu do **not** inherit your
shell's `PATH`, so `uvx` or `travel-animator` may be invisible to them even though both work in
your terminal. Fix it by giving the absolute path:

```bash
which uvx          # macOS / Linux
where uvx          # Windows
```

```json
"command": "/Users/you/.local/bin/uvx"
```

## Checking it worked

Ask your assistant to call `get_capabilities`. It answers without touching the network or
needing an account, and it reports in one go whether there's a usable GPU, whether the globe
projection is supported, whether NVIDIA encoding is available, and whether you're logged in.
