from pathlib import Path

import streamlit as st
import yaml

import theme
from llm import initialize_llm, ask_bot
from pdf_generator import generate_resume_pdf, generate_contact_card_pdf
from qr_generator import vcard_content, vcard_qr_datauri

# Load resume data and initialize chatbot
if "convo" not in st.session_state:
    with open("patrick.yaml") as f:
        st.session_state.patrick = yaml.safe_load(f)
    st.session_state.convo = initialize_llm(st.session_state.patrick)

    # Write downloadables to static/ (served at app/static/<name>). Real
    # same-origin URLs download reliably on mobile Firefox, where data:/blob
    # downloads don't. Regenerated per session so they track patrick.yaml.
    p = st.session_state.patrick
    base = p["name"].replace(" ", "_")
    static = Path("static")
    static.mkdir(exist_ok=True)
    (static / f"{base}_Resume.pdf").write_bytes(generate_resume_pdf(p).getvalue())
    (static / f"{base}_Contact_Card.pdf").write_bytes(generate_contact_card_pdf(p).getvalue())
    (static / f"{base}_Contact.vcf").write_text(vcard_content())

    # QR of the vCard, etched into the metal card's QR plate (scan to save).
    st.session_state.qr_datauri = vcard_qr_datauri(fill="#111418", back="#f7f8f9")

p = st.session_state.patrick
base = p["name"].replace(" ", "_")

# Page configuration
st.set_page_config(
    page_title="Resume | " + p["name"],
    page_icon="👨💼",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Global theme (Modern Minimalist, monochrome, editorial)
st.markdown(theme.THEME_CSS, unsafe_allow_html=True)

# ------------------------------------------------------------------ contact card
st.markdown(
    theme.contact_card_html(
        p,
        st.session_state.qr_datauri,
        resume_url=f"app/static/{base}_Resume.pdf",
        card_url=f"app/static/{base}_Contact_Card.pdf",
        vcf_url=f"app/static/{base}_Contact.vcf",
    ),
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------- résumé
st.markdown(theme.resume_divider("FULL RÉSUMÉ"), unsafe_allow_html=True)

# 01 — AI assistant
st.markdown(
    theme.section_header(
        "01", f"Chat with {p['name'].split()[0]}",
        note="Ask about my background, experience, or interests — answered live by Gemini.",
    ),
    unsafe_allow_html=True,
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for role, text in st.session_state.chat_history:
    with st.chat_message(role):
        st.write(text)

if user_question := st.chat_input("Try asking about hobbies, experience, or skills..."):
    with st.chat_message("user"):
        st.write(user_question)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = ask_bot(user_question)
        st.write(response)
    st.session_state.chat_history += [("user", user_question), ("assistant", response)]

# 02 — Experience
st.markdown(theme.section_header("02", "Experience"), unsafe_allow_html=True)
st.markdown(theme.experience_html(p), unsafe_allow_html=True)

# 03 — Education
st.markdown(theme.section_header("03", "Education"), unsafe_allow_html=True)
st.markdown(theme.education_html(p), unsafe_allow_html=True)

# 04 — Projects
st.markdown(theme.section_header("04", "Featured Projects"), unsafe_allow_html=True)
st.markdown(theme.projects_html(p), unsafe_allow_html=True)

# 05 — Skills
st.markdown(theme.section_header("05", "Technical Skills"), unsafe_allow_html=True)
st.markdown(theme.skills_html(p), unsafe_allow_html=True)

# 06 — Recommendations
if p.get("recommendations"):
    st.markdown(theme.section_header("06", "Recommendations"), unsafe_allow_html=True)
    st.markdown(theme.recommendations_html(p), unsafe_allow_html=True)

st.markdown(theme.footer_html(p), unsafe_allow_html=True)
