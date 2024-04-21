from openai import OpenAI
from langchain_community.document_loaders import DirectoryLoader
import pickle
import streamlit as st
import os

st.markdown('<h1 style="font-size: 60px; text-align: center;">Xficient Bot</h1>', unsafe_allow_html=True)
st.markdown('<h2 style="font-size: 25px; margin-top: -35px; margin-bottom: 5px; text-align: center;"><em>Efficiency at its finest</em></h2>', unsafe_allow_html=True)

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="/Users/lakshay2005/streamlit/static/image.png"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})


