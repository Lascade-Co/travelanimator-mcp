# Tool reference

30 tools, grouped the way you use them. Every tool that touches a project takes an explicit
`project_id` — there is no "current project", so nothing is ever edited implicitly.

Tools marked **account** need `travel-animator login`. Tools marked **premium** additionally
need a premium account.

---

## Check first

Call these before building a trip the machine or the account can't finish.

### `get_capabilities`
Reports what this machine can render: whether a usable GPU is present, whether the globe
projection is supported, whether NVIDIA hardware video encoding is available, and whether an
account is logged in. Anything that couldn't be determined is explained in `notes`.

### `auth_status`
Reports whether this machine holds a login for a Travel Animator account. Reads local files
only — never contacts the network.

---

## Projects

### `create_project` — `name`, `projection_name`
Creates a new named project on this machine, with the default animation settings and the
default map already filled in. Returns its `project_id`.

### `list_projects`
Lists every project stored on this machine.

### `get_project` — `project_id`
Fetches one project: name, timestamps, last render, and its full ExportConfig.

### `delete_project` — `project_id`
Deletes a project and everything under it, including videos already rendered from it. Cannot
be undone, and is refused while it is rendering.

### `import_project` — `name`, and exactly one of `path` / `config_json`
Creates a project from an existing ExportConfig, stored exactly as given — for example one
exported from the Travel Animator mobile app.

### `export_project` — `project_id`, `path`
Exports a project's ExportConfig unchanged: written to `path` if given, otherwise returned
inline.

---

## Route

Indexes are **0-based over waypoints** — the interpolated points that make up a road-following
segment don't count. The `index` `get_route` reports is the one every other route tool takes.

### `get_route` — `project_id`
The project's waypoints, in order.

### `create_route` — `project_id`, `points`
Replaces the whole route in one call. Needs at least 2 points and an **empty** route — call
`clear_route` first to replace an existing one. Send only `latitude`/`longitude` (degrees),
`place_label`, `model`, `avatars`, `effect`. `id`, `is_origin`/`is_destination` (assigned by
position — first point is the origin, last is the destination) and `country_code` (geocoded
offline from the coordinates of any point carrying a `place_label`) are server-managed and
rejected if sent. If the first point has no `model`, the catalogue's default is filled in.

### `add_point` — `project_id`, `latitude`, `longitude`, `index`, `model`, `place_label`, `effect`, avatar fields
Adds one point, appended unless `index` is given. Works on an empty route — the first point
added becomes both origin and destination, and a render needs at least 2.

> **Inserting inside a road-following segment is refused**, because the road geometry spans
> both endpoints. Disable it first with `set_real_route(index=…, enabled=false)`; the error
> names the segment.

### `update_point` — `project_id`, `index`, plus any point field
Partial update. Only the fields you send are touched; the result's `changed` list names them.
`country_code` is re-geocoded only when the update includes `place_label`.

### `remove_point` — `project_id`, `index`
Removes one waypoint. Removing the last remaining point clears the route.

### `clear_route` — `project_id`
Deletes every point in the route.

### `set_real_route` — `project_id`, `index`, `enabled` — **account**
Makes the segment *starting at* `index` follow real roads, or turns that off. The last waypoint
is refused — it has no next point to route to. Enabling looks the route up online and inserts
road geometry between the two waypoints; disabling removes it. Idempotent. Needs network access.

---

## Look and feel

### `get_animation_state` — `project_id`
Every setting `update_animation_state` can change, at its current value.

### `update_animation_state` — `project_id`, plus any setting
Partial update; the result's `changed` list names what moved. The settings that shape the video
most:

| Field | Notes |
|---|---|
| `video_duration` | seconds, 9–60 |
| `projection` | `MERCATOR` or `GLOBE` |
| `aspect_ratio`, `resolution` | output framing and size |
| `model_size` | vehicle scale, 0.2–1.5 |
| `line_style` | `line_type` / colour / width of the route line |
| `selected_map_id` | an id from `list_maps` |

Refinements: `flag`, `distance`, the `place_label_*` fields, `show_map_labels`,
`smoothening_factor`, `playback_speed`, `avatar_scale`, `animation_style`, `highlight_mode`,
`country_highlight_config`, `cover_image`, `localise_map`, `geocode_mode`.

- Setting `selected_map_id` also updates the config's map `style` in the same write. An id not
  in the current list of maps is rejected, and then **nothing at all changes**.
- Every colour field takes `#AARRGGBB` (or `#RRGGBB`).
- `watermark_slot` belongs to the ExportConfig rather than these settings, but is accepted
  here: `-1` removes the watermark, `0`–`3` select a bundled one.

### `list_maps`
The map styles available, with the id `selected_map_id` takes and whether each needs a
subscription. *34 styles today; one is free.*

### `list_models` — `type`, `premium`, `limit`, `detail`
The 3D models — id, name, type (`LAND`/`AIR`/`WATER`), premium, texture count. Capped at
`limit` (default 50). For a model's texture ids (for a point's `model.texture_id`), its model
files or its marker image: filter down to the one model, then call again with `detail=true`.
*355 models today; 11 are free.*

### `list_line_styles`
The values `line_style.line_type` accepts: `AUTO`, `SOLID`, `DASHED`, `DOTTED`, `STRIPED`,
`GLOW`, `TRANSPARENT`.

---

## Render

### `estimate_render` — `project_id`
How long a render will take and at what resolution, **without rendering anything** — no GPU,
no network, no account needed. Cheap; call it before committing a user to a long wait.

### `render_video` — `project_id` — **premium**
Validates the project and, if renderable, starts rendering to MP4 in the background; returns a
session id. If the config isn't renderable, nothing starts and the errors come back instead.

### `await_render` — `session_id`, `timeout_seconds`
Waits for the render and returns its result, pushing progress notifications to clients that ask
for them. If the render is still going it returns early with `timed_out: true` and a
human-readable `message` — frames, percent, time left.

> **The contract is: relay that message to the user, then call `await_render` again.** That
> relay is what makes a long render visible to the person waiting. Prefer it to one very long
> await, and don't poll `get_render_progress` in a loop.

### `get_render_progress` — `session_id`
Checks progress once, without waiting. For *following* a render, use `await_render`.

### `get_render_result` — `session_id`
A finished session's result, including the path to the video file.

### `cancel_render` — `session_id`
Stops a render that is still running.

---

## Account sync

These sync a route to the Travel Animator account, where the mobile app can see it. All need
`travel-animator login`.

### `list_account_routes` — **account**
Saved routes on the logged-in account — the same list the mobile app shows, across every device.

### `save_project_to_account` — `project_id` — **account**
Saves a project's route so it appears in the app's Saved Routes.

> **Waypoints only.** The reply's `dropped` list names what could not be saved — extra model
> slots, avatars, effects, local media, animation state. Relay it rather than reporting a clean
> save.

### `load_account_route` — `route_id` — **account**
Imports a saved route into a **new** local project and returns its `project_id`. No existing
project is touched, and only the waypoints are restored, not the look.

### `delete_account_route` — `route_id` — **account**
Deletes a saved route from the account — it disappears from the mobile app too.
