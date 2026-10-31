import os, json, re
from bs4 import BeautifulSoup

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "dw", "project")
C = os.path.join(P, "components")

# --- tokens.css equivalent (phone internals) ---
t = json.load(open(os.path.join(P, "tokens.json")))
css = ":root{"
for c in t["color"]["tokens"]:
    v = c["value"] if isinstance(c["value"], str) else c["value"]["light"]
    v = re.sub(r"^\{(.*)\}$", r"var(--\1)", v)
    css += "--%s:%s;" % (c["name"], v)
for fam in ("spacing", "radius", "shadow"):
    for c in t[fam]["tokens"]:
        css += "--%s:%s;" % (c["name"], c["value"])
css += "--font-sans:%s;}\n" % t["type"]["families"]["sans"]
for g in t["type"]["groups"]:
    for s in g["styles"]:
        css += ".%s{font-family:var(--font-sans);font-size:%s;line-height:%s;font-weight:%s;%s}\n" % (
            s["name"], s["fontSize"], s["lineHeight"], s["fontWeight"],
            ("letter-spacing:%s;" % s["letterSpacing"]) if s.get("letterSpacing") else "")
bundle = open(os.path.join(C, "bundle.css")).read()
bundle = re.sub(r'@import url\([^)]*\);\n', "", bundle)
bundle = bundle.replace("html,body{background:var(--canvas);color:var(--ink);font-family:var(--font-sans);-webkit-font-smoothing:antialiased}",
                        ".dw-phone{color:var(--ink);font-family:var(--font-sans);-webkit-font-smoothing:antialiased;text-align:left}")
bundle = bundle.replace("*{box-sizing:border-box;margin:0;padding:0}", ".dw-phone,.dw-phone *{box-sizing:border-box;margin:0;padding:0}")

def load(name):
    soup = BeautifulSoup(open(os.path.join(C, name, "preview.html")).read(), "html.parser")
    phones = [str(p) for p in soup.select(".dw-phone")]
    aside = soup.select_one(".dw-notes")
    lead = aside.select_one("p")
    ul = aside.select_one("ul")
    return phones, (str(lead.decode_contents()) if lead else ""), (str(ul.decode_contents()) if ul else "")

# (component, phone index, number, title, how you get here)
SECTIONS = [
 ("Start", "Every session begins on Home: today's plan across the app.", [
   ("Home", 0, "01", "Home", "Opens the app"),
 ]),
 ("Meditation", "Find a session, do it on YouTube, come back and log it.", [
   ("MeditationBrowse", 0, "02", "Browse", "Taps the Meditation tile"),
   ("SessionDetail", 0, "03", "Session detail", "Taps “Morning focus breath”"),
   ("FollowUpNotification", 0, "05", "Follow-up notification", "Taps Start on YouTube and leaves. Sent once, only if they don't come back"),
   ("CheckInSheet", 0, "04", "Check-in on return", "Returns to Daywell (or taps the notification)"),
   ("CompletionFeedback", 0, "06", "Completion feedback", "Taps Done"),
 ]),
 ("Habits", "Check in today, organise habits, capture and create, then review the week.", [
   ("HabitsToday", 0, "07", "Habits – Today", "Back to Today, then taps the Habits tile"),
   ("HabitsToday", 1, "07", "All done for today", "Checks in the last habit of the day"),
   ("MyHabits", 0, "08", "My habits", "Switches to the My habits tab"),
   ("MyHabits", 1, "08", "Habit menu", "Taps ··· on Daily study"),
   ("QuickCapture", 0, "09", "Quick capture", "Taps Save an idea"),
   ("CreateHabitStep1", 0, "10", "Create habit, step 1", "Taps + in the Habits header"),
   ("CreateHabitStep2", 0, "11", "Create habit, step 2", "Taps Next"),
   ("CreateHabitStep2", 1, "11", "Step 2 with a routine anchor", "Same step for “Read for 10 minutes”"),
   ("WeeklyReview", 0, "12", "Weekly review", "Sunday evening: taps Weekly review in My habits"),
 ]),
]

cache = {}
steps = []
for sec, sub, items in SECTIONS:
    for comp, idx, num, title, how in items:
        if comp not in cache:
            cache[comp] = load(comp)
        phones, lead, ul = cache[comp]
        steps.append(dict(section=sec, comp=comp, phone=phones[idx], num=num, title=title, how=how, lead=lead, notes=ul))

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

body = []
i = 0
for sec, sub, items in SECTIONS:
    body.append('<section class="lane" aria-labelledby="h-%s"><header class="lane-head"><h2 id="h-%s">%s</h2><p>%s</p></header><ol class="track">' % (sec, sec, sec, sub))
    for k, _ in enumerate(items):
        s = steps[i]
        body.append(
          '<li class="step">'
          '<div class="how"><span>%s</span></div>'
          '<div class="frame" role="button" tabindex="0" data-i="%d" aria-label="Present %s"><div class="zoom" inert>%s</div></div>'
          '<div class="cap"><span class="num">%s</span><span class="ttl">%s</span></div>'
          '</li>' % (esc(s["how"]), i, esc(s["title"]), s["phone"], s["num"], esc(s["title"])))
        i += 1
    body.append('</ol></section>')

data = [dict(section=s["section"], num=s["num"], title=s["title"], how=s["how"], lead=s["lead"], notes=s["notes"]) for s in steps]

html = open(os.path.join(HERE, "flow_template.html")).read()
html = html.replace("/*PHONE_TOKENS*/", css).replace("/*PHONE_CSS*/", bundle)
html = html.replace("<!--LANES-->", "\n".join(body)).replace("/*STEPS*/", json.dumps(data).replace("</", "<\\/"))
html = html.replace("<!--COUNT-->", str(len(steps)))
os.makedirs(os.path.join(HERE, "flow"), exist_ok=True)
open(os.path.join(HERE, "flow", "daywell-flow.html"), "w").write(html)
print("ok", len(steps), len(html))
