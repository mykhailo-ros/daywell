import os, urllib.parse, json

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dw", "project")
COMP = os.path.join(ROOT, "components")

# ---------- icons ----------
ICONS = {
 "check": "<path d='M5 12.5l4.5 4.5L19 7.5'/>",
 "chevron-left": "<path d='M15 5l-7 7 7 7'/>",
 "chevron-right": "<path d='M9 5l7 7-7 7'/>",
 "search": "<circle cx='11' cy='11' r='6.5'/><path d='M20 20l-4.2-4.2'/>",
 "clock": "<circle cx='12' cy='12' r='8.5'/><path d='M12 7.5V12l3 2'/>",
 "bell": "<path d='M6 16v-5a6 6 0 0 1 12 0v5l1.5 2h-15z'/><path d='M10 20.5a2 2 0 0 0 4 0'/>",
 "external": "<path d='M14 4h6v6'/><path d='M20 4l-9 9'/><path d='M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5'/>",
 "calendar": "<rect x='3.5' y='5' width='17' height='15.5' rx='2'/><path d='M3.5 10h17M8 3v4M16 3v4'/>",
 "plus": "<path d='M12 5v14M5 12h14'/>",
 "more": "<circle cx='5.5' cy='12' r='1'/><circle cx='12' cy='12' r='1'/><circle cx='18.5' cy='12' r='1'/>",
 "pause": "<path d='M9 6v12M15 6v12'/>",
 "edit": "<path d='M4 20h4L19 9l-4-4L4 16z'/><path d='M13 7l4 4'/>",
 "archive": "<rect x='3.5' y='4.5' width='17' height='4' rx='1'/><path d='M5 8.5v10a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-10M10 12.5h4'/>",
 "skip": "<path d='M6 6l8 6-8 6z'/><path d='M18 6v12'/>",
 "reschedule": "<rect x='3.5' y='5' width='17' height='15.5' rx='2'/><path d='M3.5 10h17M8 3v4M16 3v4M9 15.5h6M13 13.5l2 2-2 2'/>",
 "breath": "<path d='M3 8.5h10a2.8 2.8 0 1 0-2.8-2.8'/><path d='M3 12.5h14a3 3 0 1 1-3 3'/><path d='M3 16.5h6'/>",
 "habit": "<path d='M17 3l3 3-3 3'/><path d='M4 11V10a4 4 0 0 1 4-4h12'/><path d='M7 21l-3-3 3-3'/><path d='M20 13v1a4 4 0 0 1-4 4H4'/>",
 "exercise": "<path d='M3 12h4l3-7 4 14 3-7h4'/>",
 "flame": "<path d='M12 3.5c.8 2.8 5 5 5 9.8a5 5 0 0 1-10 0c0-2.4 1.3-3.9 2.3-4.8.2 1.8 1.2 2.8 2.2 2.8 0-2.6-.9-4.6.5-7.8z'/>",
 "award": "<circle cx='12' cy='9' r='5.5'/><path d='M8.8 13.5L7.5 20.5l4.5-2.3 4.5 2.3-1.3-7'/>",
 "sunrise": "<path d='M3 18.5h18M6.5 18.5a5.5 5.5 0 0 1 11 0M12 4v5M9.5 6.5L12 4l2.5 2.5M4.2 12.7l1.3.8M19.8 12.7l-1.3.8'/>",
 "sun": "<circle cx='12' cy='12' r='4'/><path d='M12 2.5v2M12 19.5v2M2.5 12h2M19.5 12h2M5.3 5.3l1.4 1.4M17.3 17.3l1.4 1.4M5.3 18.7l1.4-1.4M17.3 6.7l1.4-1.4'/>",
 "moon": "<path d='M19.5 14.5A7.8 7.8 0 1 1 9.5 4.5a6.3 6.3 0 0 0 10 10z'/>",
 "close": "<path d='M6 6l12 12M18 6L6 18'/>",
 "idea": "<path d='M9.5 18h5M10.5 21h3'/><path d='M12 3a6 6 0 0 0-3.6 10.8c.7.6 1.1 1.3 1.1 2.2h5c0-.9.4-1.6 1.1-2.2A6 6 0 0 0 12 3z'/>",
 "sliders": "<path d='M4 7h9M17 7h3M4 17h3M11 17h9'/><circle cx='15' cy='7' r='2'/><circle cx='9' cy='17' r='2'/>",
 "chart": "<path d='M4 20h16M7 16v-5M12 16V6M17 16v-8'/>",
 "lock": "<rect x='5' y='10.5' width='14' height='10' rx='2'/><path d='M8 10.5V8a4 4 0 0 1 8 0v2.5'/>",
}

def icon_css():
    out = []
    for n, body in ICONS.items():
        svg = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' "
               "stroke-width='1.75' stroke-linecap='round' stroke-linejoin='round'>" + body + "</svg>")
        out.append(".ic-%s{--ic:url(\"data:image/svg+xml,%s\")}" % (n, urllib.parse.quote(svg, safe=" ='/:.-,")))
    return "\n".join(out)

def ic(n, size=20, cls=""):
    return '<i class="ic ic-%s %s" style="width:%dpx;height:%dpx" aria-hidden="true"></i>' % (n, cls, size, size)

BUNDLE_CSS = r"""/* Daywell — shared screen styles. Colours, type, spacing, radii come from tokens.css. */
@import url("https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600&display=swap");

*{box-sizing:border-box;margin:0;padding:0}
html,body{background:var(--canvas);color:var(--ink);font-family:var(--font-sans);-webkit-font-smoothing:antialiased}
button{font:inherit;color:inherit;background:none;border:0;cursor:pointer}

.ic{display:inline-block;flex:none;background:currentColor;-webkit-mask:var(--ic) center/100% 100% no-repeat;mask:var(--ic) center/100% 100% no-repeat}

/* presentation stage */
.dw-stage{display:flex;gap:var(--space-8);padding:var(--space-8);align-items:flex-start;background:var(--canvas)}
.dw-notes{width:300px;flex:none;padding-top:var(--space-6);color:var(--ink-2)}
.dw-notes h3{color:var(--ink);margin-bottom:var(--space-2)}
.dw-notes p,.dw-notes li{margin-bottom:var(--space-2)}
.dw-notes ul{padding-left:18px}
.dw-notes .dw-num{display:inline-flex;align-items:center;justify-content:center;width:24px;height:24px;border-radius:var(--radius-pill);background:var(--ink);color:var(--bg);margin-bottom:var(--space-3)}
.dw-notes hr{border:0;border-top:1px solid var(--line-2);margin:var(--space-4) 0}
.dw-cap{display:block;color:var(--ink-3);margin:0 0 var(--space-2) var(--space-2)}

/* device */
.dw-phone{position:relative;width:390px;height:844px;flex:none;background:var(--bg);border-radius:44px;box-shadow:var(--shadow-device);overflow:hidden;display:flex;flex-direction:column}
.dw-phone.is-long{height:auto;min-height:844px}
.dw-fold{position:absolute;left:0;right:0;top:844px;border-top:1px dashed var(--border-control);z-index:5}
.dw-fold span{position:absolute;right:12px;top:-20px;color:var(--ink-3);background:var(--bg);padding:0 6px}
.dw-status{height:50px;flex:none;display:flex;align-items:center;justify-content:space-between;padding:6px 30px 0 34px}
.dw-status b{font-weight:600;font-size:16px}
.dw-batt{display:flex;gap:6px;align-items:center}
.dw-batt i{display:block;width:25px;height:12px;border:1.5px solid var(--ink);border-radius:4px;position:relative}
.dw-batt i:after{content:"";position:absolute;inset:1.5px;right:5px;background:var(--ink);border-radius:1.5px}
.dw-batt s{display:flex;gap:2px;align-items:flex-end;height:12px}
.dw-batt s u{display:block;width:3px;background:var(--ink);border-radius:1px}
.dw-homebar{position:absolute;bottom:8px;left:50%;width:134px;height:5px;margin-left:-67px;border-radius:var(--radius-pill);background:var(--ink);z-index:9}
.dw-body{flex:1;padding:0 var(--space-5) 40px;position:relative}

/* top bar */
.dw-nav{display:flex;align-items:center;justify-content:space-between;height:52px;margin:0 calc(-1 * var(--space-3))}
.dw-nav .dw-iconbtn{width:44px;height:44px;display:flex;align-items:center;justify-content:center;border-radius:var(--radius-pill);color:var(--ink)}
.dw-nav .dw-navtitle{flex:1;text-align:center}
.dw-steps{display:flex;gap:6px;flex:1;justify-content:center}
.dw-steps i{width:28px;height:4px;border-radius:var(--radius-pill);background:var(--line)}
.dw-steps i.on{background:var(--ink)}

/* text helpers */
.c-ink2{color:var(--ink-2)}.c-ink3{color:var(--ink-3)}.c-accent{color:var(--accent)}
.up{text-transform:uppercase}
.mt1{margin-top:var(--space-1)}.mt2{margin-top:var(--space-2)}.mt3{margin-top:var(--space-3)}.mt4{margin-top:var(--space-4)}.mt5{margin-top:var(--space-5)}.mt6{margin-top:var(--space-6)}.mt8{margin-top:var(--space-8)}
.row{display:flex;align-items:center;gap:var(--space-2)}
.between{display:flex;align-items:center;justify-content:space-between;gap:var(--space-3)}
.grow{flex:1;min-width:0}

/* section head */
.dw-sechead{display:flex;align-items:baseline;justify-content:space-between;margin:var(--space-6) 0 var(--space-1)}
.dw-group{display:flex;align-items:center;gap:var(--space-2);color:var(--ink-3);margin:var(--space-6) 0 var(--space-1)}

/* list rows */
.dw-list{list-style:none}
.dw-item{display:flex;align-items:center;gap:var(--space-3);min-height:60px;padding:10px 0;border-bottom:1px solid var(--line)}
.dw-item:last-child{border-bottom:0}
.dw-item .dw-lead{color:var(--ink-2)}
.dw-item.is-done .t-body-strong{color:var(--ink-3)}
.dw-meta{color:var(--ink-2);margin-top:2px;display:flex;align-items:center;gap:6px;flex-wrap:wrap}
.dw-meta .sep{color:var(--line-2)}

/* check-in ring */
.dw-check{width:44px;height:44px;display:flex;align-items:center;justify-content:center;flex:none;margin-right:-6px}
.dw-check span{width:32px;height:32px;border-radius:var(--radius-pill);border:1.5px solid var(--border-control);display:flex;align-items:center;justify-content:center;color:transparent}
.dw-check.is-done span{background:var(--accent);border-color:var(--accent);color:var(--on-accent)}

/* streak flag */
.dw-streak{display:inline-flex;align-items:center;gap:3px;color:var(--accent)}
.dw-kept{display:inline-flex;align-items:center;gap:4px;color:var(--accent)}

/* buttons */
.dw-btn{display:flex;align-items:center;justify-content:center;gap:var(--space-2);width:100%;height:52px;border-radius:var(--radius-md);font-size:16px;font-weight:600}
.dw-btn.primary{background:var(--accent);color:var(--on-accent)}
.dw-btn.secondary{border:1px solid var(--border-control);color:var(--ink)}
.dw-btn.tertiary{color:var(--ink-2);height:44px}
.dw-sbtn{display:inline-flex;align-items:center;gap:6px;height:36px;padding:0 12px;border-radius:var(--radius-pill);color:var(--ink-2);font-size:14px;font-weight:500}
.dw-sbtn.outline{border:1px solid var(--line-2);color:var(--ink)}
.dw-sbtn.done{border:1px solid var(--accent);color:var(--accent)}
.dw-sbtn.fill{background:var(--accent);color:var(--on-accent)}

/* chips */
.dw-chips{display:flex;gap:var(--space-2);flex-wrap:wrap}
.dw-chips.scroll{flex-wrap:nowrap;overflow:hidden;margin-right:calc(-1 * var(--space-5))}
.dw-chip{display:inline-flex;align-items:center;gap:6px;height:36px;padding:0 14px;border-radius:var(--radius-pill);border:1px solid var(--line-2);color:var(--ink);white-space:nowrap}
.dw-chip.on{background:var(--ink);border-color:var(--ink);color:var(--bg)}

/* segmented */
.dw-seg{display:flex;background:var(--surface);border-radius:12px;padding:3px}
.dw-seg span{flex:1;height:36px;display:flex;align-items:center;justify-content:center;border-radius:10px;color:var(--ink-2)}
.dw-seg span.on{background:var(--bg);color:var(--ink);box-shadow:var(--shadow-thumb)}

/* inputs */
.dw-field{display:flex;align-items:center;gap:var(--space-2);height:52px;padding:0 var(--space-4);border-radius:var(--radius-md);border:1px solid var(--border-control);background:var(--bg)}
.dw-field.focus{border:2px solid var(--focus);padding:0 15px}
.dw-field.search{background:var(--surface);border-color:transparent;color:var(--ink-3)}
.dw-caret{display:inline-block;width:2px;height:22px;background:var(--accent);margin-left:1px;vertical-align:middle}
.dw-label{display:block;color:var(--ink-2);margin-bottom:var(--space-2)}

/* toggle */
.dw-toggle{width:51px;height:31px;border-radius:var(--radius-pill);background:var(--line-2);position:relative;flex:none}
.dw-toggle:after{content:"";position:absolute;top:2px;left:2px;width:27px;height:27px;border-radius:var(--radius-pill);background:var(--bg);box-shadow:var(--shadow-thumb)}
.dw-toggle.on{background:var(--accent)}
.dw-toggle.on:after{left:22px}

/* cards & panels */
.dw-card{border:1px solid var(--line-2);border-radius:var(--radius-md);padding:var(--space-4)}
.dw-panel{background:var(--surface);border-radius:var(--radius-md);padding:var(--space-4)}
.dw-tint{background:var(--accent-tint);border-radius:var(--radius-md);padding:var(--space-4)}
.dw-tag{display:inline-flex;align-items:center;height:24px;padding:0 8px;border-radius:var(--radius-sm);background:var(--surface);color:var(--ink-2)}

/* progress strip */
.dw-strip{display:grid;grid-template-columns:1fr 1fr 1.15fr;background:var(--surface);border-radius:var(--radius-md)}
.dw-strip > div{padding:14px 12px 14px 16px;border-left:1px solid var(--line)}
.dw-strip > div:first-child{border-left:0}
.dw-strip .t-caption{color:var(--ink-2)}
.dw-bar{height:4px;border-radius:var(--radius-pill);background:var(--line);margin-top:8px;overflow:hidden}
.dw-bar i{display:block;height:100%;background:var(--accent);border-radius:var(--radius-pill)}

/* entry points */
.dw-entries{display:grid;grid-template-columns:repeat(3,1fr);gap:var(--space-2)}
.dw-entry{border:1px solid var(--line-2);border-radius:var(--radius-md);padding:14px 12px;display:flex;flex-direction:column;gap:10px}

/* week dots */
.dw-dots{display:flex;gap:6px;align-items:center}
.dw-dots i{width:12px;height:12px;border-radius:var(--radius-pill);display:block;position:relative}
.dw-dots i.d{background:var(--accent)}
.dw-dots i.k{border:1.5px solid var(--accent)}
.dw-dots i.k:after{content:"";position:absolute;left:2px;right:2px;top:4px;height:1.5px;background:var(--accent)}
.dw-dots i.m{border:1.5px solid var(--border-control)}
.dw-dots i.n{background:var(--line)}
.dw-dots i.t{border:1.5px dashed var(--border-control)}

/* sheet */
.dw-scrim{position:absolute;inset:0;background:var(--scrim);z-index:6}
.dw-sheet{position:absolute;left:0;right:0;bottom:0;background:var(--bg);border-radius:var(--radius-lg) var(--radius-lg) 0 0;box-shadow:var(--shadow-sheet);padding:12px var(--space-5) 40px;z-index:7}
.dw-grab{width:36px;height:5px;border-radius:var(--radius-pill);background:var(--line-2);margin:0 auto var(--space-5)}
.dw-dim{opacity:1}

/* menu */
.dw-menu{position:absolute;background:var(--bg);border-radius:var(--radius-md);box-shadow:var(--shadow-sheet),0 0 0 1px var(--line);width:200px;z-index:8;padding:6px 0}
.dw-menu div{display:flex;align-items:center;gap:12px;height:44px;padding:0 16px}

/* keyboard */
.dw-kb{position:absolute;left:0;right:0;bottom:0;height:291px;background:var(--surface);padding:8px 3px 0;z-index:8}
.dw-kb .r{display:flex;justify-content:center;gap:6px;margin-bottom:11px}
.dw-kb .k{width:33px;height:42px;border-radius:5px;background:var(--bg);box-shadow:var(--shadow-thumb);display:flex;align-items:center;justify-content:center;font-size:22px;color:var(--ink)}
.dw-kb .k.w{width:44px;background:var(--line);font-size:14px}
.dw-kb .k.sp{width:186px;font-size:16px}
.dw-kb .k.rt{width:88px;background:var(--line);font-size:16px}

/* lock screen */
.dw-lock{background:var(--ink);color:var(--bg)}
.dw-lock .dw-batt i{border-color:var(--bg)}
.dw-lock .dw-batt i:after,.dw-lock .dw-batt s u,.dw-lock .dw-homebar{background:var(--bg)}
.dw-notif{background:var(--bg);color:var(--ink);border-radius:var(--radius-lg);padding:14px 16px}
.dw-appmark{width:22px;height:22px;border-radius:6px;background:var(--accent);display:flex;align-items:center;justify-content:center;color:var(--on-accent)}

/* days */
.dw-days{display:flex;gap:6px}
.dw-days span{flex:1;height:44px;border-radius:var(--radius-sm);border:1px solid var(--line-2);display:flex;align-items:center;justify-content:center;color:var(--ink-2)}
.dw-days span.on{background:var(--ink);border-color:var(--ink);color:var(--bg)}

/* option rows (radio list) */
.dw-opt{display:flex;align-items:center;gap:12px;height:52px;border-bottom:1px solid var(--line)}
.dw-opt:last-child{border-bottom:0}
.dw-radio{width:22px;height:22px;border-radius:var(--radius-pill);border:1.5px solid var(--border-control);flex:none;position:relative}
.dw-radio.on{border-color:var(--ink)}
.dw-radio.on:after{content:"";position:absolute;inset:4px;border-radius:var(--radius-pill);background:var(--ink)}

/* big confirmation mark */
.dw-bigcheck{width:72px;height:72px;border-radius:var(--radius-pill);background:var(--accent);color:var(--on-accent);display:flex;align-items:center;justify-content:center}
.dw-badge{width:56px;height:56px;border-radius:var(--radius-pill);border:1.5px solid var(--accent);color:var(--accent);display:flex;align-items:center;justify-content:center;flex:none;background:var(--bg)}
.dw-textarea{border:1px solid var(--border-control);border-radius:var(--radius-md);min-height:96px;padding:14px 16px;color:var(--ink-3)}
"""

# ---------- page helpers ----------
def status(time="9:12"):
    return ('<div class="dw-status"><b>%s</b><div class="dw-batt"><s><u style="height:4px"></u><u style="height:6px"></u>'
            '<u style="height:8px"></u><u style="height:11px"></u></s><i></i></div></div>') % time

def phone(inner, cls="", time="9:12", overlay="", long=False):
    return ('<div class="dw-phone %s%s">%s<div class="dw-body">%s</div>%s<div class="dw-homebar"></div>%s</div>'
            % (cls, " is-long" if long else "", status(time), inner, overlay,
               '<div class="dw-fold"><span class="t-caption">844 — fold</span></div>' if long else ""))

def labeled(caption, ph):
    return '<div><span class="dw-cap t-caption">%s</span>%s</div>' % (caption, ph)

def notes(num, title, body):
    return ('<aside class="dw-notes"><span class="dw-num t-label">%s</span><h3 class="t-heading">%s</h3>%s</aside>'
            % (num, title, body))

def page(group, height, subtitle, title, stage, width=None):
    w = (" width=%d" % width) if width else ""
    return ('<!-- @dsCard group="%s" height=%d%s subtitle="%s" -->\n<!doctype html>\n<html>\n<head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1"><title>%s</title></head>\n<body>\n'
            '<div class="dw-stage">%s</div>\n</body>\n</html>\n') % (group, height, w, subtitle, title, stage)

def nav(title="", left="chevron-left", right=None, right_label=None):
    l = '<button class="dw-iconbtn" aria-label="Back">%s</button>' % ic(left, 24) if left else '<span style="width:44px"></span>'
    if right_label:
        r = '<button class="t-label c-ink2" style="height:44px;padding:0 12px">%s</button>' % right_label
    elif right:
        r = '<button class="dw-iconbtn" aria-label="%s">%s</button>' % (right, ic(right, 24))
    else:
        r = '<span style="width:44px"></span>'
    return '<div class="dw-nav">%s<div class="dw-navtitle t-heading">%s</div>%s</div>' % (l, title, r)

def check(done=False):
    return ('<button class="dw-check%s" aria-label="%s"><span>%s</span></button>'
            % (" is-done" if done else "", "Done" if done else "Mark as done", ic("check", 18)))

def meta(*parts):
    return '<div class="dw-meta t-caption">%s</div>' % '<span class="sep">·</span>'.join(parts)

def item(icon, title, meta_html, done=False, extra=""):
    return ('<li class="dw-item%s"><span class="dw-lead">%s</span><div class="grow"><div class="t-body-strong">%s</div>%s</div>%s%s</li>'
            % (" is-done" if done else "", ic(icon, 20), title, meta_html, extra, check(done)))

def dots(spec):
    return '<span class="dw-dots">%s</span>' % "".join('<i class="%s"></i>' % c for c in spec)

files = {}

# ============ 01 HOME ============
home = (
 '<div class="mt3 t-overline up c-ink3">Friday 30 October</div>'
 '<h1 class="t-display mt1">Good morning, Alex</h1>'
 '<p class="t-body c-ink2 mt1">2 of 6 done. A good start.</p>'
 '<div class="dw-sechead"><h2 class="t-heading">Today</h2><span class="t-caption c-ink3">6 items</span></div>'
 '<ul class="dw-list">'
 + item("habit", "Stretch for 5 minutes", meta("Habit", "Morning", "Done 7:05 a.m."), True)
 + item("breath", "Morning focus breath", meta("Meditation", "8 min", "Done 7:41 a.m."), True)
 + item("habit", "Short walk", meta("Habit", "After lunch"))
 + item("exercise", "Full-body strength", meta("Exercise", "25 min", "6:00 p.m."))
 + item("habit", "Study for 30 minutes", meta("Habit", "7:00 p.m.", '<span class="dw-streak">%s5</span>' % ic("flame", 14)))
 + item("habit", "Read for 10 minutes", meta("Habit", "Before bed"))
 + '</ul>'
 '<div class="dw-strip mt4">'
   '<div><div class="t-caption">Streak</div><div class="t-numeral mt1">5 days</div><div class="t-caption c-ink3">Daily study</div></div>'
   '<div><div class="t-caption">Today</div><div class="t-numeral mt1">2 of 6</div><div class="dw-bar"><i style="width:33%"></i></div></div>'
   '<div><div class="t-caption">Latest badge</div><div class="row mt2"><span class="c-accent">' + ic("award", 22) + '</span><span class="t-label">Three in a row</span></div></div>'
 '</div>'
 '<div class="dw-entries mt3">'
   '<div class="dw-entry">' + ic("breath", 22) + '<span class="t-label">Meditation</span></div>'
   '<div class="dw-entry">' + ic("habit", 22) + '<span class="t-label">Habits</span></div>'
   '<div class="dw-entry">' + ic("exercise", 22) + '<span class="t-label">Exercise</span></div>'
 '</div>'
)
files["Home"] = page("Home", 920, "01 · Today across the app", "Home",
  phone(home) + notes("01", "Home",
   '<p class="t-body">One list for everything scheduled today, in time order: habits, the scheduled meditation and the workout.</p>'
   '<ul class="t-caption"><li>The ring on each row is the one-tap check-in. Checking in here also marks the item in Habits, Meditation or Exercise, and the reverse is true too.</li>'
   '<li>Done items stay in place and turn <b>ink-3</b>, so the list doesn\'t jump around.</li>'
   '<li>The progress strip shows the longest current streak, today\'s completion and the latest badge. Tapping any tile opens the related section.</li>'
   '<li>The subline only counts what\'s done. It never counts what\'s left.</li>'
   '<li>Home has no tab bar. The three tiles open each section.</li></ul>'))

# ============ 02 BROWSE ============
def result(title, length, source, intent, typ):
    return ('<li class="dw-card mt2"><div class="t-body-strong">%s</div>'
            '<div class="dw-meta t-caption mt1"><span class="row" style="gap:4px">%s%s</span><span class="sep">·</span>%s<span class="sep">·</span>%s</div>'
            '<div class="row mt3"><span class="dw-tag t-caption">%s</span><span class="dw-tag t-caption">%s</span></div></li>'
            % (title, ic("clock", 14), length, typ, source, intent, "Breathwork"))
browse = (
 nav("Meditation", right="calendar")
 + '<div class="dw-chips mt2"><span class="dw-chip t-label">Meditation</span><span class="dw-chip on t-label">Breathwork</span><span class="dw-chip t-label">Affirmations</span></div>'
 '<div class="dw-field search mt4">' + ic("search", 20) + '<span class="t-body">Search breathwork</span></div>'
 '<div class="t-overline up c-ink3 mt5">Intention</div>'
 '<div class="dw-chips mt2"><span class="dw-chip t-label">Peace</span><span class="dw-chip on t-label">Focus</span><span class="dw-chip t-label">Sleep</span><span class="dw-chip t-label">Energy</span></div>'
 '<div class="t-overline up c-ink3 mt4">Length</div>'
 '<div class="dw-chips mt2"><span class="dw-chip t-label">Under 5</span><span class="dw-chip on t-label">5–10</span><span class="dw-chip t-label">10–20</span><span class="dw-chip t-label">20+ min</span></div>'
 '<div class="between mt5"><span class="t-caption c-ink2">3 sessions</span><span class="t-label c-ink2">Clear filters</span></div>'
 '<ul class="dw-list">'
 + result("Morning focus breath", "8 min", "YouTube", "Focus", "")
 + result("Box breathing for clear thinking", "6 min", "YouTube", "Focus", "")
 + result("Steady breath before work", "10 min", "Spotify", "Focus", "")
 + '</ul>'
)
browse = browse.replace('<span class="sep">·</span><span class="sep">·</span>', '<span class="sep">·</span>')
files["MeditationBrowse"] = page("Meditation", 920, "02 · Find a session", "Meditation browse",
  phone(browse) + notes("02", "Browse",
   '<p class="t-body">Daywell finds sessions and tracks them. Sessions play on their source.</p>'
   '<ul class="t-caption"><li>The type chips (Meditation, Breathwork, Affirmations) work like tabs, so one is always selected.</li>'
   '<li>Intention and length are single-select filters. Tap a selected chip again to clear it. Selected chips use <b>ink</b> because the accent only means progress.</li>'
   '<li>Each card shows title, length, source and intention. There are no thumbnails.</li>'
   '<li>The calendar icon opens scheduled sessions.</li></ul>'))

# ============ 03 DETAIL ============
detail = (
 nav("", right="more")
 + '<div class="t-overline up c-ink3 mt3">Breathwork</div>'
 '<h1 class="t-title mt1">Morning focus breath</h1>'
 '<div class="dw-meta t-body mt2" style="color:var(--ink-2)"><span class="row" style="gap:4px">' + ic("clock", 16) + '8 min</span><span class="sep">·</span>YouTube<span class="sep">·</span>Focus</div>'
 '<p class="t-body c-ink2 mt5">A short guided breathing practice to settle your attention before the day starts. Slow inhales and longer exhales, finishing with a minute of quiet.</p>'
 '<div class="dw-panel mt6"><div class="between"><div class="row"><span class="c-ink2">' + ic("calendar", 20) + '</span><span class="t-label">Scheduled</span></div><span class="t-label c-ink2">Every day · 7:30 a.m.</span></div></div>'
 '<div class="dw-panel mt2"><div class="between"><div class="row"><span class="c-accent">' + ic("flame", 20) + '</span><span class="t-label">Your streak</span></div><span class="t-label c-accent">2 days</span></div></div>'
 '<div style="position:absolute;left:20px;right:20px;bottom:40px">'
 '<button class="dw-btn primary">Start on YouTube ' + ic("external", 18) + '</button>'
 '<p class="t-caption c-ink2 mt2" style="text-align:center">This opens YouTube. Come back to log it.</p>'
 '<button class="dw-btn secondary mt4">' + ic("calendar", 20) + 'Schedule for later</button>'
 '</div>'
)
files["SessionDetail"] = page("Meditation", 920, "03 · Start or schedule", "Session detail",
  phone(detail, time="7:30") + notes("03", "Session detail",
   '<p class="t-body">Title, length, source and a short description, with two actions.</p>'
   '<ul class="t-caption"><li><b>Start on YouTube</b> is the single primary. The external-link icon and the note under it say plainly that you\'re leaving the app.</li>'
   '<li>Daywell remembers the session when you leave. When you come back, it asks if you finished (04).</li>'
   '<li><b>Schedule for later</b> opens a date and time picker, and the session then appears in Today on Home.</li>'
   '<li>The streak shown here is the meditation streak before today\'s session.</li></ul>'))

# ============ 04 CHECK-IN SHEET ============
sheet = (
 '<div class="dw-scrim"></div><div class="dw-sheet"><div class="dw-grab"></div>'
 '<div class="t-overline up c-ink3">Welcome back</div>'
 '<h2 class="t-title mt2">Did you complete Morning focus breath?</h2>'
 '<p class="t-body c-ink2 mt2">8 min · YouTube</p>'
 '<button class="dw-btn primary mt6">' + ic("check", 20) + 'Done</button>'
 '<button class="dw-btn secondary mt3">Not this time</button>'
 '<button class="dw-btn tertiary mt2">' + ic("bell", 18) + 'Remind me later</button>'
 '<p class="t-caption c-ink3 mt3" style="text-align:center">Your word is enough. No timer, no proof.</p>'
 '</div>'
)
files["CheckInSheet"] = page("Meditation", 920, "04 · Bottom sheet on return", "Check-in on return",
  phone(detail, time="7:41", overlay=sheet) + notes("04", "Check-in on return",
   '<p class="t-body">This sheet appears the first time the app opens after the user left for a session.</p>'
   '<ul class="t-caption"><li><b>Done</b> logs the session and shows the completion screen (06). It is self-reported and never asks for proof.</li>'
   '<li><b>Not this time</b> closes the sheet without logging. It says nothing about the streak and shows no warning.</li>'
   '<li><b>Remind me later</b> closes the sheet. The session stays open in Today with its ring, so it can be checked in there.</li>'
   '<li>Swiping the sheet down is the same as Remind me later.</li></ul>'))

# ============ 05 NOTIFICATION ============
lock = (
 '<div style="text-align:center;margin-top:28px">' + ic("lock", 20) + '</div>'
 '<div class="t-label" style="text-align:center;margin-top:8px;opacity:.85">Friday 30 October</div>'
 '<div style="text-align:center;font-size:88px;line-height:96px;font-weight:500;letter-spacing:-2px">8:05</div>'
 '<div class="dw-notif" style="margin-top:300px">'
   '<div class="between"><div class="row"><span class="dw-appmark">' + ic("check", 14) + '</span><span class="t-caption c-ink2">DAYWELL</span></div><span class="t-caption c-ink3">now</span></div>'
   '<div class="t-body-strong mt2">Morning focus breath</div>'
   '<div class="t-body">Finished your session? Tap to check in.</div>'
 '</div>'
)
files["FollowUpNotification"] = page("Meditation", 920, "05 · Sent once if the user doesn't return", "Follow-up notification",
  phone(lock, cls="dw-lock", time="8:05") + notes("05", "Follow-up notification",
   '<p class="t-body">This is sent <b>once</b>, about 15 minutes after the session\'s length has passed, but only if the user hasn\'t come back to the app.</p>'
   '<ul class="t-caption"><li>Tapping it opens the app with the check-in sheet (04) already showing.</li>'
   '<li>It never sends a second nudge. If the user doesn\'t respond, the item stays open in Today with no penalty until midnight.</li>'
   '<li>The copy is a question rather than a reminder of what\'s left undone.</li></ul>'))

# ============ 06 COMPLETION ============
done = (
 nav("", left=None, right="close")
 + '<div style="display:flex;flex-direction:column;align-items:center;text-align:center;margin-top:56px">'
 '<div class="dw-bigcheck">' + ic("check", 36) + '</div>'
 '<h1 class="t-display mt6">Nicely done</h1>'
 '<p class="t-body c-ink2 mt2">Morning focus breath · 8 min logged</p>'
 '</div>'
 '<div class="dw-panel mt8"><div class="between"><div><div class="t-caption c-ink2">Meditation streak</div><div class="t-numeral mt1 c-accent">3 days</div></div>'
 '</div>'
 '<div class="row mt3" style="justify-content:space-between">'
 + "".join('<div style="display:flex;flex-direction:column;align-items:center;gap:6px"><span class="t-caption c-ink3">%s</span>%s</div>' % (d, dots(c)) for d, c in [("Mon","m"),("Tue","m"),("Wed","d"),("Thu","d"),("Fri","d")])
 + '</div></div>'
 '<div class="dw-tint mt3"><div class="row" style="gap:16px"><span class="dw-badge">' + ic("award", 28) + '</span><div><div class="t-caption c-accent">New badge</div><div class="t-body-strong">Three in a row</div><div class="t-caption c-ink2">Three mornings of meditation in a row.</div></div></div></div>'
 '<div style="position:absolute;left:20px;right:20px;bottom:40px"><button class="dw-btn primary">Back to Today</button></div>'
)
files["CompletionFeedback"] = page("Meditation", 920, "06 · After Done", "Completion feedback",
  phone(done, time="7:41") + notes("06", "Completion feedback",
   '<p class="t-body">A short, calm confirmation that shows the updated streak and, only if one was earned, a badge.</p>'
   '<ul class="t-caption"><li>Without a badge, the tinted badge card isn\'t shown and the layout stays the same.</li>'
   '<li>The week row uses the shared dot legend: Mon and Tue were missed (hollow, neutral) and Wed–Fri are Done.</li>'
   '<li>It closes after 4 s or on tap and returns to where the user started. The item is now checked on Home.</li>'
   '<li>The single "!" budget is left unspent. A plain "Nicely done" is enough.</li></ul>'))

# ============ 07 HABITS TODAY ============
def hrow(title, when, state=None, streak=None):
    s = (' <span class="sep">·</span><span class="dw-streak">%s%d</span>' % (ic("flame", 14), streak)) if streak else ""
    head = ('<div class="between"><div class="grow"><div class="t-body-strong">%s</div><div class="dw-meta t-caption">%s%s</div></div>%s</div>'
            % (title, when, s, check(state == "done")))
    if state == "done":
        acts = '<div class="row mt1"><span class="t-caption c-accent">Done 7:05 a.m.</span><span class="sep t-caption" style="color:var(--line-2)">·</span><span class="t-caption c-ink2" style="text-decoration:underline">Undo</span></div>'
    else:
        acts = ('<div class="row mt2" style="gap:4px;margin-left:-12px">'
                '<button class="dw-sbtn">' + ic("check", 16) + 'Done</button>'
                '<button class="dw-sbtn">' + ic("skip", 16) + 'Skip</button>'
                '<button class="dw-sbtn">' + ic("reschedule", 16) + 'Reschedule</button></div>')
    return '<li class="dw-item" style="display:block;padding:14px 0 10px">%s%s</li>' % (head, acts)

def habits_head(active="Today"):
    t = "".join('<span class="t-label%s">%s</span>' % (" on" if x == active else "", x) for x in ["Today", "My habits"])
    return nav("Habits", right="plus") + '<div class="dw-seg mt2">%s</div>' % t

htoday = (
 habits_head()
 + '<div class="between mt5"><span class="t-label c-ink2">Friday 30 October</span><span class="t-label c-accent">1 of 4 done</span></div>'
 '<div class="dw-group">' + ic("sunrise", 18) + '<span class="t-overline up">Morning</span></div>'
 '<ul class="dw-list">' + hrow("Stretch for 5 minutes", "Morning", "done") + '</ul>'
 '<div class="dw-group">' + ic("sun", 18) + '<span class="t-overline up">During the day</span></div>'
 '<ul class="dw-list">' + hrow("Short walk", "After lunch") + '</ul>'
 '<div class="dw-group">' + ic("moon", 18) + '<span class="t-overline up">Evening</span></div>'
 '<ul class="dw-list">' + hrow("Study for 30 minutes", "7:00 p.m.", streak=5) + hrow("Read for 10 minutes", "Before bed") + '</ul>'
)
alldone = (
 habits_head()
 + '<div class="between mt5"><span class="t-label c-ink2">Friday 30 October</span><span class="t-label c-accent">4 of 4 done</span></div>'
 '<div style="display:flex;flex-direction:column;align-items:center;text-align:center;padding:40px 12px 28px">'
 '<div class="dw-bigcheck">' + ic("check", 36) + '</div>'
 '<h2 class="t-title mt5">All done for today</h2>'
 '<p class="t-body c-ink2 mt2">That\'s every habit for Friday. Enjoy your evening.</p>'
 '<p class="t-label c-accent mt3 row" style="justify-content:center">' + ic("flame", 16) + 'Daily study · 6-day streak</p>'
 '</div>'
 '<ul class="dw-list">'
 + item("sunrise", "Stretch for 5 minutes", meta("Done 7:05 a.m."), True)
 + item("sun", "Short walk", meta("Done 1:20 p.m."), True)
 + item("moon", "Study for 30 minutes", meta("Done 7:34 p.m."), True)
 + item("moon", "Read for 10 minutes", meta("Done 10:12 p.m."), True)
 + '</ul>'
 '<p class="t-caption c-ink3 mt4" style="text-align:center">Tomorrow: 3 habits</p>'
)
files["HabitsToday"] = page("Habits", 920, "07 · Default tab, plus the all-done state", "Habits – Today",
  labeled("Default", phone(htoday)) + labeled("All done for today", phone(alldone, time="10:12"))
  + notes("07", "Habits – Today",
   '<p class="t-body">Only today\'s habits, grouped by time of day. Each open row has Done, Skip and Reschedule.</p>'
   '<ul class="t-caption"><li><b>Done</b> (the ring or the text button) counts toward the streak and syncs with Home.</li>'
   '<li><b>Skip</b> and <b>Reschedule</b> keep the streak. The row then says "Skipped · Streak kept" or "Rescheduled to 8:30 p.m. · Streak kept".</li>'
   '<li>A habit left unchecked at midnight counts as missed. There\'s no alert, just a hollow dot in the weekly review.</li>'
   '<li>When everything is checked, the counter fills and the calm all-done header appears above the finished list.</li>'
   '<li><b>+</b> opens Quick capture (09) or Create habit (10).</li></ul>', ), width=1300)

# ============ 08 MY HABITS ============
def mh(title, sched, nxt, streak=None, paused=False):
    s = ('<span class="sep">·</span><span class="dw-streak">%s%d</span>' % (ic("flame", 14), streak)) if streak else ""
    return ('<li class="dw-item"><div class="grow"><div class="t-body-strong">%s</div><div class="dw-meta t-caption">%s</div>'
            '<div class="dw-meta t-caption" style="color:var(--ink-3)">%s%s</div></div>'
            '<button class="dw-iconbtn" style="width:44px;height:44px;display:flex;align-items:center;justify-content:center;color:var(--ink-2);margin-right:-10px" aria-label="More">%s</button></li>'
            % (title, sched, nxt, s, ic("more", 22)))
myh = (
 habits_head("My habits")
 + '<div class="dw-panel mt4 between"><div class="row">' + ic("chart", 20) + '<div><div class="t-label">Weekly review</div><div class="t-caption c-ink2">Week so far · 26 Oct – 1 Nov</div></div></div>' + ic("chevron-right", 20, "c-ink3") + '</div>'
 '<div class="dw-group">' + ic("sunrise", 18) + '<span class="t-overline up">Morning</span></div>'
 '<ul class="dw-list">' + mh("Stretch for 5 minutes", "Every day · Morning", "Next: tomorrow") + '</ul>'
 '<div class="dw-group">' + ic("sun", 18) + '<span class="t-overline up">During the day</span></div>'
 '<ul class="dw-list">' + mh("Short walk", "Every day · After lunch", "Next: today") + '</ul>'
 '<div class="dw-group">' + ic("moon", 18) + '<span class="t-overline up">Evening</span></div>'
 '<ul class="dw-list">' + mh("Daily study", "Study for 30 minutes · Mon–Fri · 7:00 p.m.", "Next: today, 7:00 p.m.", 5)
 + mh("Read for 10 minutes", "Every day · Before bed", "Next: today") + '</ul>'
 '<div class="between"><div class="dw-group">' + ic("idea", 18) + '<span class="t-overline up">Ideas to turn into habits</span></div><span class="t-label c-ink2 row" style="margin-top:var(--space-6);gap:4px">' + ic("plus", 16) + 'Save an idea</span></div>'
 '<div class="dw-chips mt2"><span class="dw-chip t-label">Practise guitar</span><span class="dw-chip t-label">Cook a new recipe</span></div>'
)
menu = ('<div class="dw-menu" style="right:24px;top:494px">'
        '<div class="t-body">' + ic("pause", 20) + 'Pause</div>'
        '<div class="t-body">' + ic("edit", 20) + 'Edit</div>'
        '<div class="t-body" style="border-top:1px solid var(--line)">' + ic("archive", 20) + 'Archive</div></div>')
files["MyHabits"] = page("Habits", 920, "08 · Active habits by routine, plus ideas", "My habits",
  labeled("Default", phone(myh)) + labeled("More menu on Daily study", phone(myh, overlay=menu))
  + notes("08", "My habits",
   '<p class="t-body">All active habits grouped by routine, each with its schedule and next due date.</p>'
   '<ul class="t-caption"><li>The <b>···</b> menu has Pause, Edit and Archive. Paused habits move to a "Paused" group at the bottom and their streak is frozen, not lost.</li>'
   '<li>Archive removes a habit from the active list but keeps its history.</li>'
   '<li>"Ideas to turn into habits" holds saved intentions. Tapping one opens Create habit (10) with the name filled in. <b>Save an idea</b> opens Quick capture (09).</li>'
   '<li>The Weekly review entry turns to "Ready" on Sunday evening; until then it shows the week so far.</li></ul>'), width=1300)

# ============ 09 QUICK CAPTURE ============
kb_rows = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]
kb = '<div class="dw-kb">'
kb += '<div class="r">' + "".join('<span class="k">%s</span>' % c for c in kb_rows[0]) + '</div>'
kb += '<div class="r">' + "".join('<span class="k">%s</span>' % c for c in kb_rows[1]) + '</div>'
kb += '<div class="r"><span class="k w">⇧</span>' + "".join('<span class="k">%s</span>' % c for c in kb_rows[2]) + '<span class="k w">⌫</span></div>'
kb += '<div class="r"><span class="k w" style="width:88px">123</span><span class="k sp">space</span><span class="k rt">return</span></div></div>'
qc_sheet = (
 '<div class="dw-scrim"></div><div class="dw-sheet" style="bottom:291px;padding-bottom:20px;border-radius:var(--radius-lg)">'
 '<div class="dw-grab"></div>'
 '<label class="t-heading" style="display:block">What would you like to make a habit?</label>'
 '<div class="dw-field focus mt4"><span class="t-body">Practise guitar</span><span class="dw-caret"></span></div>'
 '<p class="t-caption c-ink2 mt2">Saved to Ideas. You can add a schedule whenever you\'re ready.</p>'
 '<button class="dw-btn primary mt4">Save</button>'
 '</div>' + kb
)
files["QuickCapture"] = page("Habits", 920, "09 · Save an intention, no schedule", "Quick capture",
  phone(myh, overlay=qc_sheet) + notes("09", "Quick capture",
   '<p class="t-body">One field and one button. This saves an intention without a schedule.</p>'
   '<ul class="t-caption"><li>Save stays disabled until there\'s text, and Return does the same as Save.</li>'
   '<li>Once saved, the sheet closes and the new chip appears under "Ideas to turn into habits" in My habits.</li>'
   '<li>There are no other fields. Scheduling happens later in Create habit.</li></ul>'))

# ============ 10 CREATE STEP 1 ============
c1 = (
 '<div class="dw-nav"><button class="dw-iconbtn" aria-label="Close">' + ic("close", 24) + '</button><div class="dw-steps"><i class="on"></i><i></i></div><span class="t-label c-ink3" style="width:44px;text-align:right;padding-right:12px">1/2</span></div>'
 '<h1 class="t-title mt6">Make it specific.</h1>'
 '<p class="t-body c-ink2 mt2">A clear, small action is easier to keep.</p>'
 '<label class="dw-label t-label mt6">Name</label>'
 '<div class="dw-field"><span class="t-body">Daily study</span></div>'
 '<label class="dw-label t-label mt6">What will you actually do?</label>'
 '<div class="dw-chips">'
 '<span class="dw-chip on t-label">' + ic("check", 16) + 'Study for 30 minutes</span>'
 '<span class="dw-chip t-label">Study for 15 minutes</span>'
 '<span class="dw-chip t-label">Study one chapter</span>'
 '<span class="dw-chip t-label">Review notes for 10 minutes</span>'
 '<span class="dw-chip t-label" style="border-style:dashed;color:var(--ink-2)">' + ic("edit", 16) + 'Write your own</span>'
 '</div>'
 '<div class="dw-panel mt6"><div class="t-caption c-ink2">Your habit</div><div class="t-body-strong mt1">Study for 30 minutes</div></div>'
 '<div style="position:absolute;left:20px;right:20px;bottom:40px"><button class="dw-btn primary">Next</button></div>'
)
files["CreateHabitStep1"] = page("Habits", 920, "10 · Name, then a concrete action", "Create habit – step 1",
  phone(c1) + notes("10", "Create habit, step 1",
   '<p class="t-body">The user names the habit, then picks a suggested chip to turn it into a concrete action.</p>'
   '<ul class="t-caption"><li>Suggestions come from the name: a length of time, an amount, or a smaller version. "Study" becomes "Study for 30 minutes".</li>'
   '<li>Only one chip can be selected. <b>Write your own</b> replaces the chips with a text field.</li>'
   '<li>The "Your habit" preview is the line that appears in Today. The name stays as the label in My habits.</li>'
   '<li>Next is enabled once there\'s a name and an action.</li></ul>'))

# ============ 11 CREATE STEP 2 ============
def step2(variant):
    head = ('<div class="dw-nav"><button class="dw-iconbtn" aria-label="Back">' + ic("chevron-left", 24) + '</button><div class="dw-steps"><i class="on"></i><i class="on"></i></div><span class="t-label c-ink3" style="width:44px;text-align:right;padding-right:12px">2/2</span></div>'
            '<h1 class="t-title mt5">When would you like to do it?</h1>')
    if variant == "time":
        habit, days_on, summary = "Study for 30 minutes", "MTWTF", "Study for 30 minutes · Mon–Fri · 7:00 p.m."
    else:
        habit, days_on, summary = "Read for 10 minutes", "MTWTFSS", "Read for 10 minutes · Every day · Before bed"
    every = variant != "time"
    s = head + '<p class="t-caption c-ink2 mt1">%s</p>' % habit
    s += '<div class="dw-seg mt5"><span class="t-label%s">Every day</span><span class="t-label%s">Selected days</span></div>' % (" on" if every else "", "" if every else " on")
    s += '<div class="dw-days mt3">' + "".join('<span class="t-label%s">%s</span>' % (" on" if (variant != "time" or i < 5) else "", d) for i, d in enumerate("MTWTFSS")) + '</div>'
    s += '<div class="dw-seg mt6"><span class="t-label%s">At a time</span><span class="t-label%s">With a routine</span></div>' % (" on" if variant == "time" else "", "" if variant == "time" else " on")
    if variant == "time":
        s += ('<div class="dw-field mt3 between"><span class="row">' + ic("clock", 20, "c-ink2") + '<span class="t-body">7:00 p.m.</span></span>' + ic("chevron-right", 18, "c-ink3") + '</div>'
              '<div class="between mt4" style="min-height:52px;border-bottom:1px solid var(--line)"><span class="row">' + ic("bell", 20, "c-ink2") + '<span class="t-body">Remind me at 7:00 p.m.</span></span><span class="dw-toggle on"></span></div>')
    else:
        opts = [("sunrise", "Morning", False), ("sun", "After lunch", False), ("moon", "After dinner", False), ("moon", "Before bed", True)]
        s += '<div class="mt2">' + "".join('<div class="dw-opt"><span class="dw-radio%s"></span><span class="t-body grow">%s</span></div>' % (" on" if on else "", n) for _, n, on in opts) + '</div>'
        s += ('<div class="mt4 between" style="min-height:52px"><span class="row">' + ic("bell", 20, "c-ink2") + '<span><span class="t-body">Reminder time</span> <span class="t-caption c-ink3">Optional</span></span></span>'
              '<span class="dw-sbtn outline t-label">Add time</span></div>')
    s += ('<div style="position:absolute;left:20px;right:20px;bottom:40px"><p class="t-caption c-ink2" style="text-align:center;margin-bottom:12px">%s</p>'
          '<button class="dw-btn primary">Save</button></div>' % summary)
    return s
files["CreateHabitStep2"] = page("Habits", 920, "11 · Days, then a time or a routine anchor", "Create habit – step 2",
  labeled("Daily study: selected days, at a time", phone(step2("time"))) + labeled("Read for 10 minutes: routine anchor", phone(step2("anchor")))
  + notes("11", "Create habit, step 2",
   '<p class="t-body">First choose the days, then either a time or a routine anchor.</p>'
   '<ul class="t-caption"><li><b>Every day</b> fills all seven days. <b>Selected days</b> lets each day be toggled.</li>'
   '<li><b>At a time</b> uses a time picker, and the reminder is on by default at that time.</li>'
   '<li><b>With a routine</b> offers Morning, After lunch, After dinner and Before bed. It still asks for an <b>optional</b> reminder time, which is off unless one is added.</li>'
   '<li>The summary line above Save reads the habit back in plain words. Save adds it to My habits and to Today if it\'s due.</li></ul>'), width=1300)

# ============ 12 WEEKLY REVIEW ============
def wr(title, sched, spec, label):
    return ('<li class="dw-item"><div class="grow"><div class="t-body-strong">%s</div><div class="dw-meta t-caption">%s</div></div>'
            '<div style="text-align:right">%s<div class="t-caption c-ink2 mt1">%s</div></div></li>' % (title, sched, dots(spec), label))
review = (
 nav("Weekly review")
 + '<div class="t-overline up c-ink3 mt3">26 October – 1 November</div>'
 '<h1 class="t-title mt1">A steady week.</h1>'
 '<p class="t-body c-ink2 mt1">Every habit kept its streak this week.</p>'
 '<div class="dw-tint mt5">'
   '<div class="between"><div><div class="t-caption c-accent">Needs a tweak</div><div class="t-body-strong mt1">Daily study</div><div class="t-caption c-ink2">Study for 30 minutes · Mon–Fri · 7:00 p.m.</div></div></div>'
   '<div class="between mt3"><span>' + dots("ddkdd") + '</span><span class="t-label">4 of 5 days</span></div>'
   '<p class="t-body mt3">Wednesday was skipped. Would 6:00 p.m. be easier than 7:00?</p>'
   '<button class="dw-btn primary mt4" style="height:48px">' + ic("clock", 18) + 'Change time to 6:00 p.m.</button>'
   '<div class="row mt2" style="gap:8px"><button class="dw-btn secondary grow" style="height:44px;background:var(--bg)">' + ic("pause", 18) + 'Pause</button>'
   '<button class="dw-btn secondary grow" style="height:44px;background:var(--bg)">' + ic("archive", 18) + 'Remove</button></div>'
 '</div>'
 '<div class="dw-sechead"><h2 class="t-heading">This week</h2><span class="t-caption c-ink3">Mon–Sun</span></div>'
 '<ul class="dw-list">'
 + wr("Stretch for 5 minutes", "Every day · Morning", "ddddddd", "7 of 7 days")
 + wr("Read for 10 minutes", "Every day · Before bed", "dddkddd", "6 of 7 days · 1 skipped")
 + wr("Short walk", "Every day · After lunch", "dddddkd", "6 of 7 days · 1 rescheduled")
 + '</ul>'
 '<div class="row mt3 t-caption c-ink2" style="gap:14px;flex-wrap:wrap">'
   '<span class="row" style="gap:6px">' + dots("d") + 'Done</span>'
   '<span class="row" style="gap:6px">' + dots("k") + 'Skipped or rescheduled · streak kept</span>'
   '<span class="row" style="gap:6px">' + dots("m") + 'Missed</span></div>'
 '<div class="dw-sechead"><h2 class="t-heading">Turn one into a habit?</h2></div>'
 '<ul class="dw-list">'
 '<li class="dw-item"><span class="dw-lead">' + ic("idea", 20) + '</span><span class="t-body grow">Practise guitar</span><span class="dw-sbtn outline t-label">Make it a habit</span></li>'
 '<li class="dw-item"><span class="dw-lead">' + ic("idea", 20) + '</span><span class="t-body grow">Cook a new recipe</span><span class="dw-sbtn outline t-label">Make it a habit</span></li>'
 '</ul>'
 '<div class="dw-sechead"><h2 class="t-heading">Which habits felt manageable?</h2></div>'
 '<p class="t-caption c-ink2 mb">A sentence is plenty. Only you see this.</p>'
 '<div class="dw-textarea t-body mt3">Stretching and reading felt easy. Studying after a long day was harder…</div>'
 '<button class="dw-btn secondary mt4">Save reflection</button>'
)
files["WeeklyReview"] = page("Habits", 1400, "12 · Completion, one suggestion, ideas, reflection", "Weekly review",
  phone(review, time="6:30", long=True) + notes("12", "Weekly review",
   '<p class="t-body">Opens from My habits on Sunday evening and covers Monday to Sunday. Shown here as one long scroll, with the dashed line marking the 844px fold.</p>'
   '<ul class="t-caption"><li>Only the habit with the <b>lowest completion</b> is highlighted, on <b>accent-tint</b>, with a single concrete suggestion and three options: <b>Change time</b>, <b>Pause</b> and <b>Remove</b>.</li>'
   '<li>Daily study: 4 of 5 Done, Wednesday skipped (a kept ring), so its streak held. The suggestion is about timing, not effort.</li>'
   '<li>Skipped and rescheduled days show as kept rings, never as misses.</li>'
   '<li>"Make it a habit" opens Create habit (10) with the idea\'s name filled in.</li>'
   '<li>The reflection is free text and optional, and the user can leave without filling it in.</li></ul>'))

# ============ FOUNDATIONS: controls & streak legend ============
ctrl = (
 '<div style="background:var(--bg);border-radius:var(--radius-md);padding:28px;width:880px;display:grid;grid-template-columns:1fr 1fr;gap:28px 40px">'
 '<div><div class="t-overline up c-ink3">Check-in ring</div><div class="row mt3" style="gap:20px">' + check(False) + '<span class="t-caption c-ink2">Open</span>' + check(True) + '<span class="t-caption c-ink2">Done</span></div></div>'
 '<div><div class="t-overline up c-ink3">Row actions</div><div class="row mt3" style="gap:4px"><button class="dw-sbtn">' + ic("check", 16) + 'Done</button><button class="dw-sbtn">' + ic("skip", 16) + 'Skip</button><button class="dw-sbtn">' + ic("reschedule", 16) + 'Reschedule</button></div></div>'
 '<div><div class="t-overline up c-ink3">Buttons</div><button class="dw-btn primary mt3">Start on YouTube ' + ic("external", 18) + '</button><button class="dw-btn secondary mt2">Schedule for later</button><button class="dw-btn tertiary">Remind me later</button></div>'
 '<div><div class="t-overline up c-ink3">Chips &amp; segmented</div><div class="dw-chips mt3"><span class="dw-chip t-label">Peace</span><span class="dw-chip on t-label">Focus</span><span class="dw-chip t-label">Sleep</span></div>'
 '<div class="dw-seg mt3"><span class="t-label on">Today</span><span class="t-label">My habits</span></div>'
 '<div class="dw-field focus mt3"><span class="t-body">Practise guitar</span><span class="dw-caret"></span></div></div>'
 '<div style="grid-column:1 / -1"><div class="t-overline up c-ink3">Outline icons · 24px grid · 1.75 stroke</div><div class="row mt3" style="flex-wrap:wrap;gap:18px">'
 + "".join('<span title="%s">%s</span>' % (n, ic(n, 24)) for n in ICONS)
 + '</div></div></div>'
)
files["Controls"] = page("Foundations", 560, "Shared controls and the icon set", "Controls", ctrl)

legend = (
 '<div style="background:var(--bg);border-radius:var(--radius-md);padding:28px;width:880px">'
 '<div class="t-overline up c-ink3">Streak rules</div>'
 '<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:16px" class="mt3">'
 + "".join('<div class="dw-panel"><div class="row">%s<span class="t-body-strong">%s</span></div><p class="t-caption c-ink2 mt2">%s</p></div>' % (dots(c), t, d) for c, t, d in [
   ("d", "Done", "Counts. Adds a day to the streak."),
   ("k", "Skip / Reschedule", "Keeps the streak. Doesn’t add, doesn’t break."),
   ("m", "Missed", "Not checked off by midnight. Streak starts again, quietly."),
   ("n", "Not scheduled", "Days the habit isn’t planned. Ignored."),
 ])
 + '</div><p class="t-caption c-ink2 mt4">Meditation is self-reported: tapping Done is enough. Never ask for proof.</p></div>'
)
files["StreakLegend"] = page("Foundations", 260, "Done, kept, missed — one legend everywhere", "Streak legend", legend)

# ============ README per component ============
READMES = {
 "Home": "The hub screen: greeting, one Today list across habits, meditation and exercise with one-tap check-in rings, a progress strip and three section entry points.\n\n- Consumer provides: today's items in time order (type, title, meta, done state), the longest active streak, today's done/total and the latest badge.\n- A check-in here updates the same item in its own section.\n- Do: keep done items in place, greyed to `ink-3`. Don't: count what's left or show warnings.",
 "MeditationBrowse": "Meditation search: type chips (Meditation, Breathwork, Affirmations), a search field, intention and length filters, and result cards.\n\n- Each card shows title, length, source and intention. No thumbnails, no player.\n- Selected chips use `ink`. The accent is reserved for progress.",
 "SessionDetail": "Session detail with two actions, Start on YouTube (primary) and Schedule for later (secondary), plus the note \"This opens YouTube. Come back to log it.\"\n\n- Leaving via Start arms the return check-in (CheckInSheet).",
 "CheckInSheet": "The bottom sheet shown on return from an external session, asking \"Did you complete …?\" with Done, Not this time and Remind me later.\n\n- Self-reported: never ask for proof. Not this time is neutral, with no streak warning.",
 "FollowUpNotification": "The lock-screen notification sent once if the user doesn't return: \"Finished your session? Tap to check in.\"\n\n- Opens the app on the check-in sheet. Never repeats.",
 "CompletionFeedback": "The short confirmation after Done: a check mark, the updated streak with week dots, and a badge card only when one was earned.",
 "HabitsToday": "The Habits default tab: today's habits grouped by Morning, During the day and Evening, each with Done, Skip and Reschedule, plus the All done for today state.\n\n- Skip and Reschedule keep the streak. Show \"Streak kept\".",
 "MyHabits": "All active habits grouped by routine, with schedule and next due date, a ··· menu (Pause, Edit, Archive) and an \"Ideas to turn into habits\" section for saved intentions.",
 "QuickCapture": "A bottom sheet with a single field, \"What would you like to make a habit?\", and Save. It saves an intention with no schedule.",
 "CreateHabitStep1": "Create habit, step 1, \"Make it specific.\": a name plus suggested chips that turn it into a concrete action (\"Study\" → \"Study for 30 minutes\").",
 "CreateHabitStep2": "Create habit, step 2, \"When would you like to do it?\": every day or selected days, then a time or a routine anchor (Morning, After lunch, After dinner, Before bed) with an optional reminder, then Save.",
 "WeeklyReview": "The weekly review: per-habit completion (\"4 of 5 days\"), the lowest habit highlighted with Change time, Pause and Remove, saved intentions to turn into habits, and the reflection prompt \"Which habits felt manageable?\"",
 "Controls": "The shared controls: the check-in ring, row actions, buttons, chips, the segmented control, the focused input and the outline icon set (`.ic .ic-<name>`).",
 "StreakLegend": "The one legend for streak states, used in every week-dot row: Done counts, Skip and Reschedule keep the streak, an item unchecked by midnight is Missed, and meditation is self-reported.",
}

os.makedirs(COMP, exist_ok=True)
with open(os.path.join(COMP, "bundle.css"), "w") as f:
    f.write(BUNDLE_CSS + "\n/* icons */\n" + icon_css() + "\n")
for name, html in files.items():
    d = os.path.join(COMP, name); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "preview.html"), "w").write(html)
    open(os.path.join(d, "README.md"), "w").write("# %s\n\n%s\n" % (name, READMES[name]))
print("ok", len(files))
