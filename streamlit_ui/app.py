import streamlit as st
import os
import requests

SHARED_FOLDER = "/data"
N8N_WEBHOOK_URL = "http://n8n.ollama.svc.cluster.local:5678/webhook/reindex"

st.title("📄 Upload Case Files")

uploaded_file = st.file_uploader("Upload a .txt file", type="txt")

if uploaded_file is not None:
    file_path = os.path.join(SHARED_FOLDER, uploaded_file.name)
    
    # Save uploaded file to shared PVC
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"✅ Saved {uploaded_file.name} to shared volume.")

    # Trigger n8n to reindex
    try:
        resp = requests.post(N8N_WEBHOOK_URL)
        if resp.status_code == 200:
            st.success("🔁 Reindex triggered via n8n!")
        else:
            st.warning(f"n8n responded with status code: {resp.status_code}")
    except Exception as e:
        st.error(f"Error contacting n8n: {e}")
