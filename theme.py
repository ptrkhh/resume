"""Theme: CSS + HTML component builders.

The digital contact card is reimagined as a tactile, skeuomorphic metal NFC
business card -- a physical object resting on the dark page (brushed-metal
surface, foil monogram seal, etched EMV chip + contactless glyph, embossed
name, engraved contact lines, raised social studs, a laser-etched QR plate and
pressed-metal action keys). Below it, the resume keeps a flat, monochrome
editorial system (Space Grotesk / Inter / JetBrains Mono).
"""

import re
from html import escape


def _e(value):
    return escape(str(value))


def _join(parts):
    # Elements are emitted one-per-string with no indentation so Streamlit's
    # markdown never mistakes leading whitespace for a code block.
    return "".join(parts)


# Inline line icons (etched into the metal via currentColor).
_IC_MAIL = '<svg class="mi" viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="M4 7l8 6 8-6"/></svg>'
_IC_PHONE = '<svg class="mi" viewBox="0 0 24 24"><path d="M6.5 3h3l1.5 4.5-2 1.2a12 12 0 0 0 5.3 5.3l1.2-2 4.5 1.5v3a2 2 0 0 1-2.2 2A16.5 16.5 0 0 1 4.5 5.2 2 2 0 0 1 6.5 3z"/></svg>'
_IC_PIN = '<svg class="mi" viewBox="0 0 24 24"><path d="M12 21c4.5-4.2 7-7.3 7-10.5A7 7 0 1 0 5 10.5C5 13.7 7.5 16.8 12 21z"/><circle cx="12" cy="10" r="2.4"/></svg>'
_IC_NFC = '<svg class="nfc" viewBox="0 0 24 24"><path d="M6.5 8.5a7 7 0 0 1 0 7"/><path d="M10 6.5a11 11 0 0 1 0 11"/><path d="M13.5 5a15 15 0 0 1 0 14"/></svg>'

# Real brand marks (single-path, 24x24), rendered monochrome and laser-etched
# into the studs so each platform is unmistakable.
_SOCIAL_ICONS = {
    "linkedin": "M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0 1-2.063-2.065 2.064 2.064 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z",
    "github": "M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.5 11.5 0 0 1 12 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222 0 1.606-.014 2.898-.014 3.293 0 .319.216.694.825.576C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12",
    "whatsapp": "M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.71.306 1.263.489 1.694.625.712.227 1.36.195 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413z",
    "telegram": "M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z",
    "instagram": "M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.012-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 1 0 0 12.324 6.162 6.162 0 0 0 0-12.324zM12 16a4 4 0 1 1 0-8 4 4 0 0 1 0 8zm6.406-11.845a1.44 1.44 0 1 0 0 2.881 1.44 1.44 0 0 0 0-2.881z",
    "email": "M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z",
    "link": "M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z",
}


def _social_icon(name):
    key = re.sub(r"[^a-z]", "", str(name).lower())
    d = _SOCIAL_ICONS.get(key, _SOCIAL_ICONS["link"])
    return f'<svg class="sicon" viewBox="0 0 24 24" aria-hidden="true"><path d="{d}"/></svg>'


THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&family=Space+Grotesk:wght@400;500;600;700&display=swap');

:root{
  --bg:#15181c; --bg-soft:#1a1f24; --surface:#1f252b; --surface-2:#262d34;
  --border:#2f373f; --border-soft:rgba(255,255,255,.06);
  --text:#dfe4e8; --dim:#98a3ac; --faint:#6b757d; --white:#fff;
  --slate:#708090; --slate-lt:#a2b0bc; --silver:#d3d3d3; --accent:#c3ccd4;
  --font-display:'Space Grotesk',ui-sans-serif,system-ui,sans-serif;
  --font-body:'Inter',ui-sans-serif,system-ui,sans-serif;
  --font-mono:'JetBrains Mono',ui-monospace,'SFMono-Regular',monospace;
  --radius:16px;
}

/* ---------- base ---------- */
.stApp{
  background:
    radial-gradient(1100px 620px at 50% -10%, #27313a 0%, rgba(39,49,58,0) 62%),
    var(--bg);
  color:var(--text);
  font-family:var(--font-body);
}
[data-testid="stHeader"]{background:transparent;}
[data-testid="stBottomBlockContainer"],[data-testid="stBottom"]>div{background:transparent!important;}
#MainMenu,footer,[data-testid="stStatusWidget"]{visibility:hidden;height:0;}
.block-container{max-width:900px;padding-top:2.4rem;padding-bottom:3rem;}
html,body,[class*="css"]{font-family:var(--font-body);}
::selection{background:var(--slate);color:#fff;}
a{color:var(--accent);text-decoration:none;}
a:hover{color:var(--white);}
*::-webkit-scrollbar{width:10px;height:10px;}
*::-webkit-scrollbar-thumb{background:#2c343b;border-radius:10px;}
*::-webkit-scrollbar-thumb:hover{background:#39424a;}

/* ---------- skeuomorphic metal contact card ---------- */
.mstage{padding:.4rem 0 .2rem;}
.mcard{
  position:relative; overflow:hidden; border-radius:22px;
  padding:1.8rem 2.1rem 1.7rem;
  transform:rotate(-.5deg);
  transition:transform .55s cubic-bezier(.2,.8,.2,1), box-shadow .55s ease;
  animation:fadeUp .7s ease both;
  background:
    repeating-linear-gradient(122deg, rgba(255,255,255,.45) 0 1px, rgba(84,94,104,.06) 1px 3px),
    radial-gradient(140% 120% at 8% -10%, rgba(255,255,255,.55), rgba(255,255,255,0) 40%),
    linear-gradient(150deg,#dfe3e7 0%,#c7ccd2 42%,#b0b6bd 76%,#cdd2d7 100%);
  border:1px solid #9298a0;
  box-shadow:
    inset 0 1px 0 rgba(255,255,255,.8),
    inset 0 0 0 1px rgba(255,255,255,.25),
    inset 0 -2px 4px rgba(0,0,0,.14),
    0 2px 3px rgba(0,0,0,.35),
    0 44px 74px -34px rgba(0,0,0,.9);
}
.mcard::before{ /* soft top-left light source */
  content:""; position:absolute; inset:0; pointer-events:none; z-index:0;
  background:linear-gradient(158deg, rgba(255,255,255,.5), rgba(255,255,255,0) 26%);
}
.mcard::after{ /* diagonal sheen that sweeps on hover */
  content:""; position:absolute; top:-60%; left:-40%; width:55%; height:220%; z-index:0;
  background:linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,.4), rgba(255,255,255,0));
  transform:rotate(16deg); pointer-events:none; transition:left .85s ease;
}
.mcard:hover{
  transform:rotate(0deg) translateY(-4px);
  box-shadow:
    inset 0 1px 0 rgba(255,255,255,.85), inset 0 -2px 4px rgba(0,0,0,.14),
    0 2px 3px rgba(0,0,0,.35), 0 56px 92px -36px rgba(0,0,0,.92);
}
.mcard:hover::after{left:120%;}
.mcard>*{position:relative; z-index:1;}

.mtech{position:absolute; top:1.6rem; right:2.1rem; z-index:2; display:flex; align-items:center; gap:.8rem;}
.nfc{width:22px; height:22px; fill:none; stroke:#5f666e; stroke-width:1.7; stroke-linecap:round; opacity:.8;}
.chip{
  width:40px; height:31px; border-radius:6px; position:relative; flex:none;
  background:linear-gradient(150deg,#b3b9c0,#868d95 50%,#61686f);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.55), inset 0 -1px 2px rgba(0,0,0,.4), 0 1px 2px rgba(0,0,0,.35);
}
.chip::before{content:""; position:absolute; inset:5px; border:1px solid rgba(18,22,27,.4); border-radius:3px;}
.chip::after{
  content:""; position:absolute; left:5px; right:5px; top:50%; height:1px; transform:translateY(-.5px);
  background:rgba(18,22,27,.4); box-shadow:0 -6px 0 rgba(18,22,27,.3), 0 6px 0 rgba(18,22,27,.3);
}

.mname{
  font-family:var(--font-display); font-weight:700; line-height:1; letter-spacing:-.01em;
  font-size:clamp(2.1rem,5.6vw,3.1rem); margin:0;
  background:linear-gradient(180deg,#4c535b 0%,#2b3036 58%,#3d434b 100%);
  -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent;
  filter:drop-shadow(0 1px 0 rgba(255,255,255,.6)) drop-shadow(0 -1px 0 rgba(0,0,0,.2));
}
.mrole{
  font-family:var(--font-mono); font-size:.8rem; letter-spacing:.24em; text-transform:uppercase;
  color:#5c636b; margin-top:.6rem; text-shadow:0 1px 0 rgba(255,255,255,.55);
}
.groove{
  height:2px; margin:1.35rem 0; border-radius:2px;
  background:linear-gradient(90deg, transparent, rgba(20,26,32,.28) 12%, rgba(20,26,32,.28) 88%, transparent);
  box-shadow:0 1px 0 rgba(255,255,255,.65);
}
.mbody{display:grid; grid-template-columns:1fr auto; gap:1.7rem; align-items:center;}
.mrow{
  display:flex; align-items:center; gap:.75rem; padding:.3rem 0;
  font-family:var(--font-mono); font-size:.86rem; color:#4b525a; text-shadow:0 1px 0 rgba(255,255,255,.5);
}
a.mrow:hover{color:#23282d;}
.mi{width:16px; height:16px; flex:none; fill:none; stroke:currentColor; stroke-width:1.6; stroke-linecap:round; stroke-linejoin:round; opacity:.75;}
.studs{display:flex; gap:.5rem; margin-top:1rem; flex-wrap:wrap;}
.stud{ /* recessed dimple in the titanium with a dark etched brand mark */
  width:34px; height:34px; border-radius:50%; display:grid; place-items:center; text-decoration:none;
  background:radial-gradient(120% 120% at 50% 78%, #d0d4d9, #a9afb6);
  box-shadow:inset 0 2px 4px rgba(0,0,0,.3), inset 0 -1px 0 rgba(255,255,255,.7), 0 1px 0 rgba(255,255,255,.55);
  transition:box-shadow .16s ease;
}
.stud:hover{box-shadow:inset 0 2px 5px rgba(0,0,0,.36), inset 0 -1px 0 rgba(255,255,255,.8), 0 0 0 1px rgba(0,0,0,.06);}
.sicon{width:16px; height:16px; fill:#474e56; filter:drop-shadow(0 1px 0 rgba(255,255,255,.55)); transition:fill .16s ease;}
.stud:hover .sicon{fill:#1d2226;}
.mqr{display:flex; flex-direction:column; align-items:center; gap:.7rem;}
.qrlink{display:inline-block; text-decoration:none; transition:transform .18s ease;}
.qrlink:hover{transform:translateY(-2px);}
.qrimg{display:block; width:190px; height:190px; image-rendering:pixelated;}
.qrcap{font-family:var(--font-mono); font-size:.6rem; letter-spacing:.24em; color:#5c636b; text-align:center;}
.mactions{display:flex; flex-wrap:wrap; gap:.7rem; margin-top:1.5rem;}
.mkey{
  display:inline-flex; align-items:center; gap:.5em; cursor:pointer;
  font-family:var(--font-mono); font-size:.78rem; letter-spacing:.02em; text-decoration:none;
  padding:.75em 1.15em; border-radius:11px; color:#2b3138;
  background:linear-gradient(180deg,#d3d7dc,#b4bac0);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.7), inset 0 -2px 3px rgba(0,0,0,.16), 0 1px 2px rgba(0,0,0,.28);
  transition:transform .14s ease, box-shadow .14s ease, color .14s ease;
}
.mkey:hover{color:#0e1113; transform:translateY(-1px);}
.mkey:active{transform:translateY(1px); box-shadow:inset 0 2px 5px rgba(0,0,0,.28);}
.mkey--primary{
  color:#eef1f4; font-weight:600;
  background:linear-gradient(150deg,#3c434b,#22272c);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.14), inset 0 -2px 3px rgba(0,0,0,.5), 0 3px 6px rgba(0,0,0,.4);
}
.mkey--primary:hover{color:#fff;}
.mcaption{width:min(640px,100%); margin:2.7rem auto 0; color:var(--dim); font-size:.96rem; line-height:1.75; text-align:center;}

/* ---------- section divider between card and resume ---------- */
.rdiv{display:flex; align-items:center; gap:1.2rem; margin:3.4rem 0 .6rem;}
.rdiv::before,.rdiv::after{content:""; height:1px; flex:1; background:linear-gradient(90deg,transparent,var(--border),transparent);}
.rdiv span{font-family:var(--font-mono); font-size:.68rem; letter-spacing:.34em; color:var(--faint); white-space:nowrap;}
.rline{height:1px; margin:3.4rem 0 .6rem; background:linear-gradient(90deg,transparent,var(--border) 18%,var(--border) 82%,transparent);}

/* ---------- resume section headers ---------- */
.sec{display:flex; align-items:center; gap:1rem; margin:3rem 0 1.5rem;}
.sec-num{font-family:var(--font-mono); font-size:.82rem; color:var(--slate-lt); font-weight:500;}
.sec-title{font-family:var(--font-display); font-weight:600; font-size:clamp(1.3rem,3.6vw,1.9rem); letter-spacing:-.01em; color:#fff; margin:0; white-space:nowrap;}
.sec-line{flex:1; height:1px; background:linear-gradient(90deg,var(--border),transparent);}
.sec-note{color:var(--dim); font-size:.9rem; margin:-.6rem 0 1.4rem;}

/* ---------- cards ---------- */
.card{
  position:relative; overflow:hidden;
  background:linear-gradient(180deg,var(--surface) 0%,var(--bg-soft) 100%);
  border:1px solid var(--border); border-radius:var(--radius);
  padding:1.4rem 1.55rem; margin-bottom:1rem;
  transition:transform .25s ease,border-color .25s ease,box-shadow .25s ease;
}
.card::before{
  content:""; position:absolute; left:0; top:0; bottom:0; width:3px;
  background:linear-gradient(180deg,var(--silver),var(--slate));
  transform:scaleY(0); transform-origin:top; transition:transform .3s ease;
}
.card:hover{transform:translateY(-3px); border-color:#48535d; box-shadow:0 16px 42px -20px rgba(0,0,0,.75);}
.card:hover::before{transform:scaleY(1);}
.card.current{border-color:#4a5761;}
.card.current::before{transform:scaleY(1);}
.card-head{display:flex; justify-content:space-between; align-items:baseline; gap:1rem; flex-wrap:wrap;}
.card-title{font-family:var(--font-display); font-weight:600; font-size:1.08rem; color:#fff;}
.card-org{color:var(--slate-lt); font-weight:500;}
.card-meta{font-family:var(--font-mono); font-size:.74rem; color:var(--faint); white-space:nowrap;}
.card-sub{color:var(--dim); font-size:.83rem; margin-top:.2rem;}
.card-desc{color:var(--text); font-size:.94rem; line-height:1.65; margin:.85rem 0 .2rem;}
.badge{font-family:var(--font-mono); font-size:.6rem; letter-spacing:.16em; color:#cfd6dc; border:1px solid rgba(207,214,220,.3); border-radius:20px; padding:.18em .6em; margin-left:.55rem; vertical-align:middle;}
.bullets{list-style:none; margin:.65rem 0 0; padding:0;}
.bullets li{position:relative; padding-left:1.15rem; color:var(--dim); font-size:.89rem; line-height:1.6; margin-bottom:.32rem;}
.bullets li::before{content:""; position:absolute; left:0; top:.62em; width:7px; height:1px; background:var(--slate-lt);}

/* ---------- projects ---------- */
.proj-grid{display:grid; grid-template-columns:1fr 1fr; gap:1rem;}
.proj{
  display:flex; justify-content:space-between; align-items:flex-start; gap:1rem;
  background:linear-gradient(180deg,var(--surface),var(--bg-soft));
  border:1px solid var(--border); border-radius:var(--radius); padding:1.3rem;
  transition:transform .25s ease,border-color .25s ease,box-shadow .25s ease;
}
.proj:hover{transform:translateY(-3px); border-color:#48535d; box-shadow:0 16px 42px -20px rgba(0,0,0,.75);}
.proj-name{font-family:var(--font-body); font-weight:500; color:var(--text); font-size:.93rem; line-height:1.5;}
.proj:hover .proj-name{color:#fff;}
.proj-arrow{font-family:var(--font-mono); color:var(--slate-lt); flex-shrink:0; transition:transform .25s ease,color .25s ease;}
.proj:hover .proj-arrow{transform:translate(3px,-3px); color:#fff;}

/* ---------- skills ---------- */
.skill-head{display:flex; align-items:center; gap:.6rem; margin-bottom:1rem;}
.skill-ic{font-size:1.05rem;}
.skill-title{font-family:var(--font-display); font-weight:600; color:#fff; font-size:1.02rem;}
.chips{display:flex; flex-wrap:wrap; gap:.5rem;}
.chip-tag{font-family:var(--font-mono); font-size:.75rem; color:var(--dim); background:var(--surface-2); border:1px solid var(--border); border-radius:8px; padding:.42em .7em; transition:color .2s ease,border-color .2s ease,background .2s ease;}
.chip-tag:hover{color:#fff; border-color:var(--slate-lt); background:#2c343b;}

/* ---------- recommendations ---------- */
.rec .qm{font-family:var(--font-display); font-size:2.4rem; color:#3a434b; line-height:.5; display:block; margin-bottom:.5rem;}
.rec-text{color:var(--dim); font-size:.9rem; line-height:1.7; font-style:italic; margin:0 0 1rem;}
.rec-author{font-family:var(--font-display); font-weight:600; color:#fff; font-size:.88rem;}
.rec-role{color:var(--faint); font-weight:400; font-family:var(--font-body);}

/* ---------- footer ---------- */
.foot{margin-top:3.5rem; padding-top:1.6rem; border-top:1px solid var(--border); display:flex; justify-content:space-between; flex-wrap:wrap; gap:.6rem; font-family:var(--font-mono); font-size:.68rem; letter-spacing:.12em; color:var(--faint);}

/* ---------- streamlit widgets ---------- */
.stButton>button,.stLinkButton>a,.stDownloadButton>button,[data-testid^="stBaseButton"]{
  font-family:var(--font-mono)!important; font-size:.78rem!important; letter-spacing:.02em!important;
  background:var(--surface-2)!important; color:var(--text)!important; border:1px solid var(--border)!important;
  border-radius:11px!important; padding:.6rem .95rem!important; font-weight:500!important;
  transition:transform .2s ease,color .2s ease,border-color .2s ease,background .2s ease!important;
}
.stButton>button:hover,.stLinkButton>a:hover,.stDownloadButton>button:hover{
  border-color:var(--slate-lt)!important; background:#2c343b!important; color:#fff!important; transform:translateY(-2px);
}
[data-testid^="stBaseButton"] p{color:inherit!important; margin:0!important;}
[data-testid="stBaseButton-primary"]{background:linear-gradient(180deg,#f3f6f8,#dde3e8)!important; color:#15181c!important; border-color:#f3f6f8!important; font-weight:600!important;}

[data-testid="stChatMessage"]{background:var(--surface)!important; border:1px solid var(--border); border-radius:var(--radius); padding:1rem 1.1rem;}
[data-testid="stChatMessage"] p{color:var(--text);}
[data-testid="stChatMessage"] a{color:var(--accent);}
[data-testid="stChatInput"]{background:var(--surface)!important; border:1px solid var(--border)!important; border-radius:13px!important;}
[data-testid="stChatInput"] textarea{color:var(--text)!important;}
[data-testid="stChatInput"] textarea::placeholder{color:var(--faint)!important;}

/* links inside custom HTML must follow the theme, not Streamlit's blue */
[data-testid="stMarkdownContainer"] .mrow,
[data-testid="stMarkdownContainer"] .stud,
[data-testid="stMarkdownContainer"] .mkey,
[data-testid="stMarkdownContainer"] .qrlink,
[data-testid="stMarkdownContainer"] .proj,
[data-testid="stMarkdownContainer"] .proj-name{text-decoration:none!important;}
.mrow{color:#4b525a!important;}
a.mrow:hover{color:#23282d!important;}
.mkey{color:#2b3138!important;}
.mkey--primary{color:#eef1f4!important;}
.proj-name{color:var(--text)!important;}
.proj:hover .proj-name{color:#fff!important;}
.proj-arrow{color:var(--slate-lt)!important;}
/* Streamlit styles markdown block elements; force our centering to win */
[data-testid="stMarkdownContainer"] .mcaption{margin:2.7rem auto 0!important;}

@media(max-width:680px){
  .mbody{grid-template-columns:1fr;}
  .mcard{padding:1.5rem 1.4rem;}
  .mtech{top:1.35rem; right:1.4rem;}
  .mactions{flex-direction:column;}
  .mkey{width:100%; justify-content:center;}
  .proj-grid{grid-template-columns:1fr;}
}

@keyframes fadeUp{from{opacity:0; transform:translateY(14px);}to{opacity:1; transform:none;}}
</style>
"""


def contact_card_html(p, qr_datauri, resume_url, card_url, vcf_url):
    d = p["personal_data"]
    studs = _join(
        f'<a class="stud" href="{escape(info["link"], quote=True)}" target="_blank" rel="noopener" '
        f'title="{_e(name)}" aria-label="{_e(name)}">{_social_icon(name)}</a>'
        for name, info in p["contact"].items()
    )
    return _join([
        '<div class="mstage">',
        '<div class="mcard">',
        f'<div class="mtech">{_IC_NFC}<div class="chip"></div></div>',
        f'<div class="mname">{_e(p["name"])}</div>',
        f'<div class="mrole">{_e(p["title"])}</div>',
        '<div class="groove"></div>',
        '<div class="mbody">',
        '<div class="mdetails">',
        f'<a class="mrow" href="mailto:{_e(d["email"])}">{_IC_MAIL}<span>{_e(d["email"])}</span></a>',
        f'<div class="mrow">{_IC_PHONE}<span>{_e(d["phone_number"])}</span></div>',
        f'<div class="mrow">{_IC_PIN}<span>{_e(d["current_location"])}</span></div>',
        f'<div class="studs">{studs}</div>',
        '</div>',
        '<div class="mqr">',
        f'<a class="qrlink" href="{escape(vcf_url, quote=True)}" title="Tap to save contact">'
        f'<img class="qrimg" src="{qr_datauri}" alt="Save contact"></a>',
        '<div class="qrcap">TAP&nbsp;OR&nbsp;SCAN<br>TO&nbsp;SAVE</div>',
        '</div>',
        '</div>',
        '<div class="mactions">',
        f'<a class="mkey mkey--primary" href="{escape(resume_url, quote=True)}">Download R&eacute;sum&eacute; <span>&#8595;</span></a>',
        f'<a class="mkey" href="{escape(card_url, quote=True)}" target="_blank">Print Card</a>',
        '</div>',
        '</div>',
        f'<div class="mcaption">{_e(p["summary"])}</div>',
        '</div>',
    ])


def resume_divider(label=None):
    if label:
        return f'<div class="rdiv"><span>{_e(label)}</span></div>'
    return '<div class="rline"></div>'


def section_header(num, title, note=None):
    html = (
        '<div class="sec">'
        f'<span class="sec-num">{_e(num)}</span>'
        f'<h2 class="sec-title">{_e(title)}</h2>'
        '<span class="sec-line"></span>'
        '</div>'
    )
    if note:
        html += f'<div class="sec-note">{_e(note)}</div>'
    return html


def experience_html(p):
    cards = []
    for exp in p["experience"][:4]:
        is_current = str(exp.get("year_to", "")).strip().lower() == "present"
        badge = '<span class="badge">NOW</span>' if is_current else ""
        bullets = _join(f'<li>{_e(b)}</li>' for b in exp["description_details"])
        cards.append(_join([
            f'<div class="card exp{" current" if is_current else ""}">',
            '<div class="card-head">',
            f'<div><span class="card-title">{_e(exp["position"])}</span>'
            f'<span class="card-org"> &middot; {_e(exp["company"])}</span>{badge}</div>',
            f'<span class="card-meta">{_e(exp["year_from"])} &mdash; {_e(exp["year_to"])}</span>',
            '</div>',
            f'<div class="card-sub">{_e(exp["location"])}</div>',
            f'<p class="card-desc">{_e(exp["description"])}</p>',
            f'<ul class="bullets">{bullets}</ul>' if bullets else "",
            '</div>',
        ]))
    return _join(cards)


def education_html(p):
    cards = []
    for edu in p["education"][:3]:
        bullets = _join(f'<li>{_e(b)}</li>' for b in edu.get("description_details", []))
        cards.append(_join([
            '<div class="card">',
            '<div class="card-head">',
            f'<div><span class="card-title">{_e(edu["degree"])}</span></div>',
            f'<span class="card-meta">{_e(edu["year_from"])} &mdash; {_e(edu["year_to"])}</span>',
            '</div>',
            f'<div class="card-sub">{_e(edu["institute"])} &middot; {_e(edu["location"])}</div>',
            f'<p class="card-desc">{_e(edu["description"])}</p>',
            f'<ul class="bullets">{bullets}</ul>' if bullets else "",
            '</div>',
        ]))
    return _join(cards)


def projects_html(p):
    items = _join(
        f'<a class="proj" href="{escape(link, quote=True)}" target="_blank" rel="noopener">'
        f'<span class="proj-name">{_e(name)}</span>'
        f'<span class="proj-arrow">&#8599;</span></a>'
        for name, link in p["project"].items()
    )
    return f'<div class="proj-grid">{items}</div>'


def skills_html(p):
    cards = []
    for cat in p["skill"]:
        chips = _join(f'<span class="chip-tag">{_e(s)}</span>' for s in cat["list"])
        cards.append(_join([
            '<div class="card">',
            f'<div class="skill-head"><span class="skill-ic">{_e(cat["icon"])}</span>'
            f'<span class="skill-title">{_e(cat["title"])}</span></div>',
            f'<div class="chips">{chips}</div>',
            '</div>',
        ]))
    return _join(cards)


def recommendations_html(p, limit=4):
    cards = []
    for rec in p.get("recommendations", [])[:limit]:
        role = f'<span class="rec-role"> &middot; {_e(rec["role"])}</span>' if rec.get("role") else ""
        cards.append(_join([
            '<div class="card rec">',
            '<span class="qm">&#8220;</span>',
            f'<p class="rec-text">{_e(rec["text"])}</p>',
            f'<div class="rec-author">{_e(rec["name"])}{role}</div>',
            '</div>',
        ]))
    return _join(cards)


def footer_html(p):
    return _join([
        '<div class="foot">',
        f'<span>&copy; {_e(p["name"].upper())}</span>',
        '<span>DESIGNED &amp; BUILT WITH STREAMLIT</span>',
        '</div>',
    ])
