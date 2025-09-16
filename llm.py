import streamlit as st
import yaml
from openai import OpenAI


def initialize_llm(profile):
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    
    system_prompt = f"""You are Patrick's AI career assistant, helping recruiters and hiring managers learn about his qualifications. Be conversational, enthusiastic, and highlight his strengths naturally.

Key guidelines:
- Answer as if you're Patrick's knowledgeable advocate
- Be concise but compelling (2-3 sentences typically)
- Match specific skills/experience to what's being asked
- Show enthusiasm for opportunities that align with his background
- If asked about something not in his profile, suggest contacting Patrick directly

Patrick's Profile:
{yaml.dump(profile)}

Respond professionally but with personality - you're representing a talented candidate who's excited about new opportunities."""
    
    if 'messages' not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": system_prompt}]
    
    return client


def ask_bot(input_text):
    st.session_state.messages.append({"role": "user", "content": input_text})
    
    response = st.session_state.convo.chat.completions.create(
        model="gpt-4o",
        messages=st.session_state.messages[-7:],  # Keep last 6 messages + system
        max_tokens=150
    )
    
    assistant_message = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": assistant_message})
    
    return assistant_message
