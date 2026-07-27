"""Modern-minimalist monochrome theme: CSS + HTML component builders.

Design language: a single editorial grayscale system (Space Grotesk / Inter /
JetBrains Mono) where drama comes from typography, layout and motion rather
than colour. The page splits into two clearly separated zones -- a self-
contained "digital contact card" up top, then the numbered resume below.
"""

from html import escape


def _e(value):
    return escape(str(value))


def _join(parts):
    # Elements are emitted one-per-string with no indentation so Streamlit's
    # markdown never mistakes leading whitespace for a code block.
    return "".join(parts)


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

/* ---------- contact card ---------- */
.vcard{
  position:relative; overflow:hidden;
  background:linear-gradient(155deg,#242c33 0%,#1a1f24 52%,#171b20 100%);
  border:1px solid #333c44; border-radius:22px;
  padding:2.1rem 2.2rem 1.8rem;
  box-shadow:0 34px 70px -34px rgba(0,0,0,.85);
  animation:fadeUp .7s ease both;
}
.vcard::before{
  content:""; position:absolute; top:0; left:0; right:0; height:1px;
  background:linear-gradient(90deg,transparent,rgba(211,211,211,.55),transparent);
}
.vcard-main{display:grid; grid-template-columns:1fr auto; gap:2rem; align-items:start;}
.eyebrow{
  font-family:var(--font-mono); font-size:.7rem; letter-spacing:.28em;
  color:var(--dim); text-transform:uppercase;
  display:flex; align-items:center; gap:.65em; margin-bottom:1.05rem;
}
.pulse{
  width:7px; height:7px; border-radius:50%; background:#cfd6dc;
  box-shadow:0 0 0 0 rgba(207,214,220,.55); animation:pulse 2.4s infinite;
}
.hero-name{
  font-family:var(--font-display); font-weight:700;
  font-size:clamp(2.5rem,7vw,4.1rem); line-height:.98; letter-spacing:-.02em; margin:0;
  background:linear-gradient(135deg,#ffffff 0%,#cfd6dc 46%,#7f8c98 100%);
  -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent;
}
.hero-role{
  font-family:var(--font-display); font-weight:500;
  font-size:clamp(1.02rem,2.5vw,1.4rem); color:var(--slate-lt); margin:.65rem 0 0;
}
.hero-summary{max-width:560px; color:var(--dim); font-size:.98rem; line-height:1.7; margin:1.2rem 0 0;}
.contact-rows{display:flex; flex-direction:column; gap:.5rem; margin:1.5rem 0 1.2rem;}
.crow{display:flex; align-items:center; gap:.7rem; color:var(--dim); font-size:.86rem; font-family:var(--font-mono);}
a.crow:hover{color:#fff;}
.crow-ic{
  width:27px; height:27px; flex-shrink:0; display:grid; place-items:center;
  border:1px solid var(--border); border-radius:8px; color:var(--slate-lt); font-size:.8rem;
}
.socials{display:flex; flex-wrap:wrap; gap:.5rem;}
.social{
  display:inline-flex; align-items:center; gap:.45em;
  font-family:var(--font-mono); font-size:.75rem; color:var(--dim);
  background:var(--surface-2); border:1px solid var(--border); border-radius:9px;
  padding:.45em .72em; transition:transform .2s ease,color .2s ease,border-color .2s ease,background .2s ease;
}
.social:hover{color:#fff; border-color:var(--slate-lt); background:#2c343b; transform:translateY(-2px);}
.vcard-qr{display:flex; flex-direction:column; align-items:center; gap:.7rem;}
.qr-tile{background:#fff; border-radius:14px; padding:11px; box-shadow:0 12px 30px -14px rgba(0,0,0,.75);}
.qr-tile img{display:block; width:126px; height:126px; image-rendering:pixelated;}
.qr-cap{font-family:var(--font-mono); font-size:.62rem; letter-spacing:.22em; color:var(--faint); text-align:center; line-height:1.6;}
.vcard-actions{display:flex; flex-wrap:wrap; gap:.7rem; margin-top:1.7rem; padding-top:1.5rem; border-top:1px solid var(--border);}
.btn{
  display:inline-flex; align-items:center; gap:.5em;
  font-family:var(--font-mono); font-size:.78rem; font-weight:500; letter-spacing:.02em;
  color:var(--text); background:var(--surface-2); border:1px solid var(--border);
  border-radius:11px; padding:.72em 1.05em; cursor:pointer;
  transition:transform .2s ease,color .2s ease,border-color .2s ease,background .2s ease,box-shadow .2s ease;
}
.btn:hover{color:#fff; border-color:var(--slate-lt); background:#2c343b; transform:translateY(-2px); box-shadow:0 12px 28px -16px rgba(0,0,0,.9);}
.btn-primary{background:linear-gradient(180deg,#f3f6f8,#dde3e8); color:#15181c; border-color:#f3f6f8; font-weight:600;}
.btn-primary:hover{background:#fff; color:#000;}

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
.chip{font-family:var(--font-mono); font-size:.75rem; color:var(--dim); background:var(--surface-2); border:1px solid var(--border); border-radius:8px; padding:.42em .7em; transition:color .2s ease,border-color .2s ease,background .2s ease;}
.chip:hover{color:#fff; border-color:var(--slate-lt); background:#2c343b;}

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

/* links inside custom HTML must follow the monochrome system, not Streamlit's
   default blue markdown link colour */
[data-testid="stMarkdownContainer"] .social,
[data-testid="stMarkdownContainer"] .btn,
[data-testid="stMarkdownContainer"] .crow,
[data-testid="stMarkdownContainer"] .proj,
[data-testid="stMarkdownContainer"] .proj-name{text-decoration:none!important;}
.social{color:var(--dim)!important;}
.social:hover{color:#fff!important;}
.crow{color:var(--dim)!important;}
a.crow:hover{color:#fff!important;}
.btn{color:var(--text)!important;}
.btn-primary{color:#15181c!important;}
.proj-name{color:var(--text)!important;}
.proj:hover .proj-name{color:#fff!important;}
.proj-arrow{color:var(--slate-lt)!important;}

@media(max-width:680px){
  .vcard-main{grid-template-columns:1fr;}
  .vcard-qr{flex-direction:row; align-items:center; justify-self:start;}
  .proj-grid{grid-template-columns:1fr;}
}

@keyframes fadeUp{from{opacity:0; transform:translateY(14px);}to{opacity:1; transform:none;}}
@keyframes pulse{0%{box-shadow:0 0 0 0 rgba(207,214,220,.5);}70%{box-shadow:0 0 0 9px rgba(207,214,220,0);}100%{box-shadow:0 0 0 0 rgba(207,214,220,0);}}
</style>
"""


def contact_card_html(p, qr_datauri, resume_url, card_url, vcf_url):
    d = p["personal_data"]
    socials = _join(
        f'<a class="social" href="{escape(info["link"], quote=True)}" target="_blank" rel="noopener">'
        f'{_e(info["icon"])} {_e(name)}</a>'
        for name, info in p["contact"].items()
    )
    return _join([
        '<div class="vcard">',
        '<div class="vcard-main">',
        '<div class="vcard-id">',
        '<div class="eyebrow"><span class="pulse"></span>DIGITAL CONTACT CARD</div>',
        f'<h1 class="hero-name">{_e(p["name"])}</h1>',
        f'<div class="hero-role">{_e(p["title"])}</div>',
        f'<p class="hero-summary">{_e(p["summary"])}</p>',
        '<div class="contact-rows">',
        f'<a class="crow" href="mailto:{_e(d["email"])}"><span class="crow-ic">@</span><span>{_e(d["email"])}</span></a>',
        f'<div class="crow"><span class="crow-ic">#</span><span>{_e(d["phone_number"])}</span></div>',
        f'<div class="crow"><span class="crow-ic">&#9678;</span><span>{_e(d["current_location"])}</span></div>',
        '</div>',
        f'<div class="socials">{socials}</div>',
        '</div>',
        '<div class="vcard-qr">',
        f'<div class="qr-tile"><img src="{qr_datauri}" alt="Scan to save contact"></div>',
        '<div class="qr-cap">SCAN&nbsp;TO&nbsp;SAVE<br>CONTACT</div>',
        '</div>',
        '</div>',
        '<div class="vcard-actions">',
        f'<a class="btn btn-primary" href="{escape(resume_url, quote=True)}">Download R&eacute;sum&eacute; <span>&#8595;</span></a>',
        f'<a class="btn" href="{escape(card_url, quote=True)}" target="_blank">Print Contact Card</a>',
        f'<a class="btn" href="{escape(vcf_url, quote=True)}">Save Contact (.vcf)</a>',
        '</div>',
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
        chips = _join(f'<span class="chip">{_e(s)}</span>' for s in cat["list"])
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
