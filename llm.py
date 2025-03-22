import streamlit as st
import yaml
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.prompts import PromptTemplate


def initialize_llm(profile):
    template = f"""You are an AI assistant for Patrick in his job search. 
    Please give convincing answers why Patrick is a good candidate and should be hired for this job.
    Keep your answers to 3 or fewer sentences unless absolutely necessary.
    If you don't know the answer, inform the recruiter to contact Patrick. 
    Here's Patrick's information:
    \n\n====\n\n
    {yaml.dump(profile)}
    \n\n====\n\n
    Here is the chat history, use this to understand what to say next: {{memory}}
    Human: {{human}}
    AI:
    """

    llm = ChatOpenAI(model_name="gpt-4o", openai_api_key=st.secrets["OPENAI_API_KEY"])
    memory = ConversationBufferWindowMemory(k=3, memory_key="memory")
    return LLMChain(
        llm=llm, verbose=False, memory=memory,
        prompt=PromptTemplate(input_variables=["memory", "human"], template=template),
    )


def ask_bot(input_text):
    return st.session_state.convo.predict(human=input_text)
