import sys

from tada_render.cli import main

# The channel tag goes here, not in the manifest: this line replaces argv, so
# anything in `mcp_config.args` would be discarded. Probed because `--source`
# landed in 1.1.1, and an older pin exits 2 on an unknown argument.
argv = ["travel-animator", "mcp"]
try:
    from tada_render import analytics

    if hasattr(analytics, "set_source"):
        argv += ["--source", "mcpb"]
except Exception:
    pass

sys.argv = argv
raise SystemExit(main())
