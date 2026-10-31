import math
def rays(cx, cy, r1, r2, n=8, sw=1.8, start=0):
    out=[]
    for i in range(n):
        a=math.radians(start+i*360/n)
        out.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f"/>' % (cx+r1*math.cos(a), cy+r1*math.sin(a), cx+r2*math.cos(a), cy+r2*math.sin(a)))
    return '<g stroke="var(--two,currentColor)" stroke-width="%s" stroke-linecap="round">%s</g>' % (sw, "".join(out))
def halfrays(cx, cy, r1, r2, sw=2):
    out=[]
    for d in (-90,-135,-45,-170,-10):
        a=math.radians(d); out.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f"/>' % (cx+r1*math.cos(a), cy+r1*math.sin(a), cx+r2*math.cos(a), cy+r2*math.sin(a)))
    return '<g stroke="var(--two,currentColor)" stroke-width="%s" stroke-linecap="round">%s</g>' % (sw, "".join(out))

D = '<path d="M13 11.5v25h8a12.5 12.5 0 0 0 0-25z" fill="none" stroke="currentColor" stroke-width="4.5" stroke-linejoin="round"/>'
SYMS = {
"horizon": dict(name="Horizon", tag="Kept from round 1, refined", vb="0 0 48 48",
  svg='<path d="M10 30.5a14 14 0 0 1 28 0z" fill="var(--two,currentColor)"/><rect x="6" y="34.5" width="36" height="4.5" rx="2.25" fill="currentColor"/>',
  idea="Same idea, tighter drawing. The sun is a touch smaller and the line a touch heavier and wider, so the mark sits more firmly at icon size and holds up as a one-colour shape.",
  good=["Calmest and warmest option","The strongest silhouette at 16px","Doesn't depend on any letter or language"],
  watch=["Sunrise marks are common in wellness, so it needs a distinctive wordmark beside it"]),
"dsun": dict(name="D with a sun", tag="Your suggestion", vb="0 0 48 48",
  svg=D + '<circle cx="23.25" cy="24" r="2.8" fill="var(--two,currentColor)"/>' + rays(23.25,24,4.7,6.3,sw=1.6),
  small=D + '<circle cx="22.5" cy="24" r="4.4" fill="var(--two,currentColor)"/>',
  idea="A capital D with a real sun inside it, with eight short rays. The day holds one bright thing. Below 24px the rays merge into a blur, so the small version swaps the sun for a plain dot (shown at 20px and 16px).",
  good=["The most literal reading of “Day”","The rays give a friendly, optimistic tone","Works as a system: the same D can start the wordmark (wordmark C below)"],
  watch=["Needs two drawings, a full one and a small one","The rays add detail the rest of the UI doesn't have"]),
"drise": dict(name="D with a rising sun", tag="Horizon + D combined", vb="0 0 48 48",
  svg=D + '<path d="M18.3 27.5a5.2 5.2 0 0 1 10.4 0z" fill="var(--two,currentColor)"/><rect x="17.5" y="29.3" width="10.5" height="2.4" rx="1.2" fill="currentColor"/>',
  idea="A merge of the two directions you kept. The D frames a small horizon with the sun coming up over it. It reads as a letter from a distance and as a sunrise up close.",
  good=["Joins both favourites into one mark","Still a single solid shape, so it works in one colour","Pairs with Horizon used on its own, for example in illustrations-free headers"],
  watch=["The inner horizon is fine detail: it starts to fill in at 16px"]),
"dw": dict(name="DW", tag="Monogram", vb="0 0 60 48",
  svg='<path d="M6 12v24h5a12 12 0 0 0 0-24z" fill="none" stroke="currentColor" stroke-width="4.5" stroke-linejoin="round"/>'
      '<path d="M30 12v18a6 6 0 0 0 12 0v-8v8a6 6 0 0 0 12 0V12" fill="none" stroke="var(--two,currentColor)" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>',
  idea="Both initials in the same rounded stroke. The W is drawn as two soft U-curves, more like a gentle wave than a sharp zigzag, so the pair stays calm.",
  good=["Spells out Day + well","Rounded strokes match the app's check-in rings","The wide shape suits a website header"],
  watch=["Two letters get small inside a square icon","Monograms feel more corporate than the other options"]),
"dwsun": dict(name="DW with a sun", tag="Monogram + sun", vb="0 0 60 48",
  svg='<path d="M6 12v24h5a12 12 0 0 0 0-24z" fill="none" stroke="currentColor" stroke-width="4.5" stroke-linejoin="round"/>'
      '<path d="M30 20v10a6 6 0 0 0 12 0v-3v3a6 6 0 0 0 12 0V20" fill="none" stroke="currentColor" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>'
      '<circle cx="42" cy="15" r="3.8" fill="var(--two,currentColor)"/>',
  idea="The W is lowered into two soft hills with the sun rising between them: “day” over “well”. It's the most story-like of the five.",
  good=["Tells the name as a tiny scene","The sun carries the accent in one clear spot","The W with its sun could also stand alone as a symbol"],
  watch=["The W no longer reads strongly as a letter","Wide marks lose size inside a square app icon"]),
}

def mark(key, size, color="currentColor", two=None, small=False):
    m=SYMS[key]; vb=m["vb"]; body=m.get("small") if (small and m.get("small")) else m["svg"]
    st='color:%s;%s' % (color, ('--two:%s;' % two) if two else '')
    return '<svg viewBox="%s" width="%s" height="%s" style="%s" aria-hidden="true">%s</svg>' % (vb,size,size,st,body)

def icon(key, bg, fg, two=None, size=96):
    return '<span class="appicon" style="width:%dpx;height:%dpx;background:%s">%s</span>' % (size,size,bg,mark(key,int(size*.64),fg,two))

def lockup(key, h=44):
    return '<span class="lock">%s<span class="lname">Daywell</span></span>' % mark(key,h,"var(--ink)","var(--accent)")

cards=[]
for i,(k,m) in enumerate(SYMS.items(),1):
    sizes="".join('<figure><span class="sz">%s</span><figcaption>%dpx%s</figcaption></figure>' % (mark(k,s,"var(--ink)",small=(s<24)), s, " · small version" if (s<24 and m.get("small")) else "") for s in (48,32,20,16))
    cards.append(f'''
<section class="variant" id="s-{k}">
  <header class="vhead"><span class="vnum">A{i}</span><h2>{m["name"]}</h2><span class="lean">{m["tag"]}</span></header>
  <div class="vgrid">
    <div class="hero">{mark(k,"62%","var(--ink)","var(--accent)")}</div>
    <div class="side">
      <p class="idea">{m["idea"]}</p>
      <div class="lockrow">{lockup(k)}</div>
      <div class="icons">
        <figure>{icon(k,"var(--brand)","#ffffff")}<figcaption>Accent</figcaption></figure>
        <figure>{icon(k,"#161616","#ffffff","#86c2b2")}<figcaption>Ink</figcaption></figure>
        <figure>{icon(k,"#ffffff","#161616","#2f6f62")}<figcaption>Light</figcaption></figure>
      </div>
      <div class="sizes">{sizes}
        <figure><span class="notif"><span class="nt">{mark(k,14,"#ffffff",small=True)}</span><span class="nl">DAYWELL</span></span><figcaption>Notification · one colour</figcaption></figure>
      </div>
      <div class="pc"><div><h3>Works because</h3><ul>{"".join(f"<li>{x}</li>" for x in m["good"])}</ul></div>
      <div><h3>Watch out</h3><ul>{"".join(f"<li>{x}</li>" for x in m["watch"])}</ul></div></div>
    </div>
  </div>
</section>''')

# --- wordmarks (sized by JS after the font loads) ---
def wm(kind, h, color="var(--ink)", two="var(--accent)"):
    if kind == "plain":
        inner='<text class="wt" x="0" y="44" font-family="Figtree,sans-serif" font-weight="600" font-size="52" letter-spacing="-1.2" fill="currentColor">Daywell</text>'
    elif kind == "pills":
        inner=('<text class="wt" x="0" y="44" font-family="Figtree,sans-serif" font-weight="600" font-size="52" letter-spacing="-1" fill="currentColor">daywe</text>'
               '<rect class="p1" x="150" y="6.5" width="9.5" height="37.5" rx="4.75" fill="currentColor"/>'
               '<rect class="p2" x="166" y="8.25" width="9.5" height="34" rx="4.75" fill="none" stroke="var(--two)" stroke-width="3.5"/>')
    else:
        inner=('<path d="M4.5 10.5v31h9a15.5 15.5 0 0 0 0-31z" fill="none" stroke="currentColor" stroke-width="5.4" stroke-linejoin="round"/>'
               '<circle cx="15.5" cy="26" r="4" fill="var(--two)"/>' + rays(15.5,26,6.6,9,sw=2.2).replace('var(--two,currentColor)','var(--two)') +
               '<text class="wt" x="33.5" y="44" font-family="Figtree,sans-serif" font-weight="600" font-size="52" letter-spacing="-1" fill="currentColor">aywell</text>')
    return '<svg class="wm" data-kind="%s" viewBox="0 0 260 60" height="%d" style="color:%s;--two:%s" role="img" aria-label="Daywell">%s</svg>' % (kind,h,color,two,inner)

WMS = [
 ("plain", "Plain wordmark", "Baseline", "“Daywell” in Figtree Semibold with slightly tightened spacing. Quiet and readable, and it lets whichever symbol you choose do the talking.", "horizon"),
 ("pills", "Pill ll", "From round 1, refined", "Lowercase, with the double l drawn as one filled and one outlined pill: the streak idea hidden in the name. The pills are now matched to the letter weight.", "horizon"),
 ("dsun",  "D-sun wordmark", "Matches A2", "The word starts with the same sun-filled D as the app icon, so the website and the app clearly belong together. Best paired with A2.", "dsun"),
]
wcards=[]
for i,(k,name,tag,idea,pair) in enumerate(WMS,1):
    wcards.append(f'''
<section class="variant" id="w-{k}">
  <header class="vhead"><span class="vnum">B{i}</span><h2>{name}</h2><span class="lean">{tag}</span></header>
  <p class="idea">{idea}</p>
  <div class="wbig">{wm(k,84)}</div>
  <div class="site">
    <div class="sitebar"><span class="sitelogo">{wm(k,30)}</span><nav><span>Features</span><span>How it works</span><span class="cta">Get the app</span></nav></div>
    <div class="sitehero"><span class="sh1">Small routines, kept calmly.</span><span class="sh2">Header at real size: wordmark about 30px tall.</span></div>
    <div class="sitefoot"><span class="sitelogo">{wm(k,22,"#ecece8","#86c2b2")}</span><span class="fav"><span class="favtab">{mark(pair,16,"#161616","#2f6f62",small=True)}<span>Daywell</span></span><span class="favcap">Favicon: {SYMS[pair]["name"]}</span></span></div>
  </div>
</section>''')

strip="".join(f'<a class="chip" href="#s-{k}">{icon(k,"var(--brand)","#ffffff",size=60)}<span><b>A{i}</b> {m["name"]}</span></a>' for i,(k,m) in enumerate(SYMS.items(),1))
home="".join(f'<span class="hs">{icon(k,"#2f6f62","#ffffff",size=60)}<span>Daywell</span></span>' for k in SYMS)

CSS = open("base.css").read()
html=f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Daywell Logo Refinements</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600&family=IBM+Plex+Mono:wght@500&display=swap">
<style>{CSS}</style></head><body><div class="wrap">
<p class="eyebrow">Daywell · logo exploration · round 2</p>
<h1>Refinements</h1>
<p class="lede">You kept Horizon, the D and the wordmark (for the website), and asked to try DW and a D with a real sun. Part A is app-icon symbols. Part B is website wordmarks, shown in a real header and footer. Everything is black first, with the sage accent as the second tone.</p>
<div class="strip">{strip}</div>
<p class="cap">On a home screen, at real size:</p>
<div class="homes">{home}</div>
<h2 class="part">A · App icon symbols</h2>
{"".join(cards)}
<h2 class="part">B · Website wordmarks</h2>
{"".join(wcards)}
<section class="next"><h2>Pairings that work as a system</h2>
<div class="pairs">
 <div class="pair"><span>{icon("dsun","#2f6f62","#ffffff",size=56)}</span><span>{wm("dsun",30)}</span><p><b>A2 + B3.</b> One D shared by the app and the website. The most joined-up option.</p></div>
 <div class="pair"><span>{icon("horizon","#2f6f62","#ffffff",size=56)}</span><span>{wm("pills",30)}</span><p><b>A1 + B2.</b> The calmest pairing. The symbol and the wordmark each carry their own small idea.</p></div>
 <div class="pair"><span>{icon("drise","#2f6f62","#ffffff",size=56)}</span><span>{wm("plain",30)}</span><p><b>A3 + B1.</b> A rich icon with a quiet wordmark, so the two never compete.</p></div>
</div>
<p class="cap" style="margin-top:16px">Next round: pick one pairing, then I'll do final drawing (optical corrections, a small-size version, clear-space rules) and add the logos to the design system.</p>
</section>
</div>
<script>
function fitWordmarks(){{
  document.querySelectorAll('svg.wm').forEach(svg => {{
    const t = svg.querySelector('.wt'); let w = 0;
    try {{ w = t.getComputedTextLength(); }} catch (e) {{ return; }}
    const x0 = parseFloat(t.getAttribute('x')) || 0; let end = x0 + w;
    if (svg.dataset.kind === 'pills') {{
      const x1 = end + 4; svg.querySelector('.p1').setAttribute('x', x1);
      svg.querySelector('.p2').setAttribute('x', x1 + 9.5 + 5.5); end = x1 + 9.5 + 5.5 + 9.5;
    }}
    svg.setAttribute('viewBox', '0 0 ' + Math.ceil(end + 3) + ' 60');
  }});
}}
fitWordmarks();
if (document.fonts && document.fonts.ready) document.fonts.ready.then(fitWordmarks);
</script></body></html>'''
open("round2.html","w").write(html)
print(len(html))
