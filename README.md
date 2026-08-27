# Travel Animator MCP

**Describe a trip. Get a video of it.**

Travel Animator MCP lets an AI assistant plan a route, style the animation and render it to
an MP4 on your machine — the route drawing itself as it is travelled, a 3D vehicle following
it, map labels, country flags, and the distance badge the mobile app draws on top.

[![PyPI](https://img.shields.io/pypi/v/travel-animator)](https://pypi.org/project/travel-animator/)
[![Python](https://img.shields.io/pypi/pyversions/travel-animator)](https://pypi.org/project/travel-animator/)
![Platforms](https://img.shields.io/badge/platforms-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey)
![Licence](https://img.shields.io/badge/licence-limited%20use-orange)

<!-- TODO(asset): 12s looping demo — a route drawing itself, vehicle following, on the globe.
     Add it as assets/demo.gif, then embed it here as a markdown image.
     Deliberately absent rather than committed broken: a 404 image is worse than none. -->

> **You say:** *"Make me a 20-second video of a road trip from Lisbon to Porto to Braga, on
> the Terrain map, with a red line and a car."*
>
> **Your assistant:** creates the project, adds the three stops, follows real roads between
> them, sets the map and line style, renders, and hands back the path to the MP4.

More prompts that work — and what it won't do — in [examples/prompts.md](examples/prompts.md).

---

## Install

Two commands. The second one is not optional — a stdio MCP server cannot prompt you for
credentials, so you log in once in your own terminal.

**Claude Code**

```bash
claude mcp add travel-animator -e TADA_SOURCE=readme -- uvx --from "travel-animator[mcp]" travel-animator mcp
uvx travel-animator login
```

**Claude Desktop, Cursor, VS Code, Codex, or any client that takes JSON**

```json
{
  "mcpServers": {
    "travel-animator": {
      "command": "uvx",
      "args": ["--from", "travel-animator[mcp]", "travel-animator", "mcp"],
      "env": { "TADA_SOURCE": "readme" }
    }
  }
}
```

…then `uvx travel-animator login` in a terminal.

`TADA_SOURCE` tells us which instructions you followed. Optional — delete it if you like.

**Already have Python?** `pip install "travel-animator[mcp]"` and use `travel-animator` as
the `command`. Python 3.12+.

Per-client instructions, including the "works in the terminal but not in the desktop app"
`PATH` fix, are in [docs/clients.md](docs/clients.md).

## What you need

| | |
|---|---|
| **Python** | 3.12 or newer |
| **Account** | The same Travel Animator account as the mobile app. **A free account can log in, browse the catalogues and author a project — only a premium account can render one.** |
| **Platform** | macOS (Apple silicon), Linux (x86-64, arm64), Windows (x64). These are the four wheels published; other platforms — including Intel macOS — are not supported. |
| **Disk** | The wheel is ~85 MB. It carries its own Java runtime and, on macOS and Windows, its own graphics driver — there is nothing else to install. Linux uses the system GLES driver, or Mesa for software rendering. |
| **Network** | Rendering is **not** offline: map tiles, glyphs and sprites are fetched as frames are drawn, then cached under `~/.cache/tada/render`. |

If your machine can't render at all, the server says so up front — before you build a project
it can't finish — and can fall back to a server-side render.

## What it can make

- **34 map styles** — Terrain, Satellite, Sketch, Glow, Comic, Winter, Pixel, Watercolor and
  more (`list_maps`). One is free; the rest need premium.
- **355 3D models** — land, air and water, from realistic cars and planes to an elephant
  (`list_models`). 11 are free.
- **7 route line styles** — solid, dashed, dotted, striped, glow, transparent, auto
  (`list_line_styles`).
- **Two projections** — flat `MERCATOR` or a 3D `GLOBE` with stars, a sun and a moon.
- **9–60 second** videos, at your choice of aspect ratio and resolution.
- **Real roads or straight lines**, per segment.
- Place labels, country flags, a distance badge, avatars and per-point effects.

## How it works

```
create_project → create_route → update_animation_state → render_video → await_render → MP4
```

Two things worth knowing, because they change how your assistant behaves:

- **Nothing is edited implicitly.** Every tool takes an explicit `project_id`. There is no
  "current project", so an assistant can hold several trips open without confusing them.
- **Projects are durable local state**, under `$XDG_STATE_HOME/tada-render/projects/<id>/`
  (`~/.local/state/…` if unset). Videos land in that project's `renders/`; the newest five
  per project are kept and older ones pruned. Close your assistant and the project is still
  there tomorrow.

## Tools

30 tools. Full reference with parameters in **[docs/tools.md](docs/tools.md)**.

| Group | Tools |
|---|---|
| **Check first** | `get_capabilities` · `auth_status` |
| **Projects** | `create_project` · `list_projects` · `get_project` · `delete_project` · `import_project` · `export_project` |
| **Route** | `create_route` · `get_route` · `add_point` · `update_point` · `remove_point` · `clear_route` · `set_real_route` |
| **Look & feel** | `get_animation_state` · `update_animation_state` · `list_maps` · `list_models` · `list_line_styles` |
| **Render** | `estimate_render` · `render_video` · `await_render` · `get_render_progress` · `get_render_result` · `cancel_render` |
| **Account sync** | `list_account_routes` · `save_project_to_account` · `load_account_route` · `delete_account_route` |

**Renders report progress as they go.** `render_video` returns immediately with a session id;
`await_render` waits on it and, if the render is still going, returns a line your assistant
reads out — frames done, percent, time left — and waits again. A ten-minute render is not a
ten-minute silence.

**Routes sync to the phone.** `save_project_to_account` puts a route in the mobile app's Saved
Routes. It carries **waypoints only** — the reply's `dropped` list names what didn't survive
(avatars, effects, extra model slots, local media, the animation settings), and your assistant
should tell you rather than report a clean save.

## Privacy Policy

The full policy — covering the apps, the website and this package — is at
[travelanimator.com/privacy-policy](https://www.travelanimator.com/privacy-policy); it has a
section of its own for the MCP server and CLI. What follows is that section in brief.

Usage analytics are **opt-in and off until you turn them on**. Nothing is collected before
that, and nothing at all is collected outside the MCP server.

```bash
travel-animator analytics status   # what is set, and what it covers
travel-animator analytics on       # grant consent
travel-animator analytics off      # revoke, effective immediately
```

**Never collected — unconditionally, whatever your consent says:** route coordinates, place
labels, route annotations, file paths, your media, the contents of any route you save or load,
the names you give projects, and what a tool returned. *A route records where somebody has
actually been.*

**Collected with consent:** which tools were called, in what order, how long they took and
whether they failed; render settings (resolution, duration, animation style, map, vehicle);
the *number* of points in a route and the set of countries it crosses.

**One free-text exception:** when an assistant asks for a tool this server doesn't have, the
sentence it writes describing what it was trying to do is collected with that request (up to
2048 characters) — that is the only way a server learns which capability it is missing. It is
never attached to an ordinary tool call. Analytics are processed in the United States by a
third-party provider.

## Command line

The MCP server is one of two front ends. The CLI is the other:

```text
travel-animator login           # log in: magic link, or a bearer token for CI
travel-animator logout          # remove credentials stored on this machine
travel-animator analytics       # show, grant or revoke analytics consent
travel-animator render-bundle   # render a prepared render bundle to MP4
travel-animator mcp             # run the MCP server (needs the mcp extra)
```

`render-bundle` renders bundles produced by the Travel Animator service; it does not create
them. The MCP server is the only path that goes from nothing to a finished video.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Tools fail with a "log in" message | No credential on this machine, or it expired | `travel-animator login` in a terminal, then retry |
| Login works, rendering is refused | Free account | Rendering needs premium |
| Server doesn't start from a desktop app | GUI apps don't inherit your shell `PATH` | Use the absolute path from `which uvx` |
| `pip install` fails on your Mac | Intel macOS has no wheel | Apple silicon, Linux or Windows only |
| Render fails on a machine with no GPU | No usable GL | Call `get_capabilities` first; use the server-side fallback |
| Second render refused | One render at a time, per project and per process | Wait, or `cancel_render` |

More, including error codes, in [docs/troubleshooting.md](docs/troubleshooting.md).

## Support

Open an [issue](../../issues) — please include your OS, `travel-animator --version`, your MCP
client, the tool that failed and its `error_code`. Or email
[connect@travelanimator.com](mailto:connect@travelanimator.com).

## Licence

**This is not open-source software.** The `travel-animator` package ships under a limited use
licence: you may install and run it unmodified to prepare and render Travel Animator content
and to talk to Lascade's services. You may not redistribute it, modify it, or build a
competing service with it. The full terms ship inside the package at `tada_render/LICENSE`.

Bundled fonts, flag artwork and the libraries inside the renderer are third-party works under
their own licences, listed in `tada_render/THIRD-PARTY-NOTICES.md`. For redistribution or
modification rights, contact Lascade.

The documentation and examples *in this repository* are MIT — see [LICENSE](LICENSE).

---

[PyPI](https://pypi.org/project/travel-animator/) ·
[travelanimator.com](https://travelanimator.com) ·
[Privacy](https://www.travelanimator.com/privacy-policy) ·
[iOS](https://apps.apple.com/app/id6462844561) ·
[Android](https://play.google.com/store/apps/details?id=com.travelanimator.routemap)
