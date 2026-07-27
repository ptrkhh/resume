"""Theme: CSS + HTML component builders.

The digital contact card is reimagined as a tactile, skeuomorphic metal NFC
business card -- a physical object resting on the dark page (brushed-metal
surface, foil monogram seal, etched EMV chip + contactless glyph, embossed
name, engraved contact lines, raised social studs, a laser-etched QR plate and
pressed-metal action keys). Below it, the resume keeps a flat, monochrome
editorial system (Space Grotesk / Inter / JetBrains Mono).
"""

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
  padding:2rem 2.1rem 1.7rem;
  transform:rotate(-.5deg);
  transition:transform .55s cubic-bezier(.2,.8,.2,1), box-shadow .55s ease;
  animation:fadeUp .7s ease both;
  background:
    repeating-linear-gradient(122deg, rgba(255,255,255,.016) 0 1px, transparent 1px 4px),
    radial-gradient(140% 120% at 8% -10%, rgba(255,255,255,.05), rgba(255,255,255,0) 42%),
    linear-gradient(150deg,#2b2f35 0%,#1e2228 44%,#141619 76%,#20242a 100%);
  border:1px solid #3b4149;
  box-shadow:
    inset 0 1px 0 rgba(255,255,255,.15),
    inset 0 0 0 1px rgba(255,255,255,.018),
    inset 0 -2px 4px rgba(0,0,0,.55),
    0 2px 3px rgba(0,0,0,.4),
    0 44px 74px -34px rgba(0,0,0,.95);
}
.mcard::before{ /* soft top-left light source */
  content:""; position:absolute; inset:0; pointer-events:none; z-index:0;
  background:linear-gradient(158deg, rgba(255,255,255,.09), rgba(255,255,255,0) 24%);
}
.mcard::after{ /* diagonal sheen that sweeps on hover */
  content:""; position:absolute; top:-60%; left:-40%; width:55%; height:220%; z-index:0;
  background:linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,.055), rgba(255,255,255,0));
  transform:rotate(16deg); pointer-events:none; transition:left .85s ease;
}
.mcard:hover{
  transform:rotate(0deg) translateY(-4px);
  box-shadow:
    inset 0 1px 0 rgba(255,255,255,.17), inset 0 -2px 4px rgba(0,0,0,.55),
    0 2px 3px rgba(0,0,0,.4), 0 56px 92px -36px rgba(0,0,0,.98);
}
.mcard:hover::after{left:120%;}
.mcard>*{position:relative; z-index:1;}

.mtop{display:flex; justify-content:space-between; align-items:flex-start;}
.seal{
  width:54px; height:54px; border-radius:50%; display:grid; place-items:center;
  font-family:var(--font-display); font-weight:700; font-size:1.15rem; letter-spacing:.02em;
  background:linear-gradient(145deg,#30353b,#171a1e);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.2), inset 0 -2px 5px rgba(0,0,0,.75), 0 1px 2px rgba(0,0,0,.6);
}
.seal span{
  background:linear-gradient(135deg,#f6f8fa,#aeb6bf 50%,#6f767e);
  -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent;
  filter:drop-shadow(0 1px 0 rgba(0,0,0,.5));
}
.mtech{display:flex; align-items:center; gap:.85rem; padding-top:.3rem;}
.nfc{width:22px; height:22px; fill:none; stroke:#9aa1a8; stroke-width:1.7; stroke-linecap:round; opacity:.85;}
.chip{
  width:40px; height:31px; border-radius:6px; position:relative; flex:none;
  background:linear-gradient(150deg,#eef1f4,#c2c8ce 45%,#8f969d);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.75), inset 0 -1px 2px rgba(0,0,0,.35), 0 1px 2px rgba(0,0,0,.6);
}
.chip::before{content:""; position:absolute; inset:5px; border:1px solid rgba(28,32,37,.42); border-radius:3px;}
.chip::after{
  content:""; position:absolute; left:5px; right:5px; top:50%; height:1px; transform:translateY(-.5px);
  background:rgba(28,32,37,.4); box-shadow:0 -6px 0 rgba(28,32,37,.28), 0 6px 0 rgba(28,32,37,.28);
}

.mname{
  font-family:var(--font-display); font-weight:700; line-height:1; letter-spacing:-.01em;
  font-size:clamp(2.1rem,5.6vw,3.1rem); margin:1.4rem 0 0;
  background:linear-gradient(180deg,#fbfcfd 0%,#c6cdd3 55%,#9aa1a9 100%);
  -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent;
  filter:drop-shadow(0 1px 0 rgba(0,0,0,.55)) drop-shadow(0 -1px 0 rgba(255,255,255,.06));
}
.mrole{
  font-family:var(--font-mono); font-size:.8rem; letter-spacing:.24em; text-transform:uppercase;
  color:#8b929a; margin-top:.6rem; text-shadow:0 1px 0 rgba(255,255,255,.05);
}
.groove{
  height:2px; margin:1.35rem 0; border-radius:2px;
  background:linear-gradient(90deg, transparent, rgba(0,0,0,.6) 12%, rgba(0,0,0,.6) 88%, transparent);
  box-shadow:0 1px 0 rgba(255,255,255,.06);
}
.mbody{display:grid; grid-template-columns:1fr auto; gap:1.7rem; align-items:center;}
.mrow{
  display:flex; align-items:center; gap:.75rem; padding:.3rem 0;
  font-family:var(--font-mono); font-size:.86rem; color:#aab0b7; text-shadow:0 1px 0 rgba(255,255,255,.04);
}
a.mrow:hover{color:#eef1f4;}
.mi{width:16px; height:16px; flex:none; fill:none; stroke:currentColor; stroke-width:1.6; stroke-linecap:round; stroke-linejoin:round; opacity:.8;}
.studs{display:flex; gap:.6rem; margin-top:1rem; flex-wrap:wrap;}
.stud{
  width:39px; height:39px; border-radius:50%; display:grid; place-items:center; font-size:.98rem; text-decoration:none;
  background:linear-gradient(145deg,#2c3036,#191c20);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.15), inset 0 -2px 3px rgba(0,0,0,.6), 0 2px 3px rgba(0,0,0,.5);
  transition:transform .16s ease, box-shadow .16s ease;
}
.stud:hover{transform:translateY(-2px); box-shadow:inset 0 1px 0 rgba(255,255,255,.22), 0 7px 13px -4px rgba(0,0,0,.75);}
.stud:active{transform:translateY(0); box-shadow:inset 0 2px 5px rgba(0,0,0,.7);}
.mqr{display:flex; flex-direction:column; align-items:center; gap:.55rem;}
.qrplate{
  padding:11px; border-radius:12px;
  background:linear-gradient(145deg,#f2f3f5,#d6d9dd);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.85), inset 0 -2px 4px rgba(0,0,0,.18), 0 2px 5px rgba(0,0,0,.55);
}
.qrplate img{display:block; width:116px; height:116px; image-rendering:pixelated;}
.qrcap{font-family:var(--font-mono); font-size:.6rem; letter-spacing:.24em; color:#8b929a; text-align:center;}
.mactions{display:flex; flex-wrap:wrap; gap:.7rem; margin-top:1.5rem;}
.mkey{
  display:inline-flex; align-items:center; gap:.5em; cursor:pointer;
  font-family:var(--font-mono); font-size:.78rem; letter-spacing:.02em; text-decoration:none;
  padding:.75em 1.15em; border-radius:11px; color:#cfd4da;
  background:linear-gradient(145deg,#2c3037,#191c20);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.14), inset 0 -2px 3px rgba(0,0,0,.6), 0 2px 4px rgba(0,0,0,.5);
  transition:transform .14s ease, box-shadow .14s ease, color .14s ease;
}
.mkey:hover{color:#fff; transform:translateY(-1px);}
.mkey:active{transform:translateY(1px); box-shadow:inset 0 2px 5px rgba(0,0,0,.7);}
.mkey--primary{
  color:#1a1d21; font-weight:600;
  background:linear-gradient(145deg,#f5f7f9,#cfd4da 55%,#adb3ba);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.9), inset 0 -2px 3px rgba(0,0,0,.22), 0 3px 6px rgba(0,0,0,.5);
}
.mkey--primary:hover{color:#000;}
.mcaption{max-width:620px; margin:1.5rem auto .2rem; color:var(--dim); font-size:.96rem; line-height:1.7; text-align:center;}

/* ---------- section divider between card and resume ---------- */
.rdiv{display:flex; align-items:center; gap:1.2rem; margin:3.4rem 0 .6rem;}
.rdiv::before,.rdiv::after{content:""; height:1px; flex:1; background:linear-gradient(90deg,transparent,var(--border),transparent);}
.rdiv span{font-family:var(--font-mono); font-size:.68rem; letter-spacing:.34em; color:var(--faint); white-space:nowrap;}

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
[data-testid="stMarkdownContainer"] .proj,
[data-testid="stMarkdownContainer"] .proj-name{text-decoration:none!important;}
.mrow{color:#aab0b7!important;}
a.mrow:hover{color:#eef1f4!important;}
.mkey{color:#cfd4da!important;}
.mkey--primary{color:#1a1d21!important;}
.proj-name{color:var(--text)!important;}
.proj:hover .proj-name{color:#fff!important;}
.proj-arrow{color:var(--slate-lt)!important;}

@media(max-width:680px){
  .mbody{grid-template-columns:1fr;}
  .mqr{justify-self:start; flex-direction:row; align-items:center; gap:1rem;}
  .mcard{padding:1.6rem 1.4rem;}
  .proj-grid{grid-template-columns:1fr;}
}

@keyframes fadeUp{from{opacity:0; transform:translateY(14px);}to{opacity:1; transform:none;}}
</style>
"""


def contact_card_html(p, qr_datauri, resume_url, card_url, vcf_url):
    d = p["personal_data"]
    initials = "".join(w[0] for w in p["name"].split()[:2]).upper()
    studs = _join(
        f'<a class="stud" href="{escape(info["link"], quote=True)}" target="_blank" rel="noopener" '
        f'title="{_e(name)}" aria-label="{_e(name)}">{_e(info["icon"])}</a>'
        for name, info in p["contact"].items()
    )
    return _join([
        '<div class="mstage">',
        '<div class="mcard">',
        '<div class="mtop">',
        f'<div class="seal"><span>{_e(initials)}</span></div>',
        f'<div class="mtech">{_IC_NFC}<div class="chip"></div></div>',
        '</div>',
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
        f'<div class="qrplate"><img src="{qr_datauri}" alt="Scan to save contact"></div>',
        '<div class="qrcap">SCAN&nbsp;TO&nbsp;SAVE</div>',
        '</div>',
        '</div>',
        '<div class="mactions">',
        f'<a class="mkey mkey--primary" href="{escape(resume_url, quote=True)}">Download R&eacute;sum&eacute; <span>&#8595;</span></a>',
        f'<a class="mkey" href="{escape(card_url, quote=True)}" target="_blank">Print Card</a>',
        f'<a class="mkey" href="{escape(vcf_url, quote=True)}">Save .vcf</a>',
        '</div>',
        '</div>',
        f'<p class="mcaption">{_e(p["summary"])}</p>',
        '</div>',
    ])


def resume_divider(label="FULL RÉSUMÉ"):
    return f'<div class="rdiv"><span>{_e(label)}</span></div>'


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
