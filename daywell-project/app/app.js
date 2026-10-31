/* Daywell MVP: state, streak rules, router and screens. No framework, no build. */
'use strict';
const KEY = 'daywell.v1';
const $ = (s) => document.querySelector(s);
const phone = $('#phone');

/* ---------- dates & formatting ---------- */
const pad = (n) => String(n).padStart(2, '0');
const dkey = (d) => `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
const fromKey = (k) => { const [y, m, d] = k.split('-').map(Number); return new Date(y, m - 1, d); };
const addDays = (d, n) => { const x = new Date(d); x.setDate(x.getDate() + n); return x; };
const today = () => { const d = new Date(); d.setHours(0, 0, 0, 0); return d; };
const dow = (d) => (d.getDay() + 6) % 7; // Mon = 0
const DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
const DAY1 = ['M', 'T', 'W', 'T', 'F', 'S', 'S'];
const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
const WEEKDAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
const longDate = (d) => `${WEEKDAYS[d.getDay()]} ${d.getDate()} ${MONTHS[d.getMonth()]}`;
const fmtTime = (hm) => {
  let [h, m] = hm.split(':').map(Number);
  const ap = h >= 12 ? 'p.m.' : 'a.m.';
  h = h % 12 || 12;
  return `${h}:${pad(m)} ${ap}`;
};
const nowHM = () => { const n = new Date(); return `${pad(n.getHours())}:${pad(n.getMinutes())}`; };
const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const ic = (n, s = 20) => `<i class="ic ic-${n}" style="width:${s}px;height:${s}px" aria-hidden="true"></i>`;
const uid = () => Math.random().toString(36).slice(2, 9);

const ANCHORS = { 'Morning': '07:00', 'After lunch': '13:00', 'After dinner': '19:30', 'Before bed': '22:00' };
const daysLabel = (days) => {
  if (days.length === 7) return 'Every day';
  const s = [...days].sort().join('');
  if (s === '01234') return 'Mon–Fri';
  if (s === '56') return 'Weekends';
  return [...days].sort().map((d) => DAYS[d]).join(', ');
};
const whenLabel = (h) => (h.kind === 'anchor' ? h.anchor : fmtTime(h.time));

/* ---------- content catalogue (Daywell links out, never plays) ---------- */
const yt = (q) => `https://www.youtube.com/results?search_query=${encodeURIComponent(q)}`;
const sp = (q) => `https://open.spotify.com/search/${encodeURIComponent(q)}`;
const SESSIONS = [
  { id: 'mfb', title: 'Morning focus breath', type: 'Breathwork', mins: 8, source: 'YouTube', intent: 'Focus', url: yt('morning focus breathing 8 minutes'), desc: 'A short guided breathing practice to settle your attention before the day starts. Slow inhales and longer exhales, finishing with a minute of quiet.' },
  { id: 'box', title: 'Box breathing for clear thinking', type: 'Breathwork', mins: 6, source: 'YouTube', intent: 'Focus', url: yt('box breathing guided 6 minutes'), desc: 'Four counts in, hold, out, hold. A simple pattern to steady a busy mind.' },
  { id: 'sbw', title: 'Steady breath before work', type: 'Breathwork', mins: 10, source: 'Spotify', intent: 'Focus', url: sp('breathing before work'), desc: 'Ten minutes of even breathing to arrive at your desk calm and ready.' },
  { id: 'eb', title: 'Energising breath', type: 'Breathwork', mins: 4, source: 'YouTube', intent: 'Energy', url: yt('energizing breathwork 4 minutes'), desc: 'Quick, lively rounds of breath for a mid-afternoon lift.' },
  { id: 'calm', title: 'Calm body scan', type: 'Meditation', mins: 15, source: 'YouTube', intent: 'Peace', url: yt('calm body scan meditation 15 minutes'), desc: 'Move attention slowly from head to toe, softening as you go.' },
  { id: 'sleep', title: 'Wind down for sleep', type: 'Meditation', mins: 20, source: 'Spotify', intent: 'Sleep', url: sp('sleep meditation'), desc: 'A gentle guided practice to let the day go before bed.' },
  { id: 'focus10', title: 'Ten minutes of focus', type: 'Meditation', mins: 10, source: 'YouTube', intent: 'Focus', url: yt('10 minute focus meditation'), desc: 'Rest attention on the breath and return each time it wanders.' },
  { id: 'long', title: 'Deep stillness', type: 'Meditation', mins: 30, source: 'YouTube', intent: 'Peace', url: yt('30 minute guided meditation stillness'), desc: 'A longer sit for when you have time to settle fully.' },
  { id: 'aff1', title: 'Morning affirmations', type: 'Affirmations', mins: 5, source: 'YouTube', intent: 'Energy', url: yt('morning affirmations 5 minutes'), desc: 'Short, kind statements to set the tone for the day.' },
  { id: 'aff2', title: 'Affirmations for rest', type: 'Affirmations', mins: 12, source: 'Spotify', intent: 'Sleep', url: sp('affirmations for sleep'), desc: 'Quiet affirmations to ease into the evening.' },
];
const session = (id) => SESSIONS.find((s) => s.id === id);
const LENGTHS = [['u5', 'Under 5', (m) => m < 5], ['5-10', '5–10', (m) => m >= 5 && m <= 10], ['10-20', '10–20', (m) => m > 10 && m <= 20], ['20+', '20+ min', (m) => m > 20]];

/* ---------- state ---------- */
function seed() {
  const T = today();
  const created = dkey(addDays(T, -28));
  const s = {
    user: 'Alex',
    habits: [
      { id: 'stretch', name: 'Stretch', action: 'Stretch for 5 minutes', days: [0, 1, 2, 3, 4, 5, 6], kind: 'anchor', anchor: 'Morning', time: '07:00', reminder: false, rtime: '07:00', status: 'active', created },
      { id: 'walk', name: 'Short walk', action: 'Short walk', days: [0, 1, 2, 3, 4, 5, 6], kind: 'anchor', anchor: 'After lunch', time: '13:00', reminder: false, rtime: '13:00', status: 'active', created },
      { id: 'study', name: 'Daily study', action: 'Study for 30 minutes', days: [0, 1, 2, 3, 4], kind: 'time', anchor: 'After dinner', time: '19:00', reminder: true, rtime: '19:00', status: 'active', created },
      { id: 'read', name: 'Read', action: 'Read for 10 minutes', days: [0, 1, 2, 3, 4, 5, 6], kind: 'anchor', anchor: 'Before bed', time: '22:00', reminder: false, rtime: '21:45', status: 'active', created },
    ],
    meds: [{ id: 'mfb', sessionId: 'mfb', time: '07:30', created }],
    workouts: [{ id: 'fbs', title: 'Full-body strength', mins: 25, time: '18:00', created }],
    log: {},
    extra: {},
    ideas: ['Practise guitar', 'Cook a new recipe'],
    badges: [{ name: 'A full week', desc: 'Seven days in a row of Stretch for 5 minutes.', date: dkey(addDays(T, -14)) }],
    reflections: {},
    pending: null,
  };
  // history: build each item's recent past so the streaks match the brief
  const setLog = (d, id, st, at) => { const k = dkey(d); (s.log[k] = s.log[k] || {})[id] = { s: st, at }; };
  const past = (h, n, fn) => { // walk back over scheduled days, fn(index, date)
    let i = 0;
    for (let back = 1; back <= 27; back++) { const d = addDays(T, -back); if (h.days.includes(dow(d))) fn(i++, d); }
  };
  const H = Object.fromEntries(s.habits.map((h) => [h.id, h]));
  past(H.study, 0, (i, d) => { if (i >= 6) return; setLog(d, 'h:study', i === 2 ? 'skip' : 'done', '19:20'); }); // 5-day streak, one skip
  past(H.read, 0, (i, d) => { if (i >= 9) return; setLog(d, 'h:read', i === 2 ? 'skip' : 'done', '22:10'); });
  past(H.walk, 0, (i, d) => { if (i >= 8) return; setLog(d, 'h:walk', i === 1 ? 'resched' : 'done', '13:25'); });
  past(H.stretch, 0, (i, d) => { if (i >= 7) return; setLog(d, 'h:stretch', 'done', '07:05'); });
  setLog(addDays(T, -1), 'm:mfb', 'done', '07:41');
  setLog(addDays(T, -2), 'm:mfb', 'done', '07:38');
  setLog(T, 'h:stretch', 'done', '07:05');
  return s;
}
let S;
try { S = JSON.parse(localStorage.getItem(KEY)) || seed(); } catch { S = seed(); }
const save = () => localStorage.setItem(KEY, JSON.stringify(S));

const ui = { tab: 'today', medType: 'Breathwork', q: '', intent: null, len: null, sheet: null, draft: null, flash: null, back: '#home' };

/* ---------- items & streak rules ---------- */
// Items scheduled on a date across the app: habits, scheduled meditations, workouts.
function itemsOn(d) {
  const k = dkey(d), wd = dow(d), out = [];
  for (const h of S.habits) {
    if (h.status !== 'active' || h.created > k) continue;
    const extra = (S.extra[k] || []).includes('h:' + h.id);
    if (h.days.includes(wd) || extra) out.push({ id: 'h:' + h.id, kind: 'habit', title: h.action, when: whenLabel(h), sort: h.kind === 'anchor' ? ANCHORS[h.anchor] : h.time, ref: h });
  }
  for (const m of S.meds) {
    if (m.created > k || (m.once && m.created !== k)) continue;
    const se = session(m.sessionId);
    out.push({ id: 'm:' + m.id, kind: 'meditation', title: se.title, when: fmtTime(m.time), sort: m.time, ref: se });
  }
  for (const w of S.workouts) {
    if (w.created > k) continue;
    out.push({ id: 'w:' + w.id, kind: 'exercise', title: w.title, when: fmtTime(w.time), sort: w.time, ref: w });
  }
  return out.sort((a, b) => a.sort.localeCompare(b.sort));
}
const isScheduled = (id, d) => itemsOn(d).some((i) => i.id === id);
const status = (id, d = today()) => (S.log[dkey(d)] || {})[id];

// Done adds a day. Skip and Reschedule keep the streak. A scheduled day with nothing by midnight is missed.
function streak(id) {
  const T = today();
  let n = 0;
  for (let back = 0; back < 400; back++) {
    const d = addDays(T, -back);
    if (!isScheduled(id, d)) { if (back > 60 && n === 0) break; continue; }
    const st = status(id, d);
    if (st && st.s === 'done') n++;
    else if (st) continue;
    else if (back === 0) continue; // today isn't over yet
    else break;
  }
  return n;
}

const BADGES = [[3, 'Three in a row', (t) => `Three days in a row of ${t}.`], [7, 'A full week', (t) => `Seven days in a row of ${t}.`], [30, 'A steady month', (t) => `Thirty days in a row of ${t}.`]];
function checkIn(id, st, d = today()) {
  const k = dkey(d);
  S.log[k] = S.log[k] || {};
  const prev = S.log[k][id];
  // Undo a reschedule: drop the copy we added to tomorrow
  if (prev && prev.s === 'resched') { const t = dkey(addDays(d, 1)); S.extra[t] = (S.extra[t] || []).filter((x) => x !== id); }
  if (st === null) delete S.log[k][id];
  else S.log[k][id] = { s: st, at: nowHM() };
  if (st === 'resched') { const t = dkey(addDays(d, 1)); S.extra[t] = [...new Set([...(S.extra[t] || []), id])]; }
  let badge = null;
  if (st === 'done') {
    const n = streak(id);
    const item = itemsOn(d).find((i) => i.id === id);
    for (const [need, name, desc] of BADGES) {
      if (n === need && !S.badges.some((b) => b.name === name)) { badge = { name, desc: desc(item ? item.title : 'this'), date: k }; S.badges.push(badge); }
    }
  }
  save();
  return badge;
}

function bestHabitStreak() {
  let best = null;
  for (const h of S.habits) if (h.status === 'active') { const n = streak('h:' + h.id); if (!best || n > best.n) best = { n, h }; }
  return best;
}

/* ---------- shared bits ---------- */
const nav = (title, { back = '#home', right = '<span style="width:44px"></span>' } = {}) =>
  `<div class="dw-nav"><a class="dw-iconbtn" href="${back}" aria-label="Back">${ic('chevron-left', 24)}</a><div class="dw-navtitle t-heading">${title}</div>${right}</div>`;
const leadIcon = { habit: 'habit', meditation: 'breath', exercise: 'exercise' };
const kindLabel = { habit: 'Habit', meditation: 'Meditation', exercise: 'Exercise' };
const ring = (id, done) => `<button class="dw-check${done ? ' is-done' : ''}" data-a="ring" data-id="${id}" aria-label="${done ? 'Done. Tap to undo' : 'Mark as done'}"><span>${ic('check', 18)}</span></button>`;
const meta = (parts) => `<div class="dw-meta t-caption">${parts.filter(Boolean).join('<span class="sep">·</span>')}</div>`;
const flame = (n) => (n > 0 ? `<span class="dw-streak">${ic('flame', 14)}${n}</span>` : '');
const stLabel = (st) => (st.s === 'done' ? `Done ${fmtTime(st.at)}` : st.s === 'skip' ? 'Skipped. Streak kept' : 'Rescheduled to tomorrow. Streak kept');

/* ---------- screens ---------- */
function Home() {
  const T = today(), items = itemsOn(T);
  const done = items.filter((i) => status(i.id)?.s === 'done').length;
  const h = new Date().getHours();
  const greet = h < 12 ? 'Good morning' : h < 18 ? 'Good afternoon' : 'Good evening';
  const sub = done === 0 ? 'Here is your day.' : done === items.length ? 'All done for today. Well kept.' : `${done} of ${items.length} done. ${done / items.length < 0.5 ? 'A good start.' : 'Nicely going.'}`;
  const best = bestHabitStreak();
  const badge = S.badges[S.badges.length - 1];
  const rows = items.map((i) => {
    const st = status(i.id);
    const n = i.kind !== 'exercise' ? streak(i.id) : 0;
    const extra = i.kind === 'meditation' ? `${i.ref.mins} min` : i.kind === 'exercise' ? `${i.ref.mins} min` : null;
    return `<li class="dw-item${st ? (st.s === 'done' ? ' is-done' : ' is-kept') : ''}"><span class="dw-lead">${ic(leadIcon[i.kind])}</span>
      <div class="grow"><div class="t-body-strong">${esc(i.title)}</div>${meta([kindLabel[i.kind], extra, st ? stLabel(st) : i.when, !st && n ? flame(n) : ''])}</div>${ring(i.id, st?.s === 'done')}</li>`;
  }).join('');
  return `<div class="dw-body">
    <div class="mt3 t-overline up c-ink3">${longDate(T)}</div>
    <h1 class="t-display mt1">${greet}, ${esc(S.user)}</h1>
    <p class="t-body c-ink2 mt1">${sub}</p>
    <div class="dw-sechead"><h2 class="t-heading">Today</h2><span class="t-caption c-ink3">${items.length} items</span></div>
    <ul class="dw-list">${rows || '<li class="empty t-body">Nothing scheduled today.</li>'}</ul>
    <div class="dw-strip mt4">
      <button data-go="#habits"><div class="t-caption">Streak</div><div class="t-numeral mt1">${best ? `${best.n} ${best.n === 1 ? 'day' : 'days'}` : '–'}</div><div class="t-caption c-ink3">${best ? esc(best.h.name) : ''}</div></button>
      <button data-go="#habits"><div class="t-caption">Today</div><div class="t-numeral mt1">${done} of ${items.length}</div><div class="dw-bar"><i style="width:${items.length ? Math.round((done / items.length) * 100) : 0}%"></i></div></button>
      <button data-a="badges"><div class="t-caption">Latest badge</div><div class="row mt2"><span class="c-accent">${ic('award', 22)}</span><span class="t-label">${badge ? esc(badge.name) : 'None yet'}</span></div></button>
    </div>
    <div class="dw-entries mt3">
      <button class="dw-entry" data-go="#med">${ic('breath', 22)}<span class="t-label">Meditation</span></button>
      <button class="dw-entry" data-go="#habits">${ic('habit', 22)}<span class="t-label">Habits</span></button>
      <button class="dw-entry" disabled title="Coming soon">${ic('exercise', 22)}<span class="t-label">Exercise · Soon</span></button>
    </div>
  </div>`;
}

const groupOf = (i) => (i.sort < '12:00' ? 0 : i.sort < '17:00' ? 1 : 2);
const GROUPS = [['sunrise', 'Morning'], ['sun', 'During the day'], ['moon', 'Evening']];

function Habits() {
  const seg = `<div class="dw-seg mt2"><button class="t-label${ui.tab === 'today' ? ' on' : ''}" data-a="tab" data-v="today">Today</button><button class="t-label${ui.tab === 'mine' ? ' on' : ''}" data-a="tab" data-v="mine">My habits</button></div>`;
  const top = nav('Habits', { right: `<button class="dw-iconbtn" data-a="newHabit" aria-label="New habit">${ic('plus', 24)}</button>` });
  return `<div class="dw-body">${top}${seg}${ui.tab === 'today' ? HabitsToday() : MyHabits()}</div>`;
}

function HabitsToday() {
  const T = today(), items = itemsOn(T).filter((i) => i.kind === 'habit');
  const closed = items.filter((i) => status(i.id)).length;
  const done = items.filter((i) => status(i.id)?.s === 'done').length;
  let html = `<div class="between mt5"><span class="t-label c-ink2">${longDate(T)}</span><span class="t-label c-accent">${done} of ${items.length} done</span></div>`;
  if (items.length && closed === items.length) {
    html += `<div class="allDone"><div class="dw-bigcheck">${ic('check', 32)}</div><h2 class="t-title mt5">All done for today</h2><p class="t-body c-ink2 mt2">Every habit is checked off. Enjoy the rest of your day.</p></div>`;
  }
  if (!items.length) return html + `<p class="empty t-body">No habits today. Tap + to make one.</p>`;
  GROUPS.forEach(([icon, label], g) => {
    const gi = items.filter((i) => groupOf(i) === g);
    if (!gi.length) return;
    html += `<div class="dw-group">${ic(icon)}<span class="t-overline up">${label}</span></div><ul class="dw-list">`;
    for (const i of gi) {
      const st = status(i.id), n = streak(i.id);
      html += `<li class="dw-item${st ? (st.s === 'done' ? ' is-done' : ' is-kept') : ''}" style="display:block;padding:14px 0 10px">
        <div class="between"><div class="grow"><div class="t-body-strong">${esc(i.title)}</div>${meta([i.when, flame(n)])}</div>${ring(i.id, st?.s === 'done')}</div>
        ${st ? `<div class="row mt1"><span class="t-caption c-accent">${stLabel(st)}</span><span class="t-caption" style="color:var(--line-2)">·</span><button class="t-caption link" data-a="undo" data-id="${i.id}">Undo</button></div>`
          : `<div class="row mt2" style="gap:4px;margin-left:-12px"><button class="dw-sbtn" data-a="st" data-v="done" data-id="${i.id}">${ic('check', 16)}Done</button><button class="dw-sbtn" data-a="st" data-v="skip" data-id="${i.id}">${ic('skip', 16)}Skip</button><button class="dw-sbtn" data-a="st" data-v="resched" data-id="${i.id}">${ic('reschedule', 16)}Reschedule</button></div>`}
      </li>`;
    }
    html += '</ul>';
  });
  return html;
}

function nextDue(h) {
  const T = today();
  for (let i = 0; i < 8; i++) {
    const d = addDays(T, i);
    if (!h.days.includes(dow(d))) continue;
    if (i === 0 && status('h:' + h.id)) continue;
    return i === 0 ? 'Today' : i === 1 ? 'Tomorrow' : WEEKDAYS[d.getDay()];
  }
  return '–';
}

function MyHabits() {
  const T = today(), wd = dow(T);
  const wk = addDays(T, -wd);
  const sunday = wd === 6 && new Date().getHours() >= 18;
  let html = `<a class="dw-panel mt5 between" href="#review" style="display:flex;text-decoration:none;color:inherit"><span class="row"><span class="c-accent">${ic('chart')}</span><span><span class="t-body-strong" style="display:block">Weekly review</span><span class="t-caption c-ink2">${sunday ? 'Ready for this week' : 'Week so far'} · ${wk.getDate()} ${MONTHS[wk.getMonth()].slice(0, 3)} – ${addDays(wk, 6).getDate()} ${MONTHS[addDays(wk, 6).getMonth()].slice(0, 3)}</span></span></span>${ic('chevron-right')}</a>`;
  const active = S.habits.filter((h) => h.status === 'active');
  const order = ['Morning', 'During the day', 'Evening'];
  const routine = (h) => order[groupOf({ sort: h.kind === 'anchor' ? ANCHORS[h.anchor] : h.time })];
  const row = (h, paused) => `<li class="dw-item"><span class="dw-lead">${ic(paused ? 'pause' : 'habit')}</span><div class="grow"><div class="t-body-strong"${paused ? ' style="color:var(--ink-3)"' : ''}>${esc(h.action)}</div>
      ${meta([daysLabel(h.days) + ' · ' + whenLabel(h), paused ? `Paused · streak held at ${streak('h:' + h.id)}` : `Next: ${nextDue(h)}`, !paused ? flame(streak('h:' + h.id)) : ''])}</div>
      <button class="dw-iconbtn" style="width:44px;height:44px;display:flex;align-items:center;justify-content:center" data-a="menu" data-id="${h.id}" aria-label="More for ${esc(h.action)}">${ic('more')}</button></li>`;
  for (const g of order) {
    const hs = active.filter((h) => routine(h) === g);
    if (!hs.length) continue;
    html += `<div class="dw-group"><span class="t-overline up">${g}</span></div><ul class="dw-list">${hs.map((h) => row(h)).join('')}</ul>`;
  }
  if (!active.length) html += `<p class="empty t-body">No active habits yet.</p>`;
  const paused = S.habits.filter((h) => h.status === 'paused');
  if (paused.length) html += `<div class="dw-group"><span class="t-overline up">Paused</span></div><ul class="dw-list">${paused.map((h) => row(h, true)).join('')}</ul>`;
  html += `<div class="dw-sechead"><h2 class="t-heading">Ideas to turn into habits</h2><button class="dw-sbtn" data-a="capture">${ic('plus', 16)}Add</button></div>
    <ul class="dw-list">${S.ideas.map((t, i) => `<li class="dw-item"><span class="dw-lead">${ic('idea')}</span><div class="grow t-body">${esc(t)}</div><button class="dw-sbtn outline" data-a="ideaToHabit" data-i="${i}">Make it a habit</button></li>`).join('') || '<li class="empty t-caption">Save ideas here without a schedule.</li>'}</ul>`;
  return html;
}

/* create / edit habit */
function blankDraft(name = '') {
  return { id: null, name, action: '', days: [0, 1, 2, 3, 4, 5, 6], every: true, kind: 'time', time: '19:00', anchor: 'Morning', reminder: true, rtime: '07:00', fromIdea: null };
}
function suggestions(name) {
  const n = name.trim();
  if (!n) return [];
  const base = n.replace(/^daily\s+/i, '').replace(/^(\w)/, (c) => c.toUpperCase());
  return [`${base} for 10 minutes`, `${base} for 30 minutes`, `${base} for 5 minutes`, `${base} once`];
}
function NewStep1() {
  const d = ui.draft;
  const sug = suggestions(d.name);
  return `<div class="dw-body">
    <div class="dw-nav"><a class="dw-iconbtn" href="${ui.back}" aria-label="Back">${ic('close', 22)}</a><div class="dw-steps"><i class="on"></i><i></i></div><span class="t-label c-ink3" style="width:44px;text-align:right;padding-right:12px">1/2</span></div>
    <h1 class="t-title mt5">Make it specific.</h1>
    <p class="t-body c-ink2 mt1">Small and concrete is easier to keep.</p>
    <label class="dw-label t-label mt6" for="f-name">Name</label>
    <div class="dw-field"><input id="f-name" data-f="name" placeholder="For example, Daily study" value="${esc(d.name)}" autocomplete="off"></div>
    <label class="dw-label t-label mt5" for="f-action">What exactly will you do?</label>
    <div class="dw-field"><input id="f-action" data-f="action" placeholder="For example, Study for 30 minutes" value="${esc(d.action)}" autocomplete="off"></div>
    ${sug.length ? `<div class="t-overline up c-ink3 mt5">Suggestions</div><div class="dw-chips mt2">${sug.map((s) => `<button class="dw-chip t-label${d.action === s ? ' on' : ''}" data-a="sug" data-v="${esc(s)}">${esc(s)}</button>`).join('')}</div>` : ''}
  </div><div class="foot"><button class="dw-btn primary" data-a="step2" ${d.name.trim() ? '' : 'disabled'}>Next</button></div>`;
}
function NewStep2() {
  const d = ui.draft;
  const action = d.action.trim() || d.name.trim();
  const summary = `${esc(action)} · ${daysLabel(d.days)} · ${d.kind === 'anchor' ? d.anchor : fmtTime(d.time)}`;
  return `<div class="dw-body">
    <div class="dw-nav"><a class="dw-iconbtn" href="#new/1" aria-label="Back">${ic('chevron-left', 24)}</a><div class="dw-steps"><i class="on"></i><i class="on"></i></div><span class="t-label c-ink3" style="width:44px;text-align:right;padding-right:12px">2/2</span></div>
    <h1 class="t-title mt5">When would you like to do it?</h1>
    <p class="t-caption c-ink2 mt1">${esc(action)}</p>
    <div class="dw-seg mt5"><button class="t-label${d.every ? ' on' : ''}" data-a="every" data-v="1">Every day</button><button class="t-label${!d.every ? ' on' : ''}" data-a="every" data-v="0">Selected days</button></div>
    <div class="dw-days mt3">${DAY1.map((l, i) => `<button class="t-label${d.days.includes(i) ? ' on' : ''}" data-a="day" data-v="${i}" aria-label="${DAYS[i]}" aria-pressed="${d.days.includes(i)}">${l}</button>`).join('')}</div>
    <div class="dw-seg mt6"><button class="t-label${d.kind === 'time' ? ' on' : ''}" data-a="kind" data-v="time">At a time</button><button class="t-label${d.kind === 'anchor' ? ' on' : ''}" data-a="kind" data-v="anchor">With a routine</button></div>
    ${d.kind === 'time'
      ? `<label class="dw-field mt3 between"><span class="row">${ic('clock')}<span class="t-body">Time</span></span><input type="time" data-f="time" value="${d.time}"></label>
         <div class="between mt4" style="min-height:52px;border-bottom:1px solid var(--line)"><span class="row c-ink2">${ic('bell')}<span class="t-body" style="color:var(--ink)">Remind me at ${fmtTime(d.time)}</span></span><button class="dw-toggle${d.reminder ? ' on' : ''}" data-a="rem" role="switch" aria-checked="${d.reminder}" aria-label="Reminder"></button></div>`
      : `<div class="mt3">${Object.keys(ANCHORS).map((a) => `<button class="dw-opt" data-a="anchor" data-v="${a}"><span class="dw-radio${d.anchor === a ? ' on' : ''}"></span><span class="t-body">${a}</span></button>`).join('')}</div>
         <div class="between mt3" style="min-height:52px;border-bottom:1px solid var(--line)"><span class="row c-ink2">${ic('bell')}<span class="t-body" style="color:var(--ink)">Reminder (optional)</span></span><button class="dw-toggle${d.reminder ? ' on' : ''}" data-a="rem" role="switch" aria-checked="${d.reminder}" aria-label="Reminder"></button></div>
         ${d.reminder ? `<label class="dw-field mt3 between"><span class="row">${ic('clock')}<span class="t-body">Remind me at</span></span><input type="time" data-f="rtime" value="${d.rtime}"></label>` : ''}`}
  </div><div class="foot"><p class="t-caption c-ink2" style="text-align:center;margin-bottom:12px">${summary}</p><button class="dw-btn primary" data-a="saveHabit" ${d.days.length ? '' : 'disabled'}>Save</button></div>`;
}

/* meditation */
function Med() {
  const types = ['Meditation', 'Breathwork', 'Affirmations'];
  const q = ui.q.trim().toLowerCase();
  const lenFn = ui.len ? LENGTHS.find((l) => l[0] === ui.len)[2] : () => true;
  const res = SESSIONS.filter((s) => s.type === ui.medType && (!ui.intent || s.intent === ui.intent) && lenFn(s.mins) && (!q || s.title.toLowerCase().includes(q)));
  const chip = (a, v, label, on) => `<button class="dw-chip t-label${on ? ' on' : ''}" data-a="${a}" data-v="${v}" aria-pressed="${on}">${label}</button>`;
  return `<div class="dw-body">${nav('Meditation')}
    <div class="dw-chips mt2">${types.map((t) => chip('medType', t, t, ui.medType === t)).join('')}</div>
    <label class="dw-field search mt4">${ic('search')}<input id="f-q" data-f="q" placeholder="Search ${ui.medType.toLowerCase()}" value="${esc(ui.q)}" autocomplete="off"></label>
    <div class="t-overline up c-ink3 mt5">Intention</div>
    <div class="dw-chips mt2">${['Peace', 'Focus', 'Sleep', 'Energy'].map((t) => chip('intent', t, t, ui.intent === t)).join('')}</div>
    <div class="t-overline up c-ink3 mt4">Length</div>
    <div class="dw-chips mt2">${LENGTHS.map(([k, l]) => chip('len', k, l, ui.len === k)).join('')}</div>
    <div class="between mt5"><span class="t-caption c-ink2">${res.length} ${res.length === 1 ? 'session' : 'sessions'}</span>${ui.intent || ui.len || ui.q ? '<button class="t-label c-ink2" data-a="clear">Clear filters</button>' : ''}</div>
    <ul class="dw-list">${res.map((s) => `<li class="mt2"><a class="dw-card" href="#med/${s.id}" style="text-decoration:none;color:inherit"><div class="t-body-strong">${esc(s.title)}</div>
      <div class="dw-meta t-caption mt1"><span class="row" style="gap:4px">${ic('clock', 14)}${s.mins} min</span><span class="sep">·</span>${s.source}</div>
      <div class="row mt3"><span class="dw-tag t-caption">${s.intent}</span><span class="dw-tag t-caption">${s.type}</span></div></a></li>`).join('') || '<li class="empty t-body">No sessions match. Try fewer filters.</li>'}</ul>
  </div>`;
}

function SessionDetail(id) {
  const s = session(id);
  if (!s) return Med();
  const sched = S.meds.find((m) => m.sessionId === id);
  const n = sched ? streak('m:' + sched.id) : 0;
  return `<div class="dw-body">${nav('', { back: '#med' })}
    <div class="t-overline up c-ink3 mt3">${s.type}</div>
    <h1 class="t-title mt1">${esc(s.title)}</h1>
    <div class="dw-meta t-body mt2"><span class="row" style="gap:4px">${ic('clock', 16)}${s.mins} min</span><span class="sep">·</span>${s.source}<span class="sep">·</span>${s.intent}</div>
    <p class="t-body c-ink2 mt5">${esc(s.desc)}</p>
    ${sched ? `<div class="dw-panel mt6"><div class="between"><div class="row"><span class="c-ink2">${ic('calendar')}</span><span class="t-label">Scheduled</span></div><span class="t-label c-ink2">Every day · ${fmtTime(sched.time)}</span></div></div>
      <div class="dw-panel mt2"><div class="between"><div class="row"><span class="c-accent">${ic('flame')}</span><span class="t-label">Your streak</span></div><span class="t-label c-accent">${n} ${n === 1 ? 'day' : 'days'}</span></div></div>` : ''}
  </div><div class="foot">
    <button class="dw-btn primary" data-a="start" data-id="${s.id}">Start on ${s.source} ${ic('external', 18)}</button>
    <p class="t-caption c-ink2 mt2" style="text-align:center">This opens ${s.source}. Come back to log it.</p>
    <button class="dw-btn secondary mt4" data-a="${sched ? 'unschedule' : 'schedule'}" data-id="${s.id}">${ic('calendar', 18)}${sched ? 'Remove from schedule' : 'Schedule for later'}</button>
  </div>`;
}

function Completion() {
  const f = ui.flash;
  if (!f) { location.hash = '#home'; return ''; }
  const id = f.id, n = streak(id);
  const T = today();
  const dots = [-4, -3, -2, -1, 0].map((o) => {
    const d = addDays(T, o), st = status(id, d);
    const c = st ? (st.s === 'done' ? 'd' : 'k') : 'm';
    return `<div style="display:flex;flex-direction:column;align-items:center;gap:6px"><span class="t-caption c-ink3">${DAYS[dow(d)]}</span><span class="dw-dots"><i class="${c}"></i></span></div>`;
  }).join('');
  return `<div class="dw-body" data-a="closeDone" style="cursor:pointer">
    <div class="dw-nav"><span style="width:44px"></span><div class="dw-navtitle"></div><button class="dw-iconbtn" data-a="closeDone" aria-label="Close">${ic('close', 22)}</button></div>
    <div style="display:flex;flex-direction:column;align-items:center;text-align:center;margin-top:40px"><div class="dw-bigcheck">${ic('check', 32)}</div><h1 class="t-display mt6">Nicely done</h1><p class="t-body c-ink2 mt2">${esc(f.title)}${f.mins ? ` · ${f.mins} min logged` : ' logged'}</p></div>
    <div class="dw-panel mt8"><div class="t-caption c-ink2">${f.kind === 'meditation' ? 'Meditation streak' : 'Streak'}</div><div class="t-numeral mt1 c-accent">${n} ${n === 1 ? 'day' : 'days'}</div><div class="row mt3" style="justify-content:space-between">${dots}</div></div>
    ${f.badge ? `<div class="dw-tint mt3"><div class="row" style="gap:16px"><span class="dw-badge">${ic('award', 26)}</span><div><div class="t-caption c-accent">New badge</div><div class="t-body-strong">${esc(f.badge.name)}</div><div class="t-caption c-ink2">${esc(f.badge.desc)}</div></div></div></div>` : ''}
  </div><div class="foot"><button class="dw-btn primary" data-go="#home">Back to Today</button></div>`;
}

/* weekly review */
function weekRows() {
  const T = today(), start = addDays(T, -dow(T));
  return S.habits.filter((h) => h.status === 'active').map((h) => {
    const id = 'h:' + h.id;
    let done = 0, due = 0, skipped = 0, resched = 0, dots = '';
    for (let i = 0; i < 7; i++) {
      const d = addDays(start, i);
      if (!isScheduled(id, d)) continue;
      const st = status(id, d), future = d > T;
      if (!future && (+d !== +T || st)) due++; // today only counts once it's checked in
      if (st?.s === 'done') { done++; dots += '<i class="d"></i>'; }
      else if (st) { st.s === 'skip' ? skipped++ : resched++; dots += '<i class="k"></i>'; }
      else dots += future ? '<i class="n"></i>' : +d === +T ? '<i class="t"></i>' : '<i class="m"></i>';
    }
    return { h, done, due, skipped, resched, dots, ratio: due ? done / due : 1 };
  });
}
function Review() {
  const T = today(), start = addDays(T, -dow(T)), end = addDays(start, 6);
  const rows = weekRows();
  const missedAny = rows.some((r) => r.dots.includes('class="m"'));
  const low = rows.filter((r) => r.due && r.ratio < 1).sort((a, b) => a.ratio - b.ratio)[0];
  let tweak = '';
  if (low) {
    const h = low.h;
    const kept = low.skipped + low.resched;
    const earlier = h.kind === 'time' ? `${pad(Math.max(5, Number(h.time.slice(0, 2)) - 1))}:${h.time.slice(3)}` : null;
    tweak = `<div class="dw-tint mt5"><div class="t-caption c-accent">Needs a tweak</div><div class="t-body-strong mt1">${esc(h.name)}</div><div class="t-caption c-ink2">${esc(h.action)} · ${daysLabel(h.days)} · ${whenLabel(h)}</div>
      <div class="between mt3"><span class="dw-dots">${low.dots}</span><span class="t-label">${low.done} of ${low.due} days</span></div>
      <p class="t-body mt3">${kept ? `${kept === 1 ? 'One day was' : kept + ' days were'} skipped or rescheduled.` : 'A few days slipped.'} ${earlier ? `Would ${fmtTime(earlier)} be easier than ${fmtTime(h.time)}?` : 'Would a different time be easier?'}</p>
      <button class="dw-btn primary mt4" style="height:48px" data-a="${earlier ? 'changeTime' : 'edit'}" data-id="${h.id}" data-v="${earlier || ''}">${ic('clock', 18)}${earlier ? `Change time to ${fmtTime(earlier)}` : 'Change time'}</button>
      <div class="row mt2" style="gap:8px"><button class="dw-btn secondary grow" style="height:44px;background:var(--bg)" data-a="pause" data-id="${h.id}">${ic('pause', 18)}Pause</button><button class="dw-btn secondary grow" style="height:44px;background:var(--bg)" data-a="archive" data-id="${h.id}">${ic('archive', 18)}Archive</button></div></div>`;
  }
  const fmtD = (d) => `${d.getDate()} ${MONTHS[d.getMonth()]}`;
  const wk = dkey(start);
  return `<div class="dw-body">${nav('Weekly review', { back: '#habits/mine' })}
    <div class="t-overline up c-ink3 mt3">${fmtD(start)} – ${fmtD(end)}</div>
    <h1 class="t-title mt1">${missedAny ? 'A week with a few gaps.' : 'A steady week.'}</h1>
    <p class="t-body c-ink2 mt1">${missedAny ? 'That happens. Small adjustments help more than trying harder.' : 'Every habit kept its streak this week.'}</p>
    ${tweak}
    <div class="dw-sechead"><h2 class="t-heading">This week</h2><span class="t-caption c-ink3">Mon–Sun</span></div>
    <ul class="dw-list">${rows.map((r) => `<li class="dw-item"><div class="grow"><div class="t-body-strong">${esc(r.h.action)}</div>${meta([daysLabel(r.h.days) + ' · ' + whenLabel(r.h)])}</div>
      <div style="text-align:right"><span class="dw-dots" style="justify-content:flex-end">${r.dots}</span><div class="t-caption c-ink2 mt1">${r.done} of ${r.due} days${r.skipped ? ` · ${r.skipped} skipped` : ''}${r.resched ? ` · ${r.resched} rescheduled` : ''}</div></div></li>`).join('')}</ul>
    ${S.ideas.length ? `<div class="dw-sechead"><h2 class="t-heading">Turn one into a habit?</h2></div><div class="dw-chips mt2">${S.ideas.map((t, i) => `<button class="dw-chip t-label" data-a="ideaToHabit" data-i="${i}">${ic('plus', 16)}${esc(t)}</button>`).join('')}</div>` : ''}
    <div class="dw-sechead"><h2 class="t-heading">Which habits felt manageable?</h2></div>
    <textarea class="dw-textarea mt2" id="f-refl" data-f="refl" rows="4" placeholder="A few words for yourself. Only you see this.">${esc(S.reflections[wk] || '')}</textarea>
    <p class="t-caption c-ink3 mt2">Saved as you type.</p>
  </div>`;
}

/* ---------- sheets ---------- */
function Sheet() {
  const s = ui.sheet;
  if (!s) return '';
  let inner = '';
  if (s.type === 'checkin') {
    const se = session(s.sessionId);
    inner = `<div class="t-overline up c-ink3">Welcome back</div><h2 class="t-title mt2">Did you complete ${esc(se.title)}?</h2><p class="t-body c-ink2 mt2">${se.mins} min · ${se.source}</p>
      <button class="dw-btn primary mt6" data-a="ciDone">${ic('check', 18)}Done</button>
      <button class="dw-btn secondary mt3" data-a="ciNot">Not this time</button>
      <button class="dw-btn tertiary mt2" data-a="ciLater">${ic('bell', 18)}Remind me later</button>
      <p class="t-caption c-ink3 mt3" style="text-align:center">Your word is enough. No timer, no proof.</p>`;
  } else if (s.type === 'capture') {
    inner = `<h2 class="t-heading">What would you like to make a habit?</h2>
      <div class="dw-field mt4"><input id="f-idea" data-f="idea" placeholder="For example, Practise guitar" value="${esc(s.text || '')}" autocomplete="off"></div>
      <p class="t-caption c-ink2 mt2">Saved as an idea. No schedule needed yet.</p>
      <button class="dw-btn primary mt5" data-a="saveIdea">Save</button>`;
  } else if (s.type === 'menu') {
    const h = S.habits.find((x) => x.id === s.id);
    const paused = h.status === 'paused';
    inner = `<div class="t-overline up c-ink3">Habit</div><h2 class="t-heading mt1">${esc(h.action)}</h2><div class="mt4">
      <button class="dw-opt" data-a="${paused ? 'resume' : 'pause'}" data-id="${h.id}">${ic(paused ? 'reschedule' : 'pause')}<span class="t-body">${paused ? 'Resume' : 'Pause'}</span></button>
      <button class="dw-opt" data-a="edit" data-id="${h.id}">${ic('edit')}<span class="t-body">Edit</span></button>
      <button class="dw-opt" data-a="archive" data-id="${h.id}">${ic('archive')}<span class="t-body">Archive</span></button></div>
      <p class="t-caption c-ink3 mt3">${paused ? 'Resuming picks the streak up where it was.' : 'Pausing freezes the streak. Archive keeps its history.'}</p>`;
  } else if (s.type === 'schedule') {
    const se = session(s.sessionId);
    inner = `<div class="t-overline up c-ink3">Schedule for later</div><h2 class="t-heading mt1">${esc(se.title)}</h2>
      <p class="t-body c-ink2 mt1">Add it to Today, every day at:</p>
      <label class="dw-field mt4 between"><span class="row">${ic('clock')}<span class="t-body">Time</span></span><input type="time" data-f="stime" value="${s.time}"></label>
      <button class="dw-btn primary mt5" data-a="saveSchedule">Add to Today</button>`;
  } else if (s.type === 'badges') {
    inner = `<h2 class="t-heading">Your badges</h2><ul class="dw-list mt2">${[...S.badges].reverse().map((b) => `<li class="dw-item"><span class="dw-badge" style="width:44px;height:44px">${ic('award', 22)}</span><div class="grow"><div class="t-body-strong">${esc(b.name)}</div><div class="t-caption c-ink2">${esc(b.desc)}</div></div></li>`).join('') || '<li class="empty t-body">None yet. Three days in a row earns the first.</li>'}</ul>`;
  }
  return `<div class="dw-scrim" data-a="closeSheet"></div><div class="dw-sheet" role="dialog" aria-modal="true"><div class="dw-grab"></div>${inner}</div>`;
}

/* ---------- router & render ---------- */
function route() {
  const h = location.hash || '#home';
  if (h === '#habits') ui.tab = 'today';
  if (h === '#habits/mine') ui.tab = 'mine';
  if (h.startsWith('#habits')) return Habits();
  if (h === '#new/1') return ui.draft ? NewStep1() : (location.hash = '#habits', '');
  if (h === '#new/2') return ui.draft ? NewStep2() : (location.hash = '#habits', '');
  if (h === '#med') return Med();
  if (h.startsWith('#med/')) return SessionDetail(h.slice(5));
  if (h === '#done') return Completion();
  if (h === '#review') return Review();
  return Home();
}
let lastHash = null;
function render() {
  const a = document.activeElement;
  const focusId = a && a.id && a.id.startsWith('f-') ? a.id : null;
  const sel = focusId ? [a.selectionStart, a.selectionEnd] : null;
  const prev = phone.querySelector('.dw-body');
  const scroll = prev && lastHash === location.hash ? prev.scrollTop : 0;
  lastHash = location.hash;
  const n = new Date();
  phone.innerHTML = `<div class="dw-status"><b>${n.getHours()}:${pad(n.getMinutes())}</b><div class="dw-batt"><s><u style="height:4px"></u><u style="height:6px"></u><u style="height:8px"></u><u style="height:11px"></u></s><i></i></div></div>${route()}${Sheet()}<div class="dw-homebar"></div>`;
  const body = phone.querySelector('.dw-body');
  if (body) body.scrollTop = scroll;
  if (focusId) { const el = document.getElementById(focusId); if (el) { el.focus(); try { el.setSelectionRange(...sel); } catch {} } }
}
const go = (h) => { if (location.hash === h) render(); else location.hash = h; };

/* ---------- actions ---------- */
function itemTitle(id) { const i = itemsOn(today()).find((x) => x.id === id); return i; }
function markDone(id) {
  const item = itemTitle(id);
  const badge = checkIn(id, 'done');
  // Completion feedback for meditation, or whenever a badge is earned
  if (item && (item.kind === 'meditation' || badge)) {
    ui.back = location.hash || '#home';
    ui.flash = { id, title: item.title, mins: item.ref.mins, kind: item.kind, badge };
    clearTimeout(ui.flashTimer);
    ui.flashTimer = setTimeout(() => { if (location.hash === '#done') closeDone(); }, 4000);
    go('#done');
  } else render();
}
function closeDone() { clearTimeout(ui.flashTimer); if (location.hash !== '#done') return; const b = ui.back && ui.back !== '#done' ? ui.back : '#home'; ui.flash = null; go(b); }
function startDraft(d) { ui.back = location.hash || '#habits'; ui.draft = d; go('#new/1'); }

const A = {
  ring(el) { const id = el.dataset.id; if (status(id)?.s === 'done') { checkIn(id, null); render(); } else markDone(id); },
  st(el) { if (el.dataset.v === 'done') return markDone(el.dataset.id); checkIn(el.dataset.id, el.dataset.v); render(); },
  undo(el) { checkIn(el.dataset.id, null); render(); },
  tab(el) { go(el.dataset.v === 'mine' ? '#habits/mine' : '#habits'); },
  newHabit() { startDraft(blankDraft()); },
  capture() { ui.sheet = { type: 'capture', text: '' }; render(); setTimeout(() => $('#f-idea')?.focus(), 50); },
  saveIdea() { const t = (ui.sheet.text || '').trim(); if (!t) return $('#f-idea')?.focus(); S.ideas.push(t); save(); ui.sheet = null; render(); },
  ideaToHabit(el) { const i = +el.dataset.i; const d = blankDraft(S.ideas[i]); d.fromIdea = S.ideas[i]; startDraft(d); },
  menu(el) { ui.sheet = { type: 'menu', id: el.dataset.id }; render(); },
  badges() { ui.sheet = { type: 'badges' }; render(); },
  closeSheet() { if (ui.sheet?.type === 'checkin') return A.ciLater(); ui.sheet = null; render(); },
  pause(el) { S.habits.find((h) => h.id === el.dataset.id).status = 'paused'; save(); ui.sheet = null; render(); },
  resume(el) { S.habits.find((h) => h.id === el.dataset.id).status = 'active'; save(); ui.sheet = null; render(); },
  archive(el) { const h = S.habits.find((x) => x.id === el.dataset.id); if (!confirm(`Archive “${h.action}”? Its history is kept.`)) return; h.status = 'archived'; save(); ui.sheet = null; render(); },
  edit(el) { const h = S.habits.find((x) => x.id === el.dataset.id); ui.sheet = null; startDraft({ ...blankDraft(), ...JSON.parse(JSON.stringify(h)), every: h.days.length === 7 }); },
  changeTime(el) { const h = S.habits.find((x) => x.id === el.dataset.id); h.time = el.dataset.v; h.rtime = el.dataset.v; save(); render(); },
  sug(el) { ui.draft.action = el.dataset.v; render(); },
  step2() { if (!ui.draft.action.trim()) ui.draft.action = ui.draft.name.trim(); go('#new/2'); },
  every(el) { const on = el.dataset.v === '1'; ui.draft.every = on; if (on) ui.draft.days = [0, 1, 2, 3, 4, 5, 6]; else if (ui.draft.days.length === 7) ui.draft.days = [0, 1, 2, 3, 4]; render(); },
  day(el) { const v = +el.dataset.v, d = ui.draft; d.days = d.days.includes(v) ? d.days.filter((x) => x !== v) : [...d.days, v].sort(); d.every = d.days.length === 7; render(); },
  kind(el) { ui.draft.kind = el.dataset.v; render(); },
  anchor(el) { ui.draft.anchor = el.dataset.v; render(); },
  rem() { ui.draft.reminder = !ui.draft.reminder; render(); },
  saveHabit() {
    const d = ui.draft;
    const h = { id: d.id || uid(), name: d.name.trim(), action: d.action.trim() || d.name.trim(), days: d.days, kind: d.kind, anchor: d.anchor, time: d.time, reminder: d.reminder, rtime: d.kind === 'time' ? d.time : d.rtime, status: d.status || 'active', created: d.created || dkey(today()) };
    const i = S.habits.findIndex((x) => x.id === h.id);
    if (i >= 0) S.habits[i] = h; else S.habits.push(h);
    if (d.fromIdea) S.ideas = S.ideas.filter((x) => x !== d.fromIdea);
    save(); ui.draft = null; go('#habits/mine');
  },
  medType(el) { ui.medType = el.dataset.v; render(); },
  intent(el) { ui.intent = ui.intent === el.dataset.v ? null : el.dataset.v; render(); },
  len(el) { ui.len = ui.len === el.dataset.v ? null : el.dataset.v; render(); },
  clear() { ui.intent = ui.len = null; ui.q = ''; render(); },
  start(el) {
    const s = session(el.dataset.id);
    S.pending = { sessionId: s.id, at: Date.now() }; save();
    window.open(s.url, '_blank', 'noopener');
  },
  schedule(el) { ui.sheet = { type: 'schedule', sessionId: el.dataset.id, time: '07:30' }; render(); },
  saveSchedule() { S.meds.push({ id: ui.sheet.sessionId + '-' + uid(), sessionId: ui.sheet.sessionId, time: ui.sheet.time, created: dkey(today()) }); save(); ui.sheet = null; render(); },
  unschedule(el) { S.meds = S.meds.filter((m) => m.sessionId !== el.dataset.id); save(); render(); },
  ciDone() {
    const sid = ui.sheet.sessionId; ui.sheet = null; S.pending = null;
    let m = S.meds.find((x) => x.sessionId === sid);
    if (!m) { // an unscheduled session still gets logged: add it to today only via a one-off schedule
      m = { id: sid + '-' + uid(), sessionId: sid, time: nowHM(), created: dkey(today()), once: true };
      S.meds.push(m);
    }
    save(); markDone('m:' + m.id);
  },
  ciNot() { ui.sheet = null; S.pending = null; save(); render(); },
  ciLater() { ui.sheet = null; S.pending = null; save(); render(); },
  closeDone() { closeDone(); },
  reset() { if (confirm('Reset all demo data?')) { localStorage.removeItem(KEY); S = seed(); ui.sheet = null; ui.draft = null; go('#home'); } },
};

document.addEventListener('click', (e) => {
  const goEl = e.target.closest('[data-go]');
  if (goEl) { clearTimeout(ui.flashTimer); ui.flash = null; go(goEl.dataset.go); return; }
  const el = e.target.closest('[data-a]');
  if (!el || !A[el.dataset.a]) return;
  e.preventDefault();
  A[el.dataset.a](el);
});
document.addEventListener('input', (e) => {
  const f = e.target.dataset.f;
  if (!f) return;
  const v = e.target.value;
  if (f === 'name') { ui.draft.name = v; render(); }
  else if (f === 'action') ui.draft.action = v;
  else if (f === 'time') { ui.draft.time = v || ui.draft.time; render(); }
  else if (f === 'rtime') ui.draft.rtime = v || ui.draft.rtime;
  else if (f === 'q') { ui.q = v; render(); }
  else if (f === 'idea') ui.sheet.text = v;
  else if (f === 'stime') ui.sheet.time = v || ui.sheet.time;
  else if (f === 'refl') { const T = today(); S.reflections[dkey(addDays(T, -dow(T)))] = v; save(); }
});
document.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && e.target.dataset.f === 'idea') A.saveIdea();
  if (e.key === 'Escape' && ui.sheet) A.closeSheet();
});

// Check-in on return: when the user comes back after leaving for a session
function checkReturn() {
  if (document.visibilityState !== 'visible' || !S.pending || ui.sheet) return;
  if (Date.now() - S.pending.at < 1500) return;
  ui.sheet = { type: 'checkin', sessionId: S.pending.sessionId };
  render();
}
document.addEventListener('visibilitychange', checkReturn);
window.addEventListener('focus', checkReturn);
window.addEventListener('hashchange', render);
setInterval(() => { if (!ui.sheet && !document.activeElement?.id?.startsWith('f-')) render(); }, 60000);
render();
checkReturn();
