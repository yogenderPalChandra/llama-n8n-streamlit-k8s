from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
import os

def create_vectorstore(chunks, persist_dir):
    embedding = HuggingFaceEmbeddings(model_name="/app/local")
    vectordb = Chroma(persist_directory=persist_dir, embedding_function=embedding)
    vectordb.add_documents(documents=chunks)
    vectordb.persist()
    print ('yesyyesyes persisted')
    return vectordb
