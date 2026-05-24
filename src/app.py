import sys
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, str(Path(__file__).resolve().parent))

from main import run_assistant
from llms.models import configured_providers, provider_label
from tools.file_tool import agent_output_dir

st.set_page_config(page_title="Multi-LLM Chatbot", layout="wide")
st.title("Multi-LLM Chatbot")

providers = configured_providers()
if not providers:
    st.error("Add OPENAI_API_KEY and/or GEMINI_API_KEY to .env, then restart.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "files" not in st.session_state:
    st.session_state.files = []

with st.sidebar:
    provider = st.selectbox("Model", providers, format_func=provider_label)
    st.caption(f"Files saved in `{agent_output_dir()}`")
    for i, file_path in enumerate(st.session_state.files):
        path = Path(file_path)
        if path.is_file():
            st.download_button(
                f"Download {path.name}",
                path.read_bytes(),
                path.name,
                key=f"file_{i}",
            )
    if st.button("Clear chat"):
        st.session_state.messages = []
        st.session_state.files = []
        st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("provider"):
            st.caption(provider_label(msg["provider"]))

if prompt := st.chat_input("Ask anything..."):
    history = [
        {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
    ]
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply, new_files = run_assistant(prompt, provider=provider, history=history)
        st.markdown(reply)
        st.caption(provider_label(provider))
        for path in new_files:
            key = str(path.resolve())
            if key not in st.session_state.files:
                st.session_state.files.append(key)

    st.session_state.messages.append(
        {"role": "assistant", "content": reply, "provider": provider}
    )
