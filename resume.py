from pathlib import Path

import streamlit as st
import yaml

from llm import initialize_llm, ask_bot
from pdf_generator import generate_resume_pdf, generate_contact_card_pdf
from qr_generator import generate_vcard_qr, vcard_content

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

# Page configuration
PAGE_TITLE = "Resume | " + st.session_state.patrick["name"]
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon="👨💼",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Center content with plain CSS instead of measuring the window via JS
# (streamlit_js_eval returned None on first render and forced a rerun).
st.markdown(
    "<style>.block-container{max-width:900px;margin:auto}</style>",
    unsafe_allow_html=True,
)

with st.container(border=True):
    col1, col2 = st.columns([2, 1])

    with col1:
        st.title(f"{st.session_state.patrick['name']}")
        st.subheader(st.session_state.patrick['title'])
        st.write(f"📍 {st.session_state.patrick['personal_data']['current_location']}")
        st.write(f"📧 {st.session_state.patrick['personal_data']['email']}")
        st.write(f"📱 {st.session_state.patrick['personal_data']['phone_number']}")

    with col2:
        for platform, info in st.session_state.patrick["contact"].items():
            st.link_button(f'{info["icon"]} {platform}', info["link"], use_container_width=True)

        st.link_button(
            "📄 Download Resume",
            f"app/static/{st.session_state.patrick['name'].replace(' ', '_')}_Resume.pdf",
            use_container_width=True,
            type="primary",
        )

# Contact card action buttons
col1, col2, col3 = st.columns(3)
with col1:
    st.link_button(
        "🖨️ Print Contact Card",
        f"app/static/{st.session_state.patrick['name'].replace(' ', '_')}_Contact_Card.pdf",
        use_container_width=True,
    )

with col2:
    if st.button("📱 Scan Contact Card", use_container_width=True):
        qr_image = generate_vcard_qr()
        st.image(qr_image, caption="Scan to save contact info", width=200)

with col3:
    st.link_button(
        "💾 Download Contact",
        f"app/static/{st.session_state.patrick['name'].replace(' ', '_')}_Contact.vcf",
        use_container_width=True,
    )

st.divider()

# Resume Content Section
st.header("📋 Professional Resume")
st.write(st.session_state.patrick["summary"])

# Interactive chat section
st.header(f"💬 Chat with {st.session_state.patrick['name']}'s AI Assistant")
st.caption("*Ask me anything about my background, experience, or interests!*")

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

# Professional Experience Section
st.header("💼 Professional Experience")

for experience in st.session_state.patrick["experience"][:3]:
    with st.container(border=True):
        st.subheader(f"🏢 {experience['company']} - {experience['location']}")
        st.write(f"**{experience['position']}**")
        st.caption(f"{experience['year_from']} - {experience['year_to']}")
        st.write(experience["description"])

        if experience["description_details"]:
            st.write("**Key Achievements:**")
            for detail in experience["description_details"]:
                st.markdown(f"• {detail}")

# Education Section
st.header("🎓 Education")

for education in st.session_state.patrick["education"][:3]:
    with st.container(border=True):
        st.subheader(f"🏫 {education['institute']} - {education['location']}")
        st.write(f"**{education['degree']}**")
        st.caption(f"{education['year_from']} - {education['year_to']}")
        st.write(education["description"])

        if education["description_details"]:
            st.write("**Highlights:**")
            for detail in education["description_details"]:
                st.markdown(f"• {detail}")

# Projects Section
st.header("🚀 Featured Projects")

col1, col2 = st.columns(2)
projects = list(st.session_state.patrick["project"].items())

for idx, (project_name, project_link) in enumerate(projects):
    col = col1 if idx % 2 == 0 else col2
    with col:
        with st.container(border=True):
            st.write(f"🏆 [{project_name}]({project_link})")

# Skills Section
st.header("⚡ Technical Skills")

for skill_category in st.session_state.patrick["skill"]:
    with st.container(border=True):
        st.subheader(f"{skill_category['icon']} {skill_category['title']}")
        skills = ", ".join(skill_category["list"])
        st.write(skills)

# Recommendations Section
if st.session_state.patrick.get("recommendations"):
    st.header("🌟 Recommendations")
    for rec in st.session_state.patrick["recommendations"]:
        with st.container(border=True):
            st.markdown(f"> {rec['text']}")
            who = rec["name"] + (f" · {rec['role']}" if rec.get("role") else "")
            st.caption(f"— {who}")
