import sys

from tada_render.cli import main

# `--source` here rather than in the manifest's `mcp_config`: this line replaces
# argv wholesale, so an argument added there would be discarded, and an `env`
# entry there depends on how the host chooses to apply it. This wrapper ships
# inside the bundle, so the tag cannot be dropped by anything between us and the
# server.
#
# PROBED, not assumed. The pin in mcpb/pyproject.toml is rewritten by the release
# step, and a wrapper that passed `--source` to a travel-animator that predates
# the flag would not start AT ALL -- argparse exits 2 on an unrecognised
# argument. `analytics.set_source` shipped in the same release as the flag, so its
# presence is the exact test, and an older pin simply goes untagged.
argv = ["travel-animator", "mcp"]
try:
    from tada_render import analytics

    if hasattr(analytics, "set_source"):
        argv += ["--source", "mcpb"]
except Exception:
    pass

sys.argv = argv
raise SystemExit(main())
