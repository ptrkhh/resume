import streamlit as st
import yaml
from google import genai
from google.genai import types


def initialize_llm(profile):
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

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

    # chats.create keeps conversation history for us; thinking_budget=0 keeps the
    # short-answer bot fast/cheap and stops thinking tokens eating the output budget.
    return client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            max_output_tokens=500,
            thinking_config=types.ThinkingConfig(thinking_budget=0),
        ),
    )


def ask_bot(input_text):
    return st.session_state.convo.send_message(input_text).text
