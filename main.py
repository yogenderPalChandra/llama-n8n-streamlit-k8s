from flask import Flask, request, jsonify
from agent_tools.agent_executor import setup_agent
from rag_pipeline.load_docs import load_and_split
from rag_pipeline.embed_and_store import create_vectorstore
import os

PERSIST_DIR = "rag_pipeline/db"
DOC_PATH = "rag_pipeline/data/test.txt"

app = Flask(__name__)

def bootstrap_vector_db():
    os.makedirs("rag_pipeline/data", exist_ok=True)
    chunks = load_and_split(DOC_PATH)
    create_vectorstore(chunks, persist_dir=PERSIST_DIR)

# 🔧 Initially index at startup
bootstrap_vector_db()
agent = setup_agent()

@app.route("/query", methods=["POST"])
def query():
    data = request.json
    if not data or "question" not in data:
        return jsonify({"error": "Missing 'question' field"}), 400
    question = data["question"]
    answer = agent.invoke(question)
    return jsonify({"question": question, "answer": answer})

# 🔧 New endpoint for n8n to call
@app.route("/reindex", methods=["POST"])
def reindex():
    print("[INFO] Reindexing triggered by n8n...")
    bootstrap_vector_db()
    return jsonify({"status": "reindex complete"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
