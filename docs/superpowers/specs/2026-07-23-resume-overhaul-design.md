# Resume Overhaul — 2026-07-23

Goal: best possible resume site + PDF. Four areas, approved by Patrick.

## 1. Drop streamlit_js_eval
`resume.py` uses `window.innerWidth` to compute column ratios; returns None on
first render (`None > 1200` bug) and forces a rerun. Replace with static CSS
`max-width` on the block container. Remove dependency.

## 2. PDF via HTML+CSS (weasyprint)
Rewrite `pdf_generator.py`: HTML template string + embedded CSS, rendered by
weasyprint. One-page resume: header, contact line with links, summary, recent
roles (max 3 bullets each), education one-liner, compact skills lines. Proper
HTML escaping (fixes "R&D;" artifact). Contact card also HTML for consistency.
Streamlit Cloud needs `packages.txt` with pango libs.

## 3. Copy rewrite (patrick.yaml)
Grounded tone. Two-sentence concrete summary. Keep verifiable metrics ($500K
projects, 3,500 stores, 8-person team); cut decorative round numbers unless
defensible. Skills cut from 48 to ~20 across 3 categories. All experience
entries stay in yaml (chatbot context); PDF/web keep showing recent only.

## 4. UX + hygiene
- Chat: `st.chat_input` + `st.chat_message`, visible history.
- vcard N: field derived from yaml name, not hardcoded.
- Delete `resume.zip`; gitignore `__pycache__/`, `static/*.pdf`, `static/*.vcf`.
- README refreshed (yaml not json, real feature list).
