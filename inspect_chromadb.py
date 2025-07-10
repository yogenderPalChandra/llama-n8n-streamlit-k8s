from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

# Adjust to match your persist directory path
PERSIST_DIR = "./" 
MODEL_PATH = "/app/local"

embedding = HuggingFaceEmbeddings(model_name=MODEL_PATH)
vectordb = Chroma(persist_directory=PERSIST_DIR, embedding_function=embedding)

# Get the number of documents
docs = vectordb.get()
print("Total documents stored:", len(docs['documents']))
