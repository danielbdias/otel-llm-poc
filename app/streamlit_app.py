# Inspired by https://github.com/streamlit/llm-examples/blob/main/Chatbot.py

import config as app_config
config = app_config.get_config()

import streamlit as st
from rag.retrieval import retrieve_context_per_question, answer_question
from rag.vectorstore import load_vector_store
from create_vector_store import process_trace
# chunks_vector_store = load_vector_store(config)
# chunks_query_retriever = chunks_vector_store.as_retriever(search_kwargs={"k": 2})

############################
# UI App start
############################

# Streamlit app
st.title("💬 RAG Prototype")
st.caption("🚀 A Streamlit chatbot powered by OpenAI models to answer questions about an OTel Trace")

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password", value=config.openai_api_key)
    jaeger_api_url = st.text_input("Jaeger API URL", key="jaeger_api_url", value="http://localhost:8080/jaeger/ui")
    jaeger_ui_url = st.text_input("Jaeger UI URL", key="jaeger_ui_url", value="http://localhost:8080/jaeger/ui/search")
    if jaeger_ui_url != "":
      "[Click here to access Jaeger UI](" + jaeger_ui_url + ")"

    config.openai_api_key = openai_api_key
    config.jaeger_api_url = jaeger_api_url

if "messages" not in st.session_state.keys():  # Initialize the chat messages history
  st.session_state.messages = [
    { "role": "assistant", "content": "Hello there! Tell me what is Trace ID that you want to look for:" },
  ]

# Write message history to UI
for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.write(message["content"])

# Start user interations
if "trace_id" not in st.session_state.keys():
  if prompt := st.chat_input("Enter Trace ID"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.trace_id = prompt
    st.session_state.messages.append({"role": "assistant", "content": "Thank you! Adding Trace to the Vector Store..."})

    elapsed_time = process_trace(st.session_state.trace_id, config)
    st.session_state.messages.append({"role": "assistant", "content": f"Trace added to the Vector Store in {elapsed_time} seconds"})
    st.session_state.messages.append({"role": "assistant", "content": "What do you want to know about this Trace?"})
else:
  if prompt := st.chat_input("Ask me anything about the Trace"):
    st.session_state.messages.append({"role": "user", "content": prompt})

# If last message is not from assistant, generate a new response
# if st.session_state.messages[-1]["role"] != "assistant":
#   with st.chat_message("assistant"):
#     chunks_query_retriever = None
#     context = retrieve_context_per_question(prompt, chunks_query_retriever)
#
#     answer = answer_question(config, prompt, context)
#     st.write(answer)
#
#     message = {"role": "assistant", "content": answer}
#     # Add response to message history
#     st.session_state.messages.append(message)
