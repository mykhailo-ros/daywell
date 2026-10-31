import math
def pt(cx,cy,r,a):
    a=math.radians(a); return (round(cx+r*math.cos(a),2), round(cy+r*math.sin(a),2))

# all marks on a 48 grid; currentColor = primary ink, --two = second tone (defaults to currentColor)
s1,e1 = pt(24,24,13,-55), pt(24,24,13,-125)
MARKS = {
"kept": dict(name="Kept dot", lean="Product-native, systematic",
  svg='<circle cx="13.5" cy="24" r="8.5" fill="currentColor"/><circle cx="34" cy="24" r="7.5" fill="none" stroke="var(--two,currentColor)" stroke-width="3.5"/>',
  idea="The streak legend, reduced to two marks: a filled dot for Done and a ring for a kept day. It says “a skip doesn't break it” without words.",
  good=["Built straight from the product's own visual language","Reads instantly at 20px","Easy to animate: the ring fills in on check-in"],
  watch=["Abstract: needs the name beside it at first","Two dots is a familiar shape in tech logos"]),
"horizon": dict(name="Horizon", lean="Calm, wellbeing, warm",
  svg='<path d="M9 31a15 15 0 0 1 30 0z" fill="var(--two,currentColor)"/><rect x="6" y="35" width="36" height="4" rx="2" fill="currentColor"/>',
  idea="A sun resting on a line. One day, steady and unhurried. The line under it suggests a routine you stand on.",
  good=["Warmest and most “wellbeing” of the five","Simple silhouette that holds up at any size","Links to the name: Day"],
  watch=["Sunrise marks are common in wellness","Less tied to tracking and streaks"]),
"arc": dict(name="Day arc D", lean="Monogram, confident, letter-led",
  svg='<path d="M14 11.5v25h7a12.5 12.5 0 0 0 0-25z" fill="none" stroke="currentColor" stroke-width="5" stroke-linejoin="round"/><circle cx="21.5" cy="24" r="4.2" fill="var(--two,currentColor)"/>',
  idea="A rounded D with a sun inside it: the day as a container for one small thing. It's a letter first and a symbol second.",
  good=["Owns the initial, which works well for an app icon","Most distinctive outline of the five","The dot carries the accent nicely"],
  watch=["The inner dot gets small below 20px","More “brand” than “product” in feel"]),
"loop": dict(name="Daily loop", lean="Routine, habit, continuity",
  svg='<path d="M%s %s A13 13 0 1 1 %s %s" fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="round"/><circle cx="24" cy="11" r="3.6" fill="var(--two,currentColor)"/>' % (s1+e1),
  idea="An almost-closed ring with today as the dot in the opening. Each check-in closes the loop, and the ring is the routine that comes back every day.",
  good=["Shows the habit loop: repeat, return","Very calm, nothing sharp","Matches the round check-in control in the app"],
  watch=["Close to “power” and “refresh” icons","The meaning needs a moment to land"]),
"word": dict(name="Wordmark", lean="Typographic, friendly, quiet",
  svg=None,
  idea="No separate symbol. “daywell” in lowercase Figtree, with the double l drawn as two pills, one filled and one outlined, so the streak idea hides inside the name. The app icon uses the lowercase d.",
  good=["Puts the name front and centre while it's new","Matches the UI typeface exactly","The pill detail rewards a second look"],
  watch=["The app icon is just a letter, so it's weaker on a busy home screen","The pill detail disappears at small sizes"]),
}

def mark(key, size, color="currentColor", two=None, extra=""):
    st = 'color:%s;%s' % (color, ('--two:%s;' % two) if two else '')
    if key == "word":
        return ('<svg viewBox="0 0 48 48" width="%s" height="%s" style="%s" aria-hidden="true" %s>'
                '<text x="24" y="35" text-anchor="middle" font-family="Figtree,sans-serif" font-weight="600" font-size="34" fill="currentColor">d</text></svg>') % (size,size,st,extra)
    return '<svg viewBox="0 0 48 48" width="%s" height="%s" style="%s" aria-hidden="true" %s>%s</svg>' % (size,size,st,extra,MARKS[key]["svg"])

def lockup(key, h=44, color="var(--ink)", two="var(--accent)"):
    if key == "word":
        return ('<svg class="wm" viewBox="0 0 230 60" height="%d" style="color:%s;--two:%s" aria-label="daywell">'
                '<text class="wt" x="0" y="44" font-family="Figtree,sans-serif" font-weight="600" font-size="52" letter-spacing="-1" fill="currentColor">daywe</text>'
                '<rect class="p1" x="150" y="6" width="9" height="38" rx="4.5" fill="currentColor"/>'
                '<rect class="p2" x="166" y="7.75" width="7.5" height="34.5" rx="3.75" fill="none" stroke="var(--two)" stroke-width="3.5"/></svg>') % (h, color, two)
    return '<span class="lock" style="color:%s">%s<span class="lname">Daywell</span></span>' % (color, mark(key, h, color, two))

def icon(key, bg, fg, two=None, size=96):
    return '<span class="appicon" style="width:%dpx;height:%dpx;background:%s">%s</span>' % (size,size,bg,mark(key, int(size*.62), fg, two))

cards=[]
for i,(k,m) in enumerate(MARKS.items(),1):
    cards.append(f'''
<section class="variant" id="v-{k}">
  <header class="vhead"><span class="vnum">{i:02d}</span><h2>{m["name"]}</h2><span class="lean">Leans: {m["lean"]}</span></header>
  <div class="vgrid">
    <div class="hero">{mark(k,"60%","var(--ink)","var(--accent)") if k!="word" else lockup(k,72)}</div>
    <div class="side">
      <p class="idea">{m["idea"]}</p>
      <div class="lockrow">{lockup(k) if k!="word" else mark(k,56,"var(--ink)")}</div>
      <div class="icons">
        <figure>{icon(k,"var(--accent)","#ffffff")}<figcaption>Accent</figcaption></figure>
        <figure>{icon(k,"#161616","#ffffff","#86c2b2")}<figcaption>Ink</figcaption></figure>
        <figure>{icon(k,"#ffffff","#161616","#2f6f62")}<figcaption>Light</figcaption></figure>
      </div>
      <div class="sizes">
        {"".join(f'<figure><span class="sz">{mark(k,s,"var(--ink)")}</span><figcaption>{s}px</figcaption></figure>' for s in (48,32,20,16))}
        <figure><span class="notif"><span class="nt">{mark(k,14,"#ffffff")}</span><span class="nl">DAYWELL</span></span><figcaption>Notification · 20px, one colour</figcaption></figure>
      </div>
      <div class="pc"><div><h3>Works because</h3><ul>{"".join(f"<li>{x}</li>" for x in m["good"])}</ul></div>
      <div><h3>Watch out</h3><ul>{"".join(f"<li>{x}</li>" for x in m["watch"])}</ul></div></div>
    </div>
  </div>
</section>''')

strip = "".join(f'<a class="chip" href="#v-{k}">{icon(k,"var(--accent)","#ffffff",size=64)}<span><b>{i:02d}</b> {m["name"]}</span></a>' for i,(k,m) in enumerate(MARKS.items(),1))
home = "".join(f'<span class="hs">{icon(k,"var(--accent)","#ffffff",size=60)}<span>Daywell</span></span>' for k in MARKS)

html = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Daywell Logo Directions</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600&family=IBM+Plex+Mono:wght@500&display=swap">
<style>
/* Layout: a comparison strip of all five as app icons, then one section per direction: big mark, then the mark in real use (lockup, icons, small sizes, notification). */
:root{{--bg:#f3f3f0;--panel:#ffffff;--ink:#161616;--muted:#55554f;--line:#dcdcd6;--accent:#2f6f62;--tint:#e7f0ec;
  --sans:Figtree,"Helvetica Neue",system-ui,sans-serif;--mono:"IBM Plex Mono",ui-monospace,Menlo,monospace}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#131514;--panel:#1c1f1e;--ink:#ecece8;--muted:#a6a9a4;--line:#323634;--accent:#86c2b2;--tint:#1f2b28;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#131514;--panel:#1c1f1e;--ink:#ecece8;--muted:#a6a9a4;--line:#323634;--accent:#86c2b2;--tint:#1f2b28;color-scheme:dark}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);font-size:15px;line-height:1.5}}
.wrap{{max-width:1180px;margin:0 auto;padding:40px max(16px,env(safe-area-inset-right,0px)) 72px max(16px,env(safe-area-inset-left,0px))}}
.eyebrow{{font-family:var(--mono);font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin:0}}
h1{{font-size:clamp(32px,5vw,46px);line-height:1.05;letter-spacing:-.02em;margin:6px 0 10px;font-weight:600;text-wrap:balance}}
.lede{{max-width:62ch;color:var(--muted);margin:0}}
.strip{{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;margin:28px 0 12px}}
.chip{{display:flex;align-items:center;gap:12px;padding:12px;border:1px solid var(--line);border-radius:16px;background:var(--panel);color:var(--ink);text-decoration:none}}
.chip:hover,.chip:focus-visible{{border-color:var(--accent);outline:none}}
.chip b{{font-family:var(--mono);font-weight:500;font-size:12px;color:var(--accent);margin-right:4px}}
.homes{{display:flex;flex-wrap:wrap;gap:20px 28px;padding:22px 24px;border-radius:20px;background:#1d2422;margin-bottom:8px}}
.hs{{display:flex;flex-direction:column;align-items:center;gap:6px;color:#fff;font-size:11px}}
.cap{{font-size:13px;color:var(--muted);margin:0 0 8px}}
.appicon{{display:inline-flex;align-items:center;justify-content:center;border-radius:23%;box-shadow:0 0 0 1px rgba(0,0,0,.08);flex:none}}
.variant{{margin-top:48px;padding-top:28px;border-top:1px solid var(--line)}}
.vhead{{display:flex;flex-wrap:wrap;align-items:baseline;gap:6px 14px;margin-bottom:18px}}
.vnum{{font-family:var(--mono);font-size:13px;color:var(--accent)}}
.vhead h2{{margin:0;font-size:26px;letter-spacing:-.01em;font-weight:600}}
.lean{{font-size:13px;padding:3px 10px;border-radius:99px;background:var(--tint);color:var(--accent);font-weight:500}}
.vgrid{{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:24px}}
.hero{{background:var(--panel);border-radius:20px;aspect-ratio:1;max-width:100%;display:flex;align-items:center;justify-content:center;border:1px solid var(--line)}}
.hero svg.wm{{width:78%;height:auto}}
.side{{display:flex;flex-direction:column;gap:20px;min-width:0}}
.idea{{margin:0;font-size:17px;line-height:1.5;max-width:56ch}}
.lockrow{{padding:20px 22px;background:var(--panel);border-radius:16px;border:1px solid var(--line);display:flex;align-items:center}}
.lock{{display:inline-flex;align-items:center;gap:12px}}
.lname{{font-weight:600;font-size:34px;letter-spacing:-.02em;line-height:1}}
.icons,.sizes{{display:flex;flex-wrap:wrap;gap:18px;align-items:flex-end}}
figure{{margin:0;display:flex;flex-direction:column;align-items:center;gap:6px}}
figcaption{{font-size:12px;color:var(--muted)}}
.sz{{display:flex;align-items:center;justify-content:center;min-height:48px}}
.notif{{display:inline-flex;align-items:center;gap:8px;background:#161616;color:#fff;border-radius:12px;padding:10px 14px;min-height:48px}}
.nt{{width:20px;height:20px;border-radius:5px;background:#2f6f62;display:inline-flex;align-items:center;justify-content:center}}
.nl{{font-size:11px;letter-spacing:.06em;color:#c8cbc6}}
.pc{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}
.pc h3{{margin:0 0 4px;font-size:13px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);font-weight:600}}
.pc ul{{margin:0;padding-left:18px}}
.pc li{{margin-bottom:4px}}
.next{{margin-top:56px;padding:24px;border-radius:20px;background:var(--panel);border:1px solid var(--line)}}
.next h2{{margin:0 0 8px;font-size:22px}}
.next ol{{margin:0;padding-left:20px;max-width:70ch}}
@media (max-width:760px){{.vgrid,.pc{{grid-template-columns:1fr}}.hero{{max-width:360px}}}}
</style></head><body><div class="wrap">
<p class="eyebrow">Daywell · logo exploration · round 1</p>
<h1>Five directions</h1>
<p class="lede">Each direction leans a different way: product, calm, letter, routine, type. All are drawn on a 48-unit grid in black first, with the sage accent as an optional second tone. They're shown here at the sizes they'll really be used.</p>
<div class="strip">{strip}</div>
<p class="cap">On a home screen, at real size:</p>
<div class="homes">{home}</div>
{"".join(cards)}
<section class="next"><h2>To choose a direction</h2><ol>
<li>Pick the one or two that feel most like Daywell. It's fine to like a direction and dislike its drawing.</li>
<li>Say what to keep from the others, for example the warmth of Horizon with the system of Kept dot.</li>
<li>Next round: three refinements of the chosen direction, the wordmark tuned to match, and a trademark search on the shortlist.</li>
</ol></section>
</div>
<script>
function placePills(){{
  document.querySelectorAll('svg.wm').forEach(svg => {{
    const t = svg.querySelector('.wt'); let w = 0;
    try {{ w = t.getComputedTextLength(); }} catch (e) {{ return; }}
    const x1 = w + 5; svg.querySelector('.p1').setAttribute('x', x1);
    svg.querySelector('.p2').setAttribute('x', x1 + 9 + 6.25);
    svg.setAttribute('viewBox', '0 0 ' + Math.ceil(x1 + 9 + 6.25 + 9.5 + 4) + ' 60');
  }});
}}
placePills();
if (document.fonts && document.fonts.ready) document.fonts.ready.then(placePills);
</script></body></html>'''
open("index.html","w").write(html)
print(len(html))
