# Troubleshooting

Every failing tool returns an `error_code`. It is the single most useful thing to include in a
bug report.

## "Log in" errors

These all mean the same thing — this machine has no usable credential — and they all have the
same fix: **run `travel-animator login` in a terminal, then retry.**

`missing_tars_token` · `auth_session_expired` · `not_authenticated` · `authentication_failed`
· `invalid_session` · `session_expired` · `token_expired` · `invalid_token`

The server can't do this for you: on a stdio server, stdin *is* the JSON-RPC channel, so the
interactive magic-link prompt can't run inside the server process.

## `premium_required`

Not a login problem, and logging in again will not fix it. **A free account can log in, browse
the catalogues and author a project; only a premium account can render one.** Free accounts
also see one free map style and 11 free models out of 34 and 355.

## Rendering

| Code | What happened | What to do |
|---|---|---|
| `gl_unavailable` | No usable OpenGL ES on this machine | Call `get_capabilities` first — it tells you before you build a project. Use the server-side fallback |
| `hardware_encoder_unavailable` | NVENC asked for, no NVIDIA encoder present | Use the default `libx264` encoder |
| `render_busy` | This server process is already rendering | Wait, or `cancel_render` |
| `project_busy` | Another server process holds this project's render lock | The message names the holding pid |
| `output_too_large` / `render_output_invalid` | Encode produced nothing usable | Reduce resolution or duration; report it |
| `invalid_media` | A referenced image or media file couldn't be read | Check the path or URI on the point |
| `invalid_render_job` / `internal_render_error` | The render service refused or failed | Include the code in a bug report |

A common config-level rejection: **a route needs at least 2 points, and the origin needs a 3D
model.** `create_route` and `add_point` fill the origin's model from the catalogue default when
you omit it, so this normally only bites configs imported from elsewhere.

## Catalogue and account sync

`catalog_unreachable` · `catalog_http_error` · `catalog_invalid_response` ·
`catalog_response_too_large` — `list_maps`/`list_models` couldn't reach the catalogue service.
Usually network or a proxy.

`saved_route_unreachable` · `saved_route_request_failed` · `saved_route_invalid_response` ·
`saved_route_response_too_large` — the account-sync tools couldn't reach the service.

## Install and startup

**The server doesn't start from a desktop app, but works in the terminal.** Apps launched from
a GUI don't inherit your shell's `PATH`. Put the absolute path in the config — `which uvx`
prints it.

**`pip install` finds no matching distribution.** Four wheels are published: macOS Apple
silicon, Linux x86-64, Linux arm64, Windows x64. Intel macOS is not among them.

**Tools appear but every render fails.** You're probably on a machine with no GPU. Call
`get_capabilities`.

**The download is huge.** ~85 MB. The wheel carries its own Java runtime, and on macOS and
Windows its own graphics driver, so there's nothing else to install.

## Renders are slow or silent

Renders are not instant, and progress is a two-part contract: `render_video` returns a session
id immediately, and `await_render` blocks for up to 90 seconds before returning
`timed_out: true` with a progress line. If your assistant goes quiet for ten minutes, it is
awaiting once instead of relaying and re-awaiting. `estimate_render` will tell you how long to
expect before you start.

## Where things are on disk

| | |
|---|---|
| Projects | `$XDG_STATE_HOME/tada-render/projects/<id>/` (`~/.local/state/…` if unset) |
| Rendered videos | that project's `renders/` — newest five per project are kept |
| Tile cache | `~/.cache/tada/render` |
| Credentials | removed by `travel-animator logout` |

## Reporting a bug

Open an [issue](../../issues) with: your OS, `travel-animator --version`, your MCP client, the
tool that failed, its `error_code`, and the command you ran. For a render that produced a
*wrong-looking* video rather than an error, attach a frame and the output of `export_project`.
