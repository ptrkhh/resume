import base64
import io
from html import escape

import qrcode
from weasyprint import HTML

RESUME_CSS = """
@page { size: letter; margin: 1.1cm 1.5cm; }
* { margin: 0; padding: 0; }
body { font-family: Helvetica, Arial, sans-serif; font-size: 9pt; color: #222; line-height: 1.3; }
h1 { font-size: 20pt; letter-spacing: 0.5pt; }
.subtitle { font-size: 11pt; color: #1a3c6e; margin-top: 1pt; }
.contact { font-size: 8.5pt; color: #444; margin-top: 4pt; }
.contact a { color: #1a3c6e; text-decoration: none; }
h2 { font-size: 10.5pt; color: #1a3c6e; text-transform: uppercase; letter-spacing: 1pt;
     border-bottom: 1pt solid #1a3c6e; margin: 8pt 0 4pt; padding-bottom: 1pt; }
.role { margin-bottom: 5pt; }
.role-head { display: flex; justify-content: space-between; }
.role-head b { font-size: 10pt; }
.dates { color: #666; font-size: 8.5pt; }
.org { color: #444; font-style: italic; font-size: 9pt; }
ul { margin: 2pt 0 0 12pt; }
li { margin-bottom: 1pt; }
.skill-line { margin-bottom: 2pt; }
"""


def _resume_html(p):
    d = p["personal_data"]
    links = " · ".join(
        f'<a href="{escape(info["link"], quote=True)}">{escape(name)}</a>'
        for name, info in p["contact"].items()
        if name in ("LinkedIn", "GitHub")
    )
    roles = []
    for exp in p["experience"][:4]:
        bullets = "".join(f"<li>{escape(b)}</li>" for b in exp["description_details"][:4])
        roles.append(f"""
        <div class="role">
          <div class="role-head"><b>{escape(exp['position'])}</b>
            <span class="dates">{escape(exp['year_from'])} – {escape(exp['year_to'])}</span></div>
          <div class="org">{escape(exp['company'])} · {escape(exp['location'])}</div>
          <ul>{bullets}</ul>
        </div>""")

    edu = p["education"][0]
    skills = "".join(
        f'<div class="skill-line"><b>{escape(s["title"])}:</b> {escape(", ".join(s["list"]))}</div>'
        for s in p["skill"]
    )
    return f"""<style>{RESUME_CSS}</style>
    <h1>{escape(p['name'])}</h1>
    <div class="subtitle">{escape(p['title'])}</div>
    <div class="contact">{escape(d['email'])} · {escape(d['phone_number'])} ·
      {escape(d['current_location'])} · {links}</div>
    <h2>Summary</h2>
    <div>{escape(p['summary'])}</div>
    <h2>Experience</h2>
    {''.join(roles)}
    <h2>Education</h2>
    <div class="role">
      <div class="role-head"><b>{escape(edu['degree'])}</b>
        <span class="dates">{escape(edu['year_from'])} – {escape(edu['year_to'])}</span></div>
      <div class="org">{escape(edu['institute'])} · {escape(edu['location'])}</div>
    </div>
    <h2>Skills</h2>
    {skills}
    <h2>Languages</h2>
    <div>{escape(' · '.join(p['languages']))}</div>"""


CARD_CSS = """
@page { size: 4in 2.5in; margin: 0.18in; }
* { margin: 0; padding: 0; }
body { font-family: Helvetica, Arial, sans-serif; color: #333; }
h1 { font-size: 15pt; color: #1a3c6e; text-align: center; letter-spacing: 1pt; }
.subtitle { font-size: 9.5pt; color: #4a6fa5; text-align: center; margin-bottom: 6pt; }
table { width: 100%; border-collapse: collapse; }
td.label { font-weight: bold; color: #1a3c6e; font-size: 8pt; padding: 1pt 6pt 1pt 0; white-space: nowrap; }
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


def _to_pdf(html):
    buffer = io.BytesIO()
    HTML(string=html).write_pdf(buffer)
    buffer.seek(0)
    return buffer


def generate_resume_pdf(patrick_data):
    return _to_pdf(_resume_html(patrick_data))


def generate_contact_card_pdf(patrick_data):
    return _to_pdf(_card_html(patrick_data))


if __name__ == "__main__":
    import yaml
    with open("patrick.yaml") as f:
        data = yaml.safe_load(f)
    for name, fn in [("test_resume.pdf", generate_resume_pdf), ("test_card.pdf", generate_contact_card_pdf)]:
        with open(name, "wb") as out:
            out.write(fn(data).getvalue())
    print("wrote test_resume.pdf, test_card.pdf")
