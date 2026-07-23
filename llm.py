import streamlit as st
import yaml
from google import genai
from google.genai import types


def initialize_llm(profile):
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
    # Return just the prompt. We build a fresh genai.Client per request instead
    # of persisting a live chat object: Streamlit reruns the script on every
    # interaction, and a client cached in session_state gets its underlying
    # httpx client closed between reruns ("Cannot send a request, as the client
    # has been closed"). History is already kept in session_state.chat_history.
    return system_prompt


def ask_bot(input_text):
    contents = []
    for role, text in st.session_state.chat_history:
        contents.append(types.Content(
            role="user" if role == "user" else "model",
            parts=[types.Part(text=text)],
        ))
    contents.append(types.Content(role="user", parts=[types.Part(text=input_text)]))

    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=st.session_state.convo,
            max_output_tokens=500,
            thinking_config=types.ThinkingConfig(thinking_budget=0),
        ),
    )
    return response.text
