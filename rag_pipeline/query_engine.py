from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
import os

def run_query(question, persist_dir="rag_pipeline/db"):
    print(f"Question received: {question}")
    embedding = HuggingFaceEmbeddings(model_name="/app/local")
    vectordb = Chroma(persist_directory=persist_dir, embedding_function=embedding)
    retriever = vectordb.as_retriever(search_kwargs={"k": 3})
    docs = retriever.get_relevant_documents(question)
    print(f"🔍 Retrieved {len(docs)} documents")
    for i, doc in enumerate(docs):
        print(f" - Doc {i+1}: {doc.page_content[:100]}...")
    llm = Ollama(model="llama3", base_url=os.getenv("OLLAMA_HOST"))
    qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, verbose=True)
    return qa.run(question)
