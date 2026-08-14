# Prompts that work

Copy one, change the places. Your assistant does the rest — you don't need to know any tool
names.

### A simple road trip

> Make a 20-second video of a road trip from Lisbon to Porto to Braga. Follow the real roads,
> use the Terrain map, a red route line and a car.

### A flight, on the globe

> Animate a flight from Tokyo to San Francisco on the globe projection, 15 seconds, with a
> plane and the country flags showing. Portrait, for Instagram.

### A long multi-stop tour

> Build a world tour: London, Cairo, Mumbai, Bangkok, Sydney, Auckland. Globe projection,
> 45 seconds, Satellite map. Label each city.

### Sailing

> A 30-second sailing route around the Greek islands — Athens, Mykonos, Naxos, Santorini —
> with a boat, on the Marine map, in 4K.

### Style it after the fact

> Show me what map styles there are, then switch my Portugal project to Sketch and make the
> line dashed and white.

### Reuse a route from your phone

> List the routes saved on my Travel Animator account, then load the Iceland one and render it
> as a 30-second globe animation.

---

## Getting better results

**Ask for a duration.** Anything from 9 to 60 seconds. Without one you get the default, which
may be faster than you want for a long route.

**Say "follow the real roads"** if you want driving geometry rather than straight lines between
stops. It needs a network call per segment, so it's off unless asked for.

**Name the aspect ratio** — "portrait for Instagram", "16:9", "square". Same for resolution.

**Ask for an estimate first** on anything long: *"how long will that take to render?"* — it
costs nothing, uses no GPU and needs no account.

**Check the machine first** if you're unsure it can render at all: *"can this machine render
Travel Animator videos?"* answers GPU, globe support, hardware encoding and login status in one
call.

**Expect progress, not silence.** A long render should produce periodic updates — frames done,
percent, time left. If your assistant goes quiet, ask it to check on the render.

## What it won't do

- Plan an itinerary, book anything, or tell you what to see. It animates routes.
- Render without a premium account. A free account authors fine.
- Render on a machine without a usable GPU — though it can fall back to a server-side render,
  and it tells you up front.
- Save your full styled project to the phone. Account sync carries **waypoints only**; your
  assistant should relay the `dropped` list of what didn't make it.
