import json

import streamlit as st

from llm import initialize_llm, ask_bot

if "convo" not in st.session_state:
    with open("patrick.json") as f:
        st.session_state.patrick = json.load(f)
    st.session_state.convo = initialize_llm(st.session_state.patrick)

PAGE_TITLE = "Resume | " + st.session_state.patrick["name"]
PAGE_ICON = ":wave:"
st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)
st.title(st.session_state.patrick["name"])
col1, col2 = st.columns(2, gap="small")
with col1:
    st.write(st.session_state.patrick["description"])
with col2:
    for idx, (platform, i) in enumerate(st.session_state.patrick["contact"].items()):
        st.link_button(f'{i["icon"]} {platform}', i["link"])
    st.link_button("📄 Download Resume", st.session_state.patrick["resume_link"])

text_input = f'Ask anything about {st.session_state.patrick["name"]}'
text = st.text_input(text_input, placeholder="Try asking about his hobbies", help="also try asking about his birthday")
if text:
    st.info(ask_bot(text))

st.write('\n')
st.subheader("EXPERIENCES")
st.write("---")
for i in st.session_state.patrick["experience"][0:3]:
    st.write("🚧", f'**{i["company"]} ({i["location"]}) | {i["position"]}**')
    st.write(f'{i["year_from"]} - {i["year_to"]}')
    st.write(i["description"])
    for detail in i["description_details"]:
        st.write("* " + detail)
    st.write("---")

st.subheader("EDUCATIONS")
st.write("---")
for i in st.session_state.patrick["education"][0:3]:
    st.write("🎓", f'**{i["institute"]} ({i["location"]}) | {i["degree"]}**')
    st.write(f'{i["year_from"]} - {i["year_to"]}')
    st.write(i["description"])
    for detail in i["description_details"]:
        st.write("* " + detail)
    st.write("---")

st.subheader("PROJECTS")
st.write("---")
for project, link in st.session_state.patrick["project"].items():
    st.write(f"🏆 [{project}]({link})")

st.write("---")
st.subheader("SKILLS")
st.write("---")
for i in st.session_state.patrick["skill"]:
    icon, title, items = i["icon"], i["title"], i["list"]
    items = ", ".join(sorted(items))
    st.write(f"{icon} {title}: {items}")
