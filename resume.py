import streamlit as st
import yaml

from llm import initialize_llm, ask_bot

# Load resume data and initialize chatbot
if "convo" not in st.session_state:
    with open("patrick.yaml") as f:
        st.session_state.patrick = yaml.safe_load(f)
    st.session_state.convo = initialize_llm(st.session_state.patrick)

# Page configuration
PAGE_TITLE = "Resume | " + st.session_state.patrick["name"]
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon="👨💼",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Contact Card Section
with st.container(border=True):
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.title(f"{st.session_state.patrick['name']}")
        st.subheader(st.session_state.patrick['title'])
        st.write(f"📍 {st.session_state.patrick['personal_data']['current_location']}")
        st.write(f"📧 {st.session_state.patrick['personal_data']['email']}")
        st.write(f"📱 {st.session_state.patrick['personal_data']['phone_number']}")
    
    with col2:
        st.markdown("### Quick Contact")
        for platform, info in st.session_state.patrick["contact"].items():
            st.link_button(f'{info["icon"]} {platform}', info["link"], use_container_width=True)
        
        st.link_button("📄 Download Resume", st.session_state.patrick["resume_link"], use_container_width=True, type="primary")

st.divider()

# Resume Content Section
st.header("📋 Professional Resume")
st.write(st.session_state.patrick["summary"])

# Interactive chat section
st.header(f"💬 Chat with {st.session_state.patrick['name']}'s AI Assistant")
st.caption("*Ask me anything about my background, experience, or interests!*")

user_question = st.text_input(
    "Your question:",
    placeholder="Try asking about hobbies, experience, or skills...",
    help="Ask about background, projects, or personal interests"
)

if user_question:
    with st.spinner("Thinking..."):
        response = ask_bot(user_question)
    st.success(f"💡 **Answer:** {response}")

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
        skills = ", ".join(sorted(skill_category["list"]))
        st.write(skills)