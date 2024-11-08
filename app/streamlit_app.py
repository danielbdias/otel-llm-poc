# Inspired by https://github.com/streamlit/llm-examples/blob/main/Chatbot.py

import config as app_config
config = app_config.get_config()

import streamlit as st
from rag.retrieval import retrieve_context_per_question, answer_question
from rag.vectorstore import load_vector_store

chunks_vector_store = load_vector_store(config)
chunks_query_retriever = chunks_vector_store.as_retriever(search_kwargs={"k": 2})

############################
# UI App start
############################

# Streamlit app
st.title("💬 RAG Prototype")
st.caption("🚀 A Streamlit chatbot powered by OpenAI models to answer questions about an OTel Trace")

if "messages" not in st.session_state.keys():  # Initialize the chat messages history
  st.session_state.messages = [
    { "role": "assistant", "content": "Hello there!" },
    { "role": "assistant", "content": "Here is the latest trace on the system:" },
    { "role": "assistant", "image": "./data/trace_img.png" },
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

    answer = answer_question(config, prompt, context)
    st.write(answer)

    message = {"role": "assistant", "content": answer}
    # Add response to message history
    st.session_state.messages.append(message)
