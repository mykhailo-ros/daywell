Daywell helps people keep small daily routines (habits, meditation, exercise) through organisation, reminders and progress tracking. It finds and tracks meditation sessions but never plays them. The interface is minimal and focused: monochrome, one accent colour, lots of whitespace and a clear type hierarchy. Every screen is designed for a 390 × 844 phone in light mode.

## Content fundamentals

- **Calm, clear, encouraging. Never guilt.** Celebrate what got done and treat the rest as neutral. Write "2 of 6 done. A good start.", never "You still have 4 left". A missed day is just a fact, with no red, no warning icon and no "you broke your streak".
- **Second person, short sentences, sentence case.** "When would you like to do it?" Use full stops on full sentences and none on labels.
- **No emoji, no exclamation-mark pile-ups.** At most one "!" on a screen, and only on a completion moment.
- **Times** are written `7:00 p.m.` / `8 min`, and dates as `Friday 30 October`. Use ranges with an en dash: `5–10 min`, `Mon–Fri`.
- **One word per action, everywhere:**

| Action | Always | Never |
| --- | --- | --- |
| Mark complete | **Done** | Complete, Finish, Check |
| Skip today, keep streak | **Skip** | Pass, Not today |
| Move to another time or day | **Reschedule** | Move to another day, Snooze, Postpone |
| Stop temporarily | **Pause** | Disable, Hold |
| Remove from active list | **Archive** (in My habits), **Remove** (in Weekly review) | Delete |
| Save an idea without a schedule | **Save** | Add, Capture |
| Meditation check-in when the user returns | **Done** / **Not this time** / **Remind me later** | Yes / No |

## Streak rules (show these the same way everywhere)

1. **Done** counts and adds a day to the streak.
2. **Skip** and **Reschedule** keep the streak. They don't add a day and they don't break it. Show "Streak kept" beside them.
3. A habit nobody checks off by midnight counts as **missed** and the streak restarts. Say it neutrally: "Missed", in `ink-3`, with a hollow dot.
4. **Meditation is self-reported.** Never ask for proof, a timer or a screenshot. Tapping Done is enough.

Week dots use one legend in every place they appear: a filled `accent` dot means Done; a hollow `accent` ring with a dash means Skipped or Rescheduled (kept); a hollow `border-control` ring means Missed; a `line` dot means not scheduled.

## Visual foundations

- **Colour.** The app is monochrome with one accent. Text is `ink` on `bg`, secondary text is `ink-2` and tertiary text is `ink-3`. `accent` is reserved for check-ins, progress, streaks and the single primary button on a screen. Selected chips and segmented controls use `ink`, never accent, so the accent always means "progress". `accent-tint` is a quiet ground for one highlighted card per screen. `canvas` is used only behind phone frames in previews.
- **Type.** Use Figtree throughout. A screen has one `t-title` (or one `t-display` for a greeting or completion), `t-heading` for section headings, `t-body-strong` for item titles with a `t-caption` meta line under them in `ink-2`, and `t-overline` capitals in `ink-3` for group labels.
- **Spacing.** Screens use a 20px gutter (`space-5`) and `space-6` between sections. List rows are at least 56px tall, and every tap target is at least 44 × 44px.
- **Shape.** Buttons, inputs and cards use `radius-md`, chips and check rings use `radius-pill`, and sheets use `radius-lg`. Separate content with hairline `line` dividers rather than boxes. Cards get a `line-2` outline only when they hold actions.
- **Elevation.** Elevation is flat. Only bottom sheets lift, using `shadow-sheet` over `scrim`.
- **Focus.** Draw a solid 2px `focus` ring 2px outside the control.
- **Buttons.** Use at most one primary (an `accent` fill with `on-accent` text, 52px tall) per screen. Secondary buttons have a `border-control` outline with `ink` text. Tertiary buttons are text-only in `ink-2`.
- **Check-in ring.** This 32px circle is the one-tap Done control. It has a 1.5px `border-control` ring when open and an `accent` fill with an `on-accent` check when done. The same control appears on Home and in each section, and checking it in one place updates both.

## Iconography

Use simple outline icons on a 24px grid with a 1.75px stroke and round caps and joins. They are drawn in `currentColor` (`ink` or `ink-2`) and shown at 20px in rows and 24px in nav bars. The set is generated in `components/bundle.css` as `.ic .ic-<name>` (check, chevron-left, chevron-right, search, clock, bell, external, calendar, plus, more, pause, edit, archive, skip, reschedule, breath, habit, exercise, flame, award, sunrise, sun, moon, close, idea, sliders, chart). There are no illustrations, mascots or decorative images, and meditation results never show thumbnails.

## Navigation model

Home is the hub, so there is no tab bar. Home links to **Meditation**, **Habits** and **Exercise**, and each section opens with a back control. Habits has a segmented control (**Today**, the default, then **My habits**) and reaches **Weekly review** from My habits. Bottom sheets are used for the meditation check-in, quick capture and the habit actions menu.

## Example data (use it everywhere)

| Item | Type | Setup | State |
| --- | --- | --- | --- |
| Daily study → "Study for 30 minutes" | Habit | Mon–Fri, 7:00 p.m., reminder on | 5-day streak; this week 4 of 5 (Wed skipped) |
| Read for 10 minutes | Habit | Every day, Before bed | |
| Short walk | Habit | Every day, After lunch | |
| Stretch for 5 minutes | Habit | Every day, Morning | |
| Morning focus breath, 8 min | Meditation (YouTube, Focus) | Scheduled daily, 7:30 a.m. | 3-day streak, badge "Three in a row" |
| Full-body strength, 25 min | Exercise | Today, 6:00 p.m. | |
| Practise guitar, Cook a new recipe | Saved intentions | No schedule | |

Today is Friday 30 October.

## Out of scope

Don't design social features, an in-app player, mood tracking or flexible weekly targets.
