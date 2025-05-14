import os
import json

import streamlit as st
import openai

# configuring openai - api key
working_dir = os.path.dirname(os.path.abspath(__file__))
config_data = json.load(open(f"{working_dir}/config.json"))
OPENAI_API_KEY = config_data["OPENAI_API_KEY"]
openai.api_key = OPENAI_API_KEY

# configuring strealit page settings
st.set_page_config(
    page_title="GPT-4o Chat",
    page_icon="💬",
    layout="centered"
)

# initialize chat session in streamlit if not already present
if "chat_history" not in st.session_state:
    st.session_state.chat_history =[]

# streamlit page title
st.title("🤖GPT-4o ChatBot 🤖")

# diplat chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["eole"]):
        st.markdown(message["content"])



# input field for users message
user_prompt = st.chat_input("Ask GPT-4o your questionnn....")

# add users message to chat and display it
if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role":"user" , "content":user_prompt})

    try:
        # Call OpenAI API
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                *st.session_state.chat_history
            ]
        )

        assistant_response = response.choices[0].message.content
        st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    except openai.RateLimitError:
        assistant_response = "⚠️ Rate limit exceeded. Please check your OpenAI quota or try again later."
        st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    #display GPT-4o's response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)


