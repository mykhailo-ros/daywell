# Daywell: project handoff (app design with Claude)

Saved 31 October 2026. This file holds everything needed to continue the project in another account or on another computer.

## 1. Current status

The design system, all 12 first-round screens, a user-flow presentation, two rounds of logo exploration and a website entry page are built and published. A logo direction has been chosen, but the logo itself isn't finished.

**Published artifacts** (all private to the original account; other people, including another account, can't open them until they're shared from each page's Share menu):

| Artifact | Link | What it holds |
| --- | --- | --- |
| Daywell design system | https://claude.ai/artifact/NGnPyeCAXizBCnZQHWNrVD | Tokens, brand book (README), shared CSS and icon set, 12 screen cards (with extra states), Controls card, Streak legend card, Cover |
| Daywell User Flows | https://claude.ai/artifact/KcW3Ps23N2KTomjgDkAEDf | All 15 screens and states in user-flow order, with a full-size step-through present mode |
| Daywell Logo Directions (round 1) | https://claude.ai/artifact/N8tT2QEa5Mntcko2wdiBAW | 5 first directions: Kept dot, Horizon, Day arc D, Daily loop, Wordmark |
| Daywell Logo Refinements (round 2) | https://claude.ai/artifact/BUTHgVJswZuV8Bfjtrtpie | Horizon, D with a sun, D with a rising sun, DW, DW with a sun; 3 website wordmarks |
| Daywell (website entry page) | https://claude.ai/artifact/RgRmh1rpeg1tkJtEgyMXxf | Landing page with the chosen logos, product info and sign-up |

**Checked:** every screen, the flow page, both logo pages and the entry page were rendered in a headless browser (Chromium) at desktop width, and the web pages at phone width too. There was no horizontal overflow and no script errors. Contrast values were calculated by hand from the hex values and weren't measured with a tool.

**Not checked:** the design system's own published page in a browser. Screen previews were checked locally using a hand-built stand-in for the `tokens.css` file the page generates (see section 8).

## 2. How to continue in another account

1. In the original account, share the artifacts above with the new account (Share menu on each page), or accept that the new account rebuilds from this file.
2. Start a new Claude Code session, attach this file and send:

> Read this handoff file. The Daywell design system, screens, flow page, logo explorations and entry page already exist (section 1). Continue from the "Next steps" in section 9. Treat the brief in section 7 as the source of truth and sections 3 to 6 as the decisions actually built. Tell me about anything you could not verify.

If the artifacts aren't shared, the new account should create its own Design System artifact and rebuild from sections 3 to 6 and 8.

## 3. Design decisions (as built)

### Colour

Light mode only, mostly monochrome with one accent. The theme id is `light` (one theme).

| Token | Value | Use |
| --- | --- | --- |
| bg | #FFFFFF | Screen background and sheets |
| surface | #F5F5F2 | Grouped panels: progress strip, segmented track, search field |
| canvas | #E9E9E5 | Presentation only: backdrop behind phone frames |
| line | #E4E4E0 | Hairline dividers |
| line-2 | #D2D2CD | Card outlines, unselected chips |
| border-control | #8C8C86 | Check-in rings, inputs, toggles (3.4:1 on bg, 3.1:1 on surface) |
| ink | #161616 | Main text, icons, selected chips (17:1) |
| ink-2 | #4F4F4B | Secondary text (8:1) |
| ink-3 | #6B6B66 | Tertiary text, completed items (5:1) |
| accent | #2F6F62 | Deep sage teal: progress, streaks, check-ins **and the primary button** (5.9:1 on white) |
| accent-press | #245A4F | Pressed accent |
| accent-tint | #E7F0EC | Quiet accent ground: highlighted review card, badge tile |
| on-accent | #FFFFFF | Text on accent |
| scrim | #16161652 | Behind bottom sheets |
| focus | alias of accent | 2px focus ring |

**Accent rule as built:** the accent means progress, and it is also used for the single primary button on a screen. Selected chips and segmented controls use ink, never the accent.

### Type

Figtree from Google Fonts, weights 400, 500 and 600.

| Style | Size / line height / weight |
| --- | --- |
| t-display | 34 / 40 / 600, −0.5 letter spacing |
| t-title | 26 / 32 / 600, −0.3 |
| t-numeral | 24 / 28 / 600 |
| t-heading | 18 / 24 / 600 |
| t-body-strong | 16 / 22 / 600 |
| t-body | 16 / 24 / 400 |
| t-label | 14 / 20 / 500 |
| t-caption | 13 / 18 / 400 |
| t-overline | 12 / 16 / 600, +0.6, set in capitals |

### Spacing, radius, elevation and icons

- **Spacing:** 4, 8, 12, 16, 20 (screen gutter), 24, 32, 48 px.
- **Radius:** 8 (sm), 14 (md: buttons, inputs, cards), 24 (lg: sheets), 999 (pill).
- **Shadows:** `shadow-device` (preview frames only), `shadow-sheet` (the only in-app elevation), `shadow-thumb` (segmented thumb, toggle).
- **Icons:** a custom outline set on a 24 grid with a 1.75 stroke and round caps, shipped as CSS masks (`.ic .ic-<name>`). There are 28 icons: check, chevron-left, chevron-right, search, clock, bell, external, calendar, plus, more, pause, edit, archive, skip, reschedule, breath, habit, exercise, flame, award, sunrise, sun, moon, close, idea, sliders, chart, lock.
- **Tap targets:** at least 44 px. List rows are at least 56 px.
- **Frame:** 390×844 with a simple status bar and home indicator, inside a rounded frame (no realistic device mockup).

### Components

No React components were built. The screens are static HTML that share one stylesheet (`components/bundle.css`, with `dw-` classes). These patterns exist as CSS: phone frame, status bar, nav bar, list item, check-in ring, row actions, buttons (primary, secondary, tertiary, small), chips, segmented control, text field, toggle, cards and panels, progress strip, entry tiles, week dots, bottom sheet, menu, keyboard, lock screen and notification, day picker, radio rows.

The planned components (Icon, Button, CheckIn, Chip, TextField, Tabs, TodayItem, HabitRow, SessionCard, ProgressStrip, BottomSheet, Notification, Phone) don't exist as React exports.

### Navigation

There is no bottom tab bar. Home is the hub, with tiles for Meditation, Habits and Exercise. Other screens use back arrows. Habits has a segmented control with **Today | My habits** (not Review). Weekly review opens from a row at the top of My habits.

### Logo (chosen, not finished)

- **App icon:** "DW with a sun" (round 2, A5). A rounded D, then a W lowered into two soft hills, with a sun dot between them. It uses a 4.5 stroke on a 60×48 grid and goes on an accent tile in white.
- **Website logo:** "Pill ll" wordmark (round 2, B2). It's lowercase "daywe" in Figtree 600, with the double l drawn as two pills: the first filled in ink, the second outlined in accent. On dark backgrounds it uses ink #ECECE8 and a mint #86C2B2 pill.
- **Not done:** final drawing (optical corrections, a small-size version, clear-space and minimum-size rules), adding the logos to the design system, and a trademark search.

## 4. Screens produced

All 12 screens from the brief, plus 3 extra states. Each has a card in the design system with design notes beside it.

| # | Screen | Extra state |
| --- | --- | --- |
| 01 | Home | — |
| 02 | Meditation browse | — |
| 03 | Session detail | — |
| 04 | Check-in on return (bottom sheet over Session detail) | — |
| 05 | Follow-up notification (lock screen) | — |
| 06 | Completion feedback (with badge) | — |
| 07 | Habits – Today | 07b "All done for today" |
| 08 | My habits | 08b ··· menu open (Pause, Edit, Archive) |
| 09 | Quick capture (sheet with keyboard) | — |
| 10 | Create habit, step 1 | — |
| 11 | Create habit, step 2 (selected days, at a time) | 11b routine anchor (Before bed) with optional reminder |
| 12 | Weekly review (one long scroll with the 844px fold marked) | — |

The design system also has a **Controls** card (shared controls and all 28 icons), a **Streak legend** card and a **Cover**.

**Planned outputs, status:**
- One card per screen: done.
- A board with shared state, where checking in on Home updates Habits: **not built**. The flow page is static.
- A clickable single-phone prototype: **not built**. The flow page's present mode steps through screens in order but has no tappable controls.
- The planned "1b. Home after check-in" state: **not built**.

## 5. Example data (as used in the screens)

"Today" is Friday 30 October, and the user is called Alex.

| Time | Item | Type | Streak | This week (review) |
| --- | --- | --- | --- | --- |
| Morning | Stretch for 5 minutes (every day) | Habit, added as placeholder | — | 7 of 7 |
| 7:30 a.m. | Morning focus breath, 8 min (YouTube, Focus, scheduled daily) | Meditation | 2 days before, 3 after Done | — |
| After lunch | Short walk (every day) | Habit | — | 6 of 7, 1 rescheduled |
| 6:00 p.m. | Full-body strength, 25 min | Exercise, placeholder | — | — |
| 7:00 p.m. | Daily study: "Study for 30 minutes" (Mon–Fri, reminder on) | Habit | 5 days (6 after tonight) | 4 of 5, Wed skipped |
| Before bed | Read for 10 minutes (every day) | Habit | — | 6 of 7, 1 skipped |

- **Home (9:12 a.m.):** Stretch done 7:05, meditation done 7:41, so "2 of 6 done. A good start." Progress strip: Streak 5 days (Daily study), Today 2 of 6, Latest badge "Three in a row".
- **Daily study streak logic:** Done adds a day. Skip and Reschedule hold the streak without adding to it. Wednesday was skipped, so the week reads 4 of 5 and the streak is kept.
- **Meditation:** done Wed, Thu and Fri, so the meditation streak is 3 and the badge "Three in a row" is earned. Mon and Tue show as missed (neutral).
- **Weekly review:** covers Mon 26 Oct to Sun 1 Nov and opens Sunday evening. Headline "A steady week.", subline "Every habit kept its streak this week." Daily study is the lowest at 4 of 5 and the screen suggests "Change time to 6:00 p.m.".
- **Browse results:** Morning focus breath (8 min, YouTube), Box breathing for clear thinking (6 min, YouTube), Steady breath before work (10 min, Spotify). All are Breathwork with the Focus intention.
- **Saved intentions:** "Practise guitar", "Cook a new recipe".
- **Notification:** 8:05 a.m. on the lock screen, the alternative branch when the user doesn't come back.

## 6. Assumptions and open questions

### Placeholders I invented
- User name "Alex"; the habit "Stretch for 5 minutes" (so the Morning group isn't empty); the workout "Full-body strength, 25 min" at 6 p.m.; the meditation time 7:30 a.m.
- Saved intentions, the extra session titles, the Spotify source, the badge name "Three in a row".
- Weekly numbers for Stretch, Short walk and Read.
- Entry page: "Daywell for iPhone and Android" (platforms not confirmed), and placeholder footer links (About, Privacy, Terms).

### Rules I assumed (shown in the design notes)
- The progress strip shows the longest current habit streak (Daily study), not an overall app streak.
- "Not this time" closes the check-in sheet without logging and says nothing about the streak.
- "Remind me later" (or swiping the sheet down) leaves the item open in Today.
- The follow-up notification is sent once, about 15 minutes after the session's length has passed.
- Completion feedback closes after 4 seconds or on tap.
- Paused habits move to a "Paused" group with their streak frozen. Archive keeps history.
- The Weekly review entry shows "Week so far" until Sunday evening.
- Done items stay in place, greyed, rather than moving to the bottom.
- A 10-minute session counts as 5–10 (shown under that filter).

### Still open
- **Remove or Archive?** My habits uses Archive and Weekly review uses Remove, as in the brief. Are they the same action?
- **Change time vs Reschedule:** treated as permanent vs one occurrence. The Reschedule picker itself isn't designed (notes mention "Rescheduled to 8:30 p.m.").
- **Exercise:** Home has a tile, but there are no Exercise screens.
- **"Schedule for later":** the notes say it opens a date and time picker. The picker isn't designed.
- **Overall streak:** not defined or shown anywhere.
- **Platforms and launch** for the entry page.
- **Placeholder app mark:** the notification on screen 05 and the design system cover still use the old green tile with a check, not the chosen DW-with-sun icon.

## 7. Original brief (verbatim)

Design the first-round mobile screens for Daywell

Daywell is a mobile app for wellbeing and building routines. It helps people stay consistent with small daily activities such as habits, meditation and exercise. It supports users through organisation, reminders and progress tracking (streaks and badges). It does not host meditation content itself.

Visual direction: minimal and focused. Mostly monochrome with one accent colour, plenty of whitespace and clear typographic hierarchy. Use simple outline icons and no decorative illustrations. The tone should be calm, clear and encouraging, never guilt-inducing. Design for a phone at 390×844, light mode.

Screens to design (about 12):

Home

Home: a greeting, then a "Today" list of everything scheduled for today across the app (habits, a scheduled meditation, a workout). Each item gets a one-tap check-in. Below that, a compact progress strip with the current streak, today's completion and the latest badge, plus entry points to Meditation, Habits and Exercise. Checking in here also updates the item in its own section.

Meditation (Daywell helps users find sessions and track them, but doesn't play them)

Browse: tabs or chips for Meditation, Breathwork and Affirmations, a search field, and filters for intention (Peace, Focus, Sleep, Energy) and length (under 5, 5–10, 10–20, 20+ minutes). Results are cards showing title, length, source (for example YouTube) and intention.

Session detail: title, length, source and short description. Two actions: "Start on YouTube" and "Schedule for later." Add a small note: "This opens YouTube. Come back to log it."

Check-in on return: a bottom sheet that appears when the user comes back to the app after leaving for a session: "Did you complete Morning focus breath?" with the options Done, Not this time and Remind me later.

Follow-up notification: a lock-screen notification sent once if the user doesn't come back: "Finished your session? Tap to check in."

Completion feedback: a short confirmation after Done showing the updated streak, plus a badge if one was earned.

Habits

Habits – Today (the default tab): only today's habits, grouped by Morning, During the day and Evening. Each row has the habit name, its time and the actions Done, Skip and Reschedule. Include an "All done for today" state.

My habits: active habits grouped by routine, each showing its schedule and next due date. Habits can be paused, edited or archived. Saved intentions sit in their own small section ("Ideas to turn into habits").

Quick capture: a single field, "What would you like to make a habit?", with a Save button. It saves an intention without setting a schedule.

Create habit, step 1: "Make it specific." The user enters a name, then turns it into a concrete action using suggested chips (for example, "Study" becomes "Study for 30 minutes").

Create habit, step 2: "When would you like to do it?" The user picks every day or selected days, then a time or a routine anchor (Morning, After lunch, After dinner, Before bed). Picking an anchor still asks for an optional reminder time. End with a Save button.

Weekly review: each habit with its completion this week (for example "4 of 5 days"). The habit with the lowest completion is highlighted, with the options Change time, Pause or Remove. A section lists saved intentions ("Turn one into a habit?"), and the screen ends with a short reflection prompt: "Which habits felt manageable?"

Streak rules (show these consistently): Done counts. Skip and Reschedule keep the streak. A habit nobody checks off by midnight counts as missed. Meditation completion is self-reported, so never ask for proof.

Example data: Use this example data throughout: a habit called "Daily study," set up as "Study for 30 minutes," Mon–Fri at 7 p.m. with a reminder, on a 5-day streak. Its weekly review shows 4 of 5 days and suggests moving it to 6 p.m. Add "Read for 10 minutes" (before bed) and "Short walk" (after lunch), plus a scheduled meditation, "Morning focus breath, 8 min."

Constraints: keep to the features described here. Don't add social features, an in-app player, mood tracking or flexible weekly targets. Use one consistent term for each action (always "Reschedule," never "Move to another day").

## 8. Technical notes

### Design system files (as published, under `project/`)

| File | Purpose |
| --- | --- |
| project/design-system.json | The index: `namespace: "Daywell"`, `libraries: []` (no React), `createdOnFiles` marker, `lastChange` |
| project/README.md | Brand book: content rules and the one-term-per-action table, streak rules, visual foundations, iconography, navigation, example data, out of scope |
| project/tokens.json | Tokens as lists: color (one `light` theme), type (Figtree, 9 styles), spacing, radius, shadow |
| project/components/bundle.css | All shared screen styles, the 28 icons as CSS masks, and the Google Fonts `@import` for Figtree |
| project/components/<Name>/preview.html | One card each for Home, MeditationBrowse, SessionDetail, CheckInSheet, FollowUpNotification, CompletionFeedback, HabitsToday, MyHabits, QuickCapture, CreateHabitStep1, CreateHabitStep2, WeeklyReview, Controls, StreakLegend. Line 1 is a marker like `<!-- @dsCard group="Habits" height=920 width=1300 subtitle="…" -->` |
| project/components/<Name>/README.md | Short usage guideline per card |
| project/components/Cover/preview.html | The cover: accent-tint field with a week of check-in dots, an ink slab and an accent block, with "Daywell" set large. No README beside it |

There is no `bundle.js` and no `index.d.ts`, because nothing is a React component.

### How it was built

- Python scripts generated the design system files, the flow page, the logo pages and the entry page. Playwright with Chromium rendered them to check layout.
- The scripts ran in a temporary cloud container, so they may already be gone. The **published artifacts are the source of truth.**
- The flow page and the entry page **embed copies** of the screen HTML. They don't update when the design system changes, so rebuild them after screen edits.
- The entry page's sign-up form isn't connected. Submitting it shows a "Prototype" message.

### Still to verify on the live design system page
- Whether the page generates `tokens.css` for a new system before anyone saves. Previews depend on it, and local checks used a stand-in.
- Whether Figtree loads through the `@import` in `bundle.css` in the live preview frames.
- How the wide (1300px) multi-phone cards scale down on the page.
- Whether the built-in browser can open the artifact without a new sign-in.

## 9. Next steps

1. Finish the logo: final drawing of DW with a sun and the Pill ll wordmark, a small-size version, clear-space rules, and a trademark search.
2. Add the logos to the design system (a Logos asset group). Replace the placeholder app mark on screen 05 and refresh the Cover and the entry page.
3. Decide the open questions in section 6, especially Archive vs Remove, the Reschedule picker, the Schedule-for-later picker and Exercise.
4. Optional: the shared-state board, a clickable prototype, and the "Home after check-in" state.
