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

Every configuration we publish carries a `TADA_SOURCE` environment variable naming the place
it came from. It exists because nothing else can tell our channels apart: they all ship the
same `uvx --from travel-animator[mcp] travel-animator mcp`, so the install shape and the MCP
client name are identical whichever listing the user read. The tag records **which snippet was
copied** — nothing more, and nothing about the user.

| Value | Where it is set |
| --- | --- |
| `mcp-registry` | [`server.json`](server.json) — the registry entry **and every directory that mirrors it** |
| `mcpb` | [`mcpb/manifest.json`](mcpb/manifest.json) — the Claude Desktop bundle |
| `readme` | [`README.md`](README.md) |
| `docs` | [`docs/clients.md`](docs/clients.md) |
| `pypi` | the package README, i.e. the PyPI project page |

`unknown` (unset) and `invalid` (not a `[a-z0-9-]` slug of 32 characters or fewer) are
reserved and must never be assigned. A `pip install` user has no configuration file for a tag
to live in, so `unknown` is a large and legitimate bucket.

**Adding a listing.** Give it its own value, or point it at a landing URL whose snippet
carries one, *before* it goes live. A directory that copies `server.json` inherits
`mcp-registry`, which means its installs are **misattributed rather than unlabelled** — the
bucket reads as bigger than it is and the new listing reads as zero. Never reuse a value
across two places, and never rename one: events keep the old string, and the person-level
`first_source` is written with `$set_once`, so a rename splits one channel in two forever.

Registry users receive the variable only from the next version the registry publishes. The
workflow above skips a `(name, version)` pair the registry already holds, so editing
`server.json` without a version change publishes nothing.

## Publishing by hand

Only if the automation is unavailable.

```bash
# CLI: github.com/modelcontextprotocol/registry/releases/latest
mcp-publisher login dns --domain travelanimator.com --private-key "$MCP_REGISTRY_DNS_KEY"
mcp-publisher publish
```
