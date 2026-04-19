import os
import sys
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from agent.utils.embeddings import get_embeddings_model

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config import EMBEDDINGS_MODEL

def setup_vector_store(knowledge_dir=None):
    """Build a FAISS vector store from knowledge text files."""
    if knowledge_dir is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        knowledge_dir = os.path.join(base_dir, "knowledge")

    embeddings = get_embeddings_model(EMBEDDINGS_MODEL)

    loader = DirectoryLoader(knowledge_dir, glob="**/*.txt", loader_cls=TextLoader)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
    docs = text_splitter.split_documents(documents)

    vectorstore = FAISS.from_documents(docs, embeddings)
    return vectorstore

def get_retriever():
    """Returns a FAISS retriever searching the knowledge base."""
    vectorstore = setup_vector_store()
    return vectorstore.as_retriever(search_kwargs={"k": 4})
