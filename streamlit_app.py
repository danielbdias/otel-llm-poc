# Inspired by https://github.com/streamlit/llm-examples/blob/main/Chatbot.py

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

import streamlit as st
import os

from retrieval import encode_json, retrieve_context_per_question, answer_question

# chunks_vector_store = encode_json("./trace.json", chunk_size=1000, chunk_overlap=200)
chunks_vector_store = encode_json("./trace-description.txt", chunk_size=1000, chunk_overlap=200)
chunks_query_retriever = chunks_vector_store.as_retriever(search_kwargs={"k": 2})

############################
# UI App start
############################

open_api_key = os.getenv("OPENAI_API_KEY", "")

# Streamlit app
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password", value=open_api_key)
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"

st.title("💬 Prototype")
st.caption("🚀 A Streamlit chatbot powered by OpenAI")

if "messages" not in st.session_state.keys():  # Initialize the chat messages history
  st.session_state.messages = [
    { "role": "assistant", "content": "Hello there!" },
    { "role": "assistant", "content": "Here is the latest trace on the system:" },
    { "role": "assistant", "image": "./trace_img.png" },
    { "role": "assistant", "content": "Do you want to know any specific info about it?" },
  ]

if prompt := st.chat_input(
    "Ask a question"
):  # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:  # Write message history to UI
  with st.chat_message(message["role"]):
    if "image" in message:
      st.image(message["image"])
    else:
      st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
  with st.chat_message("assistant"):
    context = retrieve_context_per_question(prompt, chunks_query_retriever)

    answer = answer_question(openai_api_key, prompt, context)
    st.write(answer)

    message = {"role": "assistant", "content": ', '.join(answer)}
    # Add response to message history
    st.session_state.messages.append(message)
