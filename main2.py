from flask import Flask, request, jsonify
from agent_tools.agent_executor import setup_agent
from rag_pipeline.load_docs import load_and_split
from rag_pipeline.embed_and_store import create_vectorstore
import os
import shutil

PERSIST_DIR = "/app/rag_pipeline/db"

RE_INDEX_PATH = "/data"


agent = setup_agent()
app = Flask(__name__)

@app.route("/query", methods=["POST"])
def query():
    data = request.json
    if not data or "question" not in data:
        return jsonify({"error": "Missing 'question' field"}), 400

    question = data["question"]
    answer = agent.invoke(question)
    #answer = agent.invoke({"input": question}) 
    return jsonify({"question": question, "answer": answer})

# 🔧 New endpoint for n8n to call
@app.route("/reindex", methods=["POST"])
def reindex():
    all_chunks = []
    for file in os.listdir(RE_INDEX_PATH):
        file_path = os.path.join(RE_INDEX_PATH, file)
        if os.path.isfile(file_path) and file.endswith(".txt"):
            chunks = load_and_split(file_path)
            all_chunks.extend(chunks)
    print ("[INFO] printing Chunks at reindx:", chunks)
    print("lenlenlenlen:", len(all_chunks))
    create_vectorstore(all_chunks, persist_dir=PERSIST_DIR)
    return jsonify({"status": "reindex complete"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
