import streamlit as st
import requests
import os

# Constants
DATA_DIR = "/data"
RAG_AGENT_URL = "http://rag-agent.ollama.svc.cluster.local:8080/query"
N8N_WEBHOOK_URL = "http://n8n.ollama.svc.cluster.local:5678/webhook/reindex"

st.set_page_config(page_title="Staff Knowledge Assistant", layout="centered")

st.title("📄 Staff Document Assistant")

# --- File Upload Section ---
st.header("📤 Upload a Text Document")

uploaded_file = st.file_uploader("Upload .txt file", type="txt")

if uploaded_file is not None:
    save_path = os.path.join(DATA_DIR, uploaded_file.name)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"✅ Uploaded `{uploaded_file.name}`")

    # Notify n8n to reindex
    try:
        r = requests.post(N8N_WEBHOOK_URL)
        if r.status_code == 200:
            st.success("🔁 Reindex ttriggered successfully.")
        else:
            st.error(f"Failed to trigger reindex: {r.status_code}")
    except Exception as e:
        st.error(f"Error calling n8n webhook: {e}")

st.divider()

# --- Query Section ---
st.header("❓ Ask a Question")

question = st.text_input("Type your question here:")

if st.button("Ask"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        try:
            response = requests.post(
                RAG_AGENT_URL,
                json={"question": question},
                timeout=1180
            )
            if response.status_code == 200:
                data = response.json()
                st.success("Answer:")
                st.markdown(data["answer"])
            else:
                st.error(f"Error: {response.status_code}")
        except Exception as e:
            st.error(f"Error contacting RAG agent: {e}")
