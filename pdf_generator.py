"""PDF downloadables: the ATS-oriented résumé and the pocket contact card.

The résumé is the important one. It is built to survive two very different
readers:

  * an applicant-tracking system, which throws away every pixel and keeps only
    the extracted text stream — so: single column, no tables, no images, no
    icon glyphs, real text for every URL, and month/year dates in a format
    date regexes actually match;
  * a human recruiter giving it a six-second scan — so: the site's editorial
    type system (Space Grotesk + Inter), a strong hierarchy, and enough
    restraint that the page reads as one thing.

Fonts are bundled and subset under assets/fonts so output is byte-identical
on a laptop and on Streamlit Cloud, which ships a different font set.
"""

import base64
import io
import re
from html import escape
from pathlib import Path

import qrcode
from weasyprint import HTML

ROOT = Path(__file__).parent
FONT_DIR = ROOT / "assets" / "fonts"

# A4 is the standard everywhere except the US/Canada; Patrick is Jakarta-based
# with a German academic history. Flip to "letter" for a US-only search.
PAGE_SIZE = "A4"

MAX_ROLES = 4       # roles shown in full; the rest collapse into "Earlier".
MAX_BULLETS = 4     # bullets per role; each is written to hold a single line.
MIN_EARLIER_MONTHS = 3   # skip sub-quarter stints in the "Earlier" line.
MAX_EARLIER = 4

# Body size in points. The fit loop starts at BASE_PT and steps down toward
# MIN_BASE_PT looking for a single page, so the type is always the largest size
# that fits rather than a number hand-tuned against today's patrick.yaml.
# Below MIN_BASE_PT the page stops being readable and it settles for two
# well-set pages instead of one unreadable one. Inter carries a tall x-height,
# so 8.6pt here reads about as large as 9.5pt Arial.
BASE_PT = 9.4
MIN_BASE_PT = 8.0
FIT_STEP = 0.2
TARGET_PAGES = 1

MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
PRESENT = (9999, 12)


# --------------------------------------------------------------------- dates
def _ym(value):
    """Parse a YAML date ("03 / 2024", "2018", "present") into (year, month)."""
    text = (value or "").strip()
    if text.lower() in {"present", "current", "now", "ongoing"}:
        return PRESENT
    match = re.search(r"(\d{1,2})\s*/\s*(\d{4})", text)
    if match:
        return int(match.group(2)), min(max(int(match.group(1)), 1), 12)
    match = re.search(r"(\d{4})", text)
    return (int(match.group(1)), 1) if match else None


def _date_label(value):
    """"03 / 2024" -> "Mar 2024". ATS date regexes want a month name or MM/YYYY,
    not the spaced slash the YAML uses."""
    parsed = _ym(value)
    if parsed is None:
        return (value or "").strip()
    if parsed == PRESENT:
        return "Present"
    year, month = parsed
    return f"{MONTHS[month - 1]} {year}"


def _year(value):
    parsed = _ym(value)
    if parsed is None:
        return (value or "").strip()
    return "Present" if parsed == PRESENT else str(parsed[0])


def _months(start, end):
    if not start or not end:
        return 0
    return max(0, (end[0] - start[0]) * 12 + (end[1] - start[1]))


def _ranked_experience(experience):
    """Reverse-chronological by end date, then start date. The YAML is
    hand-ordered and drifts; sorting here means the PDF is always in the order
    a recruiter expects."""
    roles = []
    for exp in experience:
        start = _ym(exp.get("year_from")) or (0, 1)
        end = _ym(exp.get("year_to")) or start
        roles.append({**exp, "_start": start, "_end": end})
    roles.sort(key=lambda r: (r["_end"], r["_start"]), reverse=True)
    return roles


# ----------------------------------------------------------------- resources
def _font_face(family, filename, weight, style="normal"):
    return (f"@font-face{{font-family:'{family}';font-weight:{weight};"
            f"font-style:{style};src:url('assets/fonts/{filename}') format('truetype');}}")


FONT_CSS = "".join([
    _font_face("Inter", "Inter-Regular.ttf", 400),
    _font_face("Inter", "Inter-Italic.ttf", 400, "italic"),
    _font_face("Inter", "Inter-Medium.ttf", 500),
    _font_face("Inter", "Inter-SemiBold.ttf", 600),
    _font_face("Inter", "Inter-Bold.ttf", 700),
    _font_face("Space Grotesk", "SpaceGrotesk-Medium.ttf", 500),
    _font_face("Space Grotesk", "SpaceGrotesk-Bold.ttf", 700),
])

# Every size below is in rem, so the whole page scales from one number and the
# fit loop in generate_resume_pdf() can shrink it a hair to hold one page.
# Every grey clears 4.5:1 on white, so the page stays legible after a recruiter
# prints it on a tired office laser.
def _resume_css(base_pt):
    return FONT_CSS + f"""
@page {{
  size: {PAGE_SIZE};
  margin: 12mm 12mm 11mm;
  @bottom-right {{
    content: "Patrick Hermawan · " counter(page) " / " counter(pages);
    font-family: 'Inter', sans-serif; font-size: 7.4pt; color: #6b7681;
  }}
}}
@page :first {{ @bottom-right {{ content: none; }} }}

* {{ margin: 0; padding: 0; }}
html {{ font-size: {base_pt}pt; }}
body {{
  font-family: 'Inter', Helvetica, Arial, sans-serif;
  font-size: 1rem; line-height: 1.33; color: #24292f;
  orphans: 2; widows: 2;
}}
a {{ color: #2f4858; text-decoration: none; }}
.sep {{ color: #9aa4ae; }}

/* ---------------------------------------------------------------- header */
.name {{
  font-family: 'Space Grotesk', Helvetica, sans-serif; font-weight: 700;
  font-size: 2.58rem; line-height: 1.05; letter-spacing: -0.045rem; color: #1b2026;
}}
.headline {{
  font-weight: 500; font-size: 1.06rem; text-transform: uppercase;
  letter-spacing: 0; color: #4a5560; margin-top: 0.4rem;
}}
.contact {{ font-size: 0.955rem; color: #384049; margin-top: 0.56rem; }}
.contact div + div {{ margin-top: 0.11rem; }}

.rule {{ border-bottom: 1.2pt solid #2b333b; margin-top: 0.79rem; }}

/* -------------------------------------------------------------- sections */
h2 {{
  font-family: 'Space Grotesk', Helvetica, sans-serif; font-weight: 700;
  font-size: 0.955rem; text-transform: uppercase; letter-spacing: 0;
  color: #2b333b; margin: 0.9rem 0 0.39rem; padding-bottom: 0.17rem;
  border-bottom: 0.6pt solid #c7ced4;
  break-after: avoid;
}}

/* ------------------------------------------------------------------ roles */
.role {{ margin-top: 0.56rem; break-inside: avoid; }}
.role:first-of-type {{ margin-top: 0.22rem; }}
.role-head {{ display: flex; justify-content: space-between; align-items: baseline; }}
.role-title {{ font-weight: 600; font-size: 1.09rem; color: #1b2026; }}
.dates {{ font-size: 0.944rem; color: #5b6672; white-space: nowrap; padding-left: 0.9rem; }}
.org {{ font-size: 0.978rem; color: #46505a; }}
ul {{ margin: 0.22rem 0 0 1.24rem; }}
li {{ margin-bottom: 0.11rem; padding-left: 0.11rem; }}
li::marker {{ color: #8a949e; }}

.earlier {{ margin-top: 0.56rem; color: #46505a; font-size: 0.955rem; }}
.earlier b {{ color: #2b333b; }}

/* ------------------------------------------------------- projects, skills */
.line {{ margin-bottom: 0.22rem; break-inside: avoid; }}
.line:last-child {{ margin-bottom: 0; }}
.line b {{ font-weight: 600; color: #1b2026; }}
/* Projects sit a touch tighter so each one holds a single line — a URL split
   across a line break is unclickable in some readers and ugly in all of them. */
.proj {{ font-size: 0.944rem; }}
.url {{ color: #2f4858; white-space: nowrap; }}
"""


# ------------------------------------------------------------------ résumé
# Real spaces around the middot: text extraction keeps them, so an ATS reading
# the org line sees "Kata.ai · Jakarta" rather than "Kata.ai·Jakarta".
SEP = ' <span class="sep">·</span> '


def _contact_lines(p):
    d = p["personal_data"]
    contact = p.get("contact", {})

    email = d["email"]
    phone = d["phone_number"]
    primary = SEP.join([
        f'<a href="mailto:{escape(email, quote=True)}">{escape(email)}</a>',
        f'<a href="tel:{escape(re.sub(r"[^+0-9]", "", phone), quote=True)}">{escape(phone)}</a>',
        escape(d["current_location"]),
    ])

    # Anchor text is the URL itself, not the word "LinkedIn". An ATS keeps the
    # text stream and discards the href, so a bare label loses the profile.
    profiles = []
    for key in ("LinkedIn", "GitHub"):
        link = contact.get(key, {}).get("link")
        if not link:
            continue
        shown = link.split("//")[-1].removeprefix("www.").rstrip("/")
        profiles.append(f'<a href="{escape(link, quote=True)}">{escape(shown)}</a>')

    lines = [f'<div>{primary}</div>']
    if profiles:
        lines.append(f'<div>{SEP.join(profiles)}</div>')
    return "".join(lines)


def _roles_html(roles):
    out = []
    for exp in roles:
        bullets = "".join(
            f"<li>{escape(b)}</li>" for b in exp.get("description_details", [])[:MAX_BULLETS]
        )
        out.append(f"""
        <div class="role">
          <div class="role-head">
            <span class="role-title">{escape(exp['position'])}</span>
            <span class="dates">{_date_label(exp['year_from'])} – {_date_label(exp['year_to'])}</span>
          </div>
          <div class="org">{escape(exp['company'])}{SEP}{escape(exp['location'])}</div>
          <ul>{bullets}</ul>
        </div>""")
    return "".join(out)


def _earlier_html(roles):
    """One line covering the roles that did not make the cut, so the years
    before the first listed role do not read as an unexplained gap."""
    kept = [r for r in roles if _months(r["_start"], r["_end"]) >= MIN_EARLIER_MONTHS]
    if not kept:
        return ""
    entries = []
    for exp in kept[:MAX_EARLIER]:
        start, end = _year(exp["year_from"]), _year(exp["year_to"])
        span = start if start == end else f"{start}–{end}"
        entries.append(f"{escape(exp['position'])}, {escape(exp['company'])} ({span})")
    return f'<div class="earlier"><b>Earlier:</b> {SEP.join(entries)}</div>'


def _projects_html(p):
    projects = p.get("project") or {}
    out = []
    for label, url in list(projects.items())[:4]:
        name, _, detail = label.partition(": ")
        shown = url.split("//")[-1].removeprefix("www.").rstrip("/")
        out.append(
            f'<div class="line proj"><b>{escape(name)}</b> — {escape(detail or name)}'
            f'{SEP}<a class="url" href="{escape(url, quote=True)}">{escape(shown)}</a></div>'
        )
    return "".join(out)


def _keywords(p):
    seen, terms = set(), []
    for group in p.get("skill", []):
        for term in [group["title"], *group["list"]]:
            clean = re.sub(r"\s*\([^)]*\)", "", term).strip()
            if clean and clean.lower() not in seen:
                seen.add(clean.lower())
                terms.append(clean)
    return ", ".join(terms)


def _resume_html(p, base_pt=BASE_PT):
    ranked = _ranked_experience(p["experience"])
    shown, rest = ranked[:MAX_ROLES], ranked[MAX_ROLES:]

    edu = p["education"][0]
    skills = "".join(
        f'<div class="line"><b>{escape(s["title"])}:</b> {escape(", ".join(s["list"]))}</div>'
        for s in p["skill"]
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{escape(p['name'])} — {escape(p['title'])} — Résumé</title>
  <meta name="author" content="{escape(p['name'], quote=True)}">
  <meta name="description" content="{escape(p['summary'], quote=True)}">
  <meta name="keywords" content="{escape(_keywords(p), quote=True)}">
  <style>{_resume_css(base_pt)}</style>
</head>
<body>
  <div class="name">{escape(p['name'])}</div>
  <div class="headline">{escape(p['title'])}</div>
  <div class="contact">{_contact_lines(p)}</div>
  <div class="rule"></div>

  <h2>Summary</h2>
  <div class="summary">{escape(p['summary'])}</div>

  <h2>Experience</h2>
  {_roles_html(shown)}
  {_earlier_html(rest)}

  <h2>Technical Skills</h2>
  {skills}

  <h2>Education</h2>
  <div class="role">
    <div class="role-head">
      <span class="role-title">{escape(edu['degree'])}</span>
      <span class="dates">{_date_label(edu['year_from'])} – {_date_label(edu['year_to'])}</span>
    </div>
    <div class="org">{escape(edu['institute'])}{SEP}{escape(edu['location'])}</div>
  </div>

  <h2>Languages</h2>
  <div class="line">{SEP.join(escape(lang) for lang in p['languages'])}</div>
</body>
</html>"""


CARD_CSS = """
@page { size: 4in 2.5in; margin: 0.18in; }
* { margin: 0; padding: 0; }
body { font-family: Helvetica, Arial, sans-serif; color: #333; }
h1 { font-size: 15pt; color: #36454f; text-align: center; letter-spacing: 1pt; }
.subtitle { font-size: 9.5pt; color: #708090; text-align: center; margin-bottom: 6pt; }
table { width: 100%; border-collapse: collapse; }
td.label { font-weight: bold; color: #36454f; font-size: 8pt; padding: 1pt 6pt 1pt 0; white-space: nowrap; }
td.value { font-size: 8pt; }
img.qr { width: 0.85in; height: 0.85in; }
"""


def _card_html(p):
    qr = qrcode.make("https://contactpatrick.streamlit.app")
    buf = io.BytesIO()
    qr.save(buf, format="PNG")
    qr_b64 = base64.b64encode(buf.getvalue()).decode()

    d = p["personal_data"]
    rows = [
        ("Email", d["email"]),
        ("Phone", d["phone_number"]),
        ("Location", d["current_location"]),
    ] + [
        (name, p["contact"][name]["link"].split("//")[-1].removeprefix("www."))
        for name in ("LinkedIn", "GitHub")
        if name in p["contact"]
    ]
    trs = "".join(
        f'<tr><td class="label">{escape(k)}</td><td class="value">{escape(v)}</td></tr>'
        for k, v in rows
    )
    return f"""<style>{CARD_CSS}</style>
    <h1>{escape(p['name'].upper())}</h1>
    <div class="subtitle">{escape(p['title'])}</div>
    <table><tr>
      <td>{f'<table>{trs}</table>'}</td>
      <td style="width:0.9in; text-align:right;"><img class="qr" src="data:image/png;base64,{qr_b64}"></td>
    </tr></table>"""


def _to_pdf(html, **kwargs):
    buffer = io.BytesIO()
    HTML(string=html, base_url=str(ROOT)).write_pdf(buffer, **kwargs)
    buffer.seek(0)
    return buffer


def _write(html):
    # A tagged PDF exposes headings and lists as real structure, which is what
    # the better parsers read before falling back to naive text extraction.
    try:
        return _to_pdf(html, pdf_variant="pdf/ua-1")
    except Exception:
        return _to_pdf(html)


def generate_resume_pdf(patrick_data):
    """Render the résumé, shrinking the type scale a step at a time until it
    holds TARGET_PAGES. Without this, one added bullet in patrick.yaml silently
    pushes a stray section onto a near-empty second page."""
    base = BASE_PT
    while True:
        document = HTML(
            string=_resume_html(patrick_data, base), base_url=str(ROOT)
        ).render()
        if len(document.pages) <= TARGET_PAGES or base <= MIN_BASE_PT:
            break
        base = round(base - FIT_STEP, 2)
    return _write(_resume_html(patrick_data, base))


def generate_contact_card_pdf(patrick_data):
    return _to_pdf(_card_html(patrick_data))


if __name__ == "__main__":
    import yaml
    with open(ROOT / "patrick.yaml") as f:
        data = yaml.safe_load(f)
    for name, fn in [("test_resume.pdf", generate_resume_pdf), ("test_card.pdf", generate_contact_card_pdf)]:
        with open(name, "wb") as out:
            out.write(fn(data).getvalue())
    print("wrote test_resume.pdf, test_card.pdf")
