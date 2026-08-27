# Publishing to the MCP Registry

Maintainer notes. Nothing here is needed to *use* the server — start at the [README](README.md).

## How it works

[`.github/workflows/publish-mcp-registry.yml`](.github/workflows/publish-mcp-registry.yml)
publishes to the registry whenever `server.json` changes on `main`. The release pipeline is
what changes it: after `travel-animator` is published to PyPI, its version is committed here,
and that commit triggers the publish. An ordinary release needs nothing done by hand.

The workflow refuses to publish a version that is not on PyPI yet, and **skips** — rather than
fails — a version the registry already holds, since a published `(name, version)` pair is
immutable.

## One-time setup

**1. A TXT record on the apex of `travelanimator.com`** — not under a `_mcp-auth` selector,
which the registry does not read:

```bash
openssl genpkey -algorithm Ed25519 -out key.pem
PUBLIC_KEY="$(openssl pkey -in key.pem -pubout -outform DER | tail -c 32 | base64)"
echo "travelanimator.com. IN TXT \"v=MCPv1; k=ed25519; p=${PUBLIC_KEY}\""
```

macOS ships LibreSSL, which has no Ed25519 — `brew install openssl@3` and call it explicitly.

**2. `MCP_REGISTRY_DNS_KEY`**, in an environment named `mcp-registry` (Settings →
Environments) so it can be restricted to `main`. The value is the hex-encoded private seed:

```bash
openssl pkey -in key.pem -noout -text | grep -A3 "priv:" | tail -n +2 | tr -d ' :\n'
```

Keep `key.pem` out of the repo. When rotating, delete the old TXT record — a stale one is
tried first and fails verification.

## The `mcp-name` marker

The registry proves ownership of the PyPI package by finding

```
mcp-name: com.travelanimator/mcp
```

in the package README, which becomes the PyPI long description. It must match `name` in
[`server.json`](server.json) exactly — the registry compares them literally, so a rename has
to land on both. A description is baked into the built artifact, so the marker only reaches
the registry via a new release; it has shipped since 1.0.1.

Auth is DNS-based because the name is `com.travelanimator/mcp`. GitHub OIDC would authorise
only `io.github.lascade-co/*`, which would mean changing the marker and cutting another
release.

## Channel tags

Each config we publish names where it came from, so we can tell which listings are worth
keeping. Every channel ships the same `uvx --from travel-animator[mcp] travel-animator mcp`,
so nothing else tells them apart.

| Value | Set in | How |
| --- | --- | --- |
| `mcp-registry` | [`server.json`](server.json) — the registry entry, and anything mirroring it | `--source` in `packageArguments` |
| `mcpb` | [`mcpb/src/server.py`](mcpb/src/server.py) | `--source` in the wrapper, which replaces `sys.argv` |
| `readme` | [`README.md`](README.md) | `TADA_SOURCE` |
| `docs` | [`docs/clients.md`](docs/clients.md) | `TADA_SOURCE` |
| `pypi` | the package README | `TADA_SOURCE` |

- **Generated configs use `--source`, hand-copied ones use `TADA_SOURCE`.** The flag wins if
  both are set. A client that installed the server necessarily applied its arguments, while
  `environmentVariables` can be skipped silently — and a skipped one makes that channel read
  zero, which looks like a listing nobody used.
- **A new listing gets its own value, or a landing URL carrying one, before it goes live.**
  One that copies `server.json` inherits `mcp-registry`: misattributed, not unlabelled.
- **Never rename a value**, and never assign `unknown` or `invalid`. Events keep the old
  string, and the person-level `first_source` is written once and never updated.
- **The registry only sees a change on the next version bump** — the workflow skips a
  version it already holds, so editing `server.json` alone publishes nothing.
- **Keep the wrapper's `set_source` probe** when the release step rewrites
  `mcpb/pyproject.toml`. `--source` landed in 1.1.1; passing it to an older pin stops the
  server from starting at all.

## Publishing by hand

Only if the automation is unavailable.

```bash
# CLI: github.com/modelcontextprotocol/registry/releases/latest
mcp-publisher login dns --domain travelanimator.com --private-key "$MCP_REGISTRY_DNS_KEY"
mcp-publisher publish
```
