import streamlit as st
import requests

st.set_page_config(page_title="RAG Chatbot", page_icon="🤖", layout="centered")

API_BASE = "http://127.0.0.1:8000"
UPLOAD_URL = f"{API_BASE}/user/upload_file"
CHAT_URL = f"{API_BASE}/user/chat"

st.title("💬 AI Technical Assistant")
st.caption("Ask questions about your uploaded documents.")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None

# Sidebar for upload
with st.sidebar:
    st.header("📂 Upload Document")
    uploaded_file = st.file_uploader("Upload a PDF, TXT, or DOCX file", type=["pdf", "txt", "docx"])

    if uploaded_file is not None:
        with st.spinner("Uploading file..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                res = requests.post(UPLOAD_URL, files=files)
                if res.status_code == 200:
                    st.success(f"✅ {uploaded_file.name} uploaded successfully!")
                    st.session_state.uploaded_file = uploaded_file.name
                else:
                    st.error(f"❌ Upload failed: {res.text}")
            except Exception as e:
                st.error(f"⚠️ Connection error: {e}")

    st.markdown("---")
    if st.session_state.uploaded_file:
        st.markdown(f"**Active document:** `{st.session_state.uploaded_file}`")

    st.markdown("### ℹ️ Info")
    st.markdown("- Backend: FastAPI + LangChain")
    st.markdown("- Vector DB: Chroma")
    st.markdown("- Model: `llama3.2-vision`")

# Display chat messages
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if user_input := st.chat_input("Ask something about your document..."):
    st.chat_message("user").markdown(user_input)
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            try:
                res = requests.post(CHAT_URL, json={"query": user_input})
                if res.status_code == 200:
                    answer = res.json().get("response", "No response received.")
                else:
                    answer = f"❌ Error: {res.status_code}"
            except Exception as e:
                answer = f"⚠️ Connection error: {e}"
            st.markdown(answer)

    st.session_state.chat_history.append({"role": "assistant", "content": answer})
