import sys

from tada_render.cli import main

sys.argv = ["travel-animator", "mcp"]
raise SystemExit(main())