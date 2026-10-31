# Daywell project files

Exported 31 October 2026 from a Claude Code cloud session. Read HANDOFF.md first.

- design-system/project/ : the exact files published to the Daywell design system artifact (tokens, README, bundle.css, screen previews, cover)
- design-system/build.py : generates project/components (screens, bundle.css). render.js : local Playwright preview check
- flow-page/ : the User Flows page and its builder (reads ../design-system paths; adjust paths in build_flow.py)
- logos/ : round 1 (index.html, build.py) and round 2 (round2.html, build2.py)
- website/ : entry page (index.html) and its builder; screens/ holds the copied screen previews it embeds

Builders need Python 3 with beautifulsoup4; render checks need Node with Playwright.
Note: paths inside the scripts point at the original cloud folders and need updating on a new machine.
