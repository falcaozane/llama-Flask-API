import os
import logging
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Set up logging
logging.basicConfig(level=logging.INFO)
DATA_PATH = 'data/'
DB_FAISS_PATH = 'vectorstore/db_faiss'

# Create vector database
def create_vector_db():
    if not os.path.exists(DATA_PATH):
        logging.error(f"Data path {DATA_PATH} does not exist.")
        return
    
    # Load PDF documents using PyPDFLoader
    try:
        loader = DirectoryLoader(DATA_PATH, glob='*.pdf', loader_cls=PyPDFLoader)
        documents = loader.load()
        logging.info(f"Loaded {len(documents)} documents from {DATA_PATH}")
    except Exception as e:
        logging.error(f"Error loading documents: {e}")
        return
    
    # Split documents into manageable chunks
    try:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        texts = text_splitter.split_documents(documents)
        logging.info(f"Split documents into {len(texts)} text chunks.")
    except Exception as e:
        logging.error(f"Error splitting documents: {e}")
        return

    # Initialize embeddings model
    try:
        embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
        logging.info("Initialized HuggingFace embeddings model.")
    except Exception as e:
        logging.error(f"Error initializing embeddings model: {e}")
        return

    # Create FAISS vector database
    try:
        db = FAISS.from_documents(texts, embeddings)
        db.save_local(DB_FAISS_PATH)
        logging.info(f"FAISS database created and saved at {DB_FAISS_PATH}")
    except Exception as e:
        logging.error(f"Error creating FAISS database: {e}")
        return

if __name__ == "__main__":
    create_vector_db()
