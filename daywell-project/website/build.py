import os, re, json
from bs4 import BeautifulSoup

HERE = os.path.dirname(os.path.abspath(__file__))

# ---- phone styles: tokens + shared screen CSS, scoped so they don't touch the page ----
t = json.load(open(os.path.join(HERE, "tokens.json")))
tok = ":root{"
for c in t["color"]["tokens"]:
    v = c["value"] if isinstance(c["value"], str) else c["value"]["light"]
    tok += "--%s:%s;" % (c["name"], re.sub(r"^\{(.*)\}$", r"var(--\1)", v))
for fam in ("spacing", "radius", "shadow"):
    for c in t[fam]["tokens"]:
        tok += "--%s:%s;" % (c["name"], c["value"])
tok += "--font-sans:%s;}\n" % t["type"]["families"]["sans"]
for g in t["type"]["groups"]:
    for s in g["styles"]:
        tok += ".%s{font-family:var(--font-sans);font-size:%s;line-height:%s;font-weight:%s;%s}\n" % (
            s["name"], s["fontSize"], s["lineHeight"], s["fontWeight"],
            ("letter-spacing:%s;" % s["letterSpacing"]) if s.get("letterSpacing") else "")
bundle = open(os.path.join(HERE, "screens", "bundle.css")).read()
bundle = re.sub(r'@import url\([^)]*\);\n', "", bundle)
bundle = bundle.replace("html,body{background:var(--canvas);color:var(--ink);font-family:var(--font-sans);-webkit-font-smoothing:antialiased}",
                        ".dw-phone{color:var(--ink);font-family:var(--font-sans);text-align:left}")
bundle = bundle.replace("*{box-sizing:border-box;margin:0;padding:0}", ".dw-phone,.dw-phone *{box-sizing:border-box;margin:0;padding:0}")

def phone(name, idx=0):
    soup = BeautifulSoup(open(os.path.join(HERE, "screens", name + ".html")).read(), "html.parser")
    return str(soup.select(".dw-phone")[idx])

# ---- brand marks ----
DW_SUN = ('<path d="M6 12v24h5a12 12 0 0 0 0-24z" fill="none" stroke="currentColor" stroke-width="4.5" stroke-linejoin="round"/>'
          '<path d="M30 20v10a6 6 0 0 0 12 0v-3v3a6 6 0 0 0 12 0V20" fill="none" stroke="currentColor" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>'
          '<circle cx="42" cy="15" r="3.8" fill="var(--sun,currentColor)"/>')

def app_icon(size, cls=""):
    return ('<span class="lp-appicon %s" style="width:%dpx;height:%dpx"><svg viewBox="0 0 60 48" width="%d" height="%d" aria-hidden="true">%s</svg></span>'
            % (cls, size, size, int(size * .66), int(size * .66), DW_SUN))

def wordmark(h, cls=""):
    return ('<svg class="lp-wm %s" viewBox="0 0 200 60" height="%d" role="img" aria-label="Daywell">'
            '<text class="wt" x="0" y="44" font-family="Figtree,sans-serif" font-weight="600" font-size="52" letter-spacing="-1" fill="currentColor">daywe</text>'
            '<rect class="p1" x="150" y="6.5" width="9.5" height="37.5" rx="4.75" fill="currentColor"/>'
            '<rect class="p2" x="166" y="8.25" width="9.5" height="34" rx="4.75" fill="none" stroke="var(--pill,currentColor)" stroke-width="3.5"/></svg>') % (cls, h)

def ico(path, size=22):
    return ('<svg viewBox="0 0 24 24" width="%d" height="%d" fill="none" stroke="currentColor" stroke-width="1.75" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>') % (size, size, path)

I_LIST = '<path d="M9 6h11M9 12h11M9 18h11"/><circle cx="4.5" cy="6" r="1"/><circle cx="4.5" cy="12" r="1"/><circle cx="4.5" cy="18" r="1"/>'
I_CHECK = '<circle cx="12" cy="12" r="8.5"/><path d="M8 12.3l2.8 2.8L16.2 9.6"/>'
I_CHART = '<path d="M4 20h16M7 16v-5M12 16V6M17 16v-8"/>'
I_EXT = '<path d="M14 4h6v6"/><path d="M20 4l-9 9"/><path d="M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/>'

dot = lambda c: '<span class="lp-dot lp-dot-%s" aria-hidden="true"></span>' % c

html = open(os.path.join(HERE, "template.html")).read()
for k, v in {
    "/*PHONE_CSS*/": tok + bundle,
    "<!--WM_HEADER-->": wordmark(28),
    "<!--WM_FOOTER-->": wordmark(26),
    "<!--ICON_HERO-->": app_icon(44),
    "<!--ICON_APP-->": app_icon(112, "lp-appicon-lg"),
    "<!--ICON_FOOT-->": app_icon(36),
    "<!--PHONE_HOME-->": phone("Home"),
    "<!--PHONE_HABITS-->": phone("HabitsToday"),
    "<!--PHONE_CHECKIN-->": phone("CheckInSheet"),
    "<!--PHONE_DONE-->": phone("CompletionFeedback"),
    "<!--I_LIST-->": ico(I_LIST), "<!--I_CHECK-->": ico(I_CHECK), "<!--I_CHART-->": ico(I_CHART), "<!--I_EXT-->": ico(I_EXT, 18),
    "<!--D_DONE-->": dot("done"), "<!--D_KEPT-->": dot("kept"), "<!--D_MISS-->": dot("miss"), "<!--D_OFF-->": dot("off"),
}.items():
    html = html.replace(k, v)
open(os.path.join(HERE, "index.html"), "w").write(html)
print("ok", len(html))
