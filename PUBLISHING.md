# Publishing this server to MCP registries

Maintainer notes for whoever runs the listing. Nothing here is needed to *use* the server —
start at the [README](README.md) for that.

## 1. The prerequisite: the `mcp-name` marker

The official registry verifies PyPI ownership by fetching
`https://pypi.org/pypi/travel-animator/json` and looking for a line

```
mcp-name: com.travelanimator/mcp
```

**in the package README** — the one that becomes the PyPI long description. Without it,
publishing fails with *"Registry validation failed for package"*. `travel-animator` 1.0.0
does not carry it; 1.0.1 is the first release that does.

A package description is **baked into the built artifact**, so no already-published version
can be retrofitted. The marker reaches the registry only via a new release, which fixes the
order of operations:

1. Release 1.0.1 (or later) to PyPI.
2. Confirm the marker landed:
   `curl -s https://pypi.org/pypi/travel-animator/json | grep -c "mcp-name"` → `1`
3. Then, and only then, `mcp-publisher publish`.

The marker must match `name` in [`server.json`](server.json) **exactly** — the registry
compares them literally. Both say `com.travelanimator/mcp`; a rename on either side has to
land on both.

## 2. Namespace

`com.travelanimator/mcp`, verified by a DNS or HTTP challenge on `travelanimator.com`.

The name must match the namespace of whatever auth method you use, or publishing fails with
"You do not have permission to publish this server." The GitHub-auth alternative would be
`io.github.lascade-co/…` — which would mean changing the marker in the package and cutting
another release, so the choice is settled by whatever the published artifact says, not by
preference.

## 3. Publish

```bash
# get the CLI from github.com/modelcontextprotocol/registry/releases/latest
mcp-publisher init          # generates/validates server.json — trust this over the hand-written file
mcp-publisher login dns --domain travelanimator.com   # or: mcp-publisher login github
mcp-publisher publish
```

`server.json` in this repo was written by hand against the published schema. **Validate it
against `$schema` before publishing** — run `mcp-publisher init` and diff, rather than
assuming the hand-written argument shapes are right.

## 4. Automate the version bump

`server.json` carries the version twice (server and package) and both must track PyPI. Add a
GitHub Action on release that rewrites them and republishes, using OIDC (`id-token: write`)
so no token is stored. Otherwise the registry entry silently rots one release after launch.

## 5. Also list on

- [mcpservers.org](https://mcpservers.org) — PR to their list
- [Smithery](https://smithery.ai), [Glama](https://glama.ai/mcp/servers), [PulseMCP](https://www.pulsemcp.com)
- [punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) — PR
- Docker MCP community registry, if a container image is ever published

Keep `server.json` the canonical source for the metadata each of these asks for, and copy from
it, so the directories don't drift apart.

## 6. Repo settings to set at the same time

- **Description:** "Make animated travel-route videos by asking your AI assistant — MCP server
  for Travel Animator." *(The current one promises "itineraries and trip media", which the
  server does not do.)*
- **Topics:** `mcp`, `model-context-protocol`, `mcp-server`, `claude`, `video-generation`,
  `maps`, `travel`, `python`, `animation`
- **Social preview image** (Settings → Social preview, 1280×640) — this is what renders when
  the repo is shared anywhere.
- **Website:** https://travelanimator.com
- Enable Issues; add the issue templates.

## 7. The links back from PyPI

Through 1.0.0 the PyPI sidebar carried only `Homepage`, so nobody arriving from PyPI could
find this page. `Documentation` and `Issues` entries pointing here ship with 1.0.1, alongside
the `mcp-name` marker.

They are deliberately **not** `Repository`/`Source`: this repo is documentation, and the
package source is not public — a `Source` link here would claim otherwise.
