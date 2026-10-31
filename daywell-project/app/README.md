# Daywell MVP

A clickable, working prototype of Daywell built on the design system (`tokens.css` is generated from `../design-system/project/tokens.json`; `bundle.css` is copied from `../design-system/project/components/`).

- No build step, no dependencies. Data lives in the browser (localStorage). "Reset demo data" restores the example data.
- Run locally: `python3 -m http.server 8000 -d daywell-project/app` and open http://localhost:8000
- Hosting: pushing to `main` deploys this folder to GitHub Pages (`.github/workflows/pages.yml`).

## What works
Home with one-tap check-ins synced to Habits; Habits Today (Done / Skip / Reschedule / Undo, All done state); My habits (pause, edit, archive, ideas); Quick capture; Create habit in two steps; Meditation browse with type, search, intention and length filters; Session detail that opens YouTube/Spotify; check-in sheet on return; completion feedback with streak and badges; Weekly review built from real history.

Streak rules: Done adds a day; Skip and Reschedule keep the streak; a scheduled day with nothing checked by midnight is missed. Reschedule moves the item to tomorrow.

## Not in the MVP
Accounts and sync, real push notifications, Exercise screens (tile shows "Soon"), date/time pickers for Reschedule.
