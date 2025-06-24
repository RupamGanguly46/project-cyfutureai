import os
import hashlib
from dotenv import load_dotenv
# from langchain.document_loaders import (
#     TextLoader, PDFPlumberLoader, Docx2txtLoader,
#     UnstructuredPowerPointLoader, UnstructuredExcelLoader, CSVLoader
# )
from langchain.text_splitter import CharacterTextSplitter
# from langchain.embeddings import AzureOpenAIEmbeddings
# from langchain.vectorstores import FAISS

from langchain_community.document_loaders import (
    TextLoader, PDFPlumberLoader, Docx2txtLoader,
    UnstructuredPowerPointLoader, UnstructuredExcelLoader, CSVLoader
)
from langchain_community.vectorstores import FAISS
# For OpenAI embeddings:
from langchain_openai import AzureOpenAIEmbeddings

# Load environment variables from .env
load_dotenv()

# Config
FOLDER_PATH = "knowledge_base"
INDEX_PATH = "faiss_index"
HASH_FILE = "index_hash.txt"

# ✅ Hashing function
def calculate_folder_hash(folder_path):
    sha = hashlib.sha256()
    for root, _, files in os.walk(folder_path):
        for file in sorted(files):  # sort for consistent order
            path = os.path.join(root, file)
            with open(path, "rb") as f:
                while chunk := f.read(8192):
                    sha.update(chunk)
    return sha.hexdigest()

def load_saved_hash():
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, "r") as f:
            return f.read().strip()
    return None

def save_hash(hash_value):
    with open(HASH_FILE, "w") as f:
        f.write(hash_value)

# ✅ Document loader
def load_documents(folder_path):
    docs = []
    for filename in os.listdir(folder_path):
        path = os.path.join(folder_path, filename)
        ext = filename.lower().split('.')[-1]
        try:
            if ext == "txt":
                docs.extend(TextLoader(path).load())
            elif ext == "pdf":
                docs.extend(PDFPlumberLoader(path).load())
            elif ext == "docx":
                docs.extend(Docx2txtLoader(path).load())
            elif ext in ["ppt", "pptx"]:
                docs.extend(UnstructuredPowerPointLoader(path).load())
            elif ext in ["xls", "xlsx"]:
                docs.extend(UnstructuredExcelLoader(path).load())
            elif ext == "csv":
                docs.extend(CSVLoader(path).load())
            else:
                print(f"Unsupported file type: {filename}")
        except Exception as e:
            print(f"Failed to load {filename}: {e}")
    return docs

# ✅ Azure OpenAI Embeddings Setup
embeddings = AzureOpenAIEmbeddings(
    azure_deployment="embed",
    # model="text-embedding-3-large",
    azure_endpoint=os.getenv("EMBED_ENDPOINT"),
    openai_api_key=os.getenv("EMBED_API_KEY"),
    openai_api_version="2024-02-01"
)

# ✅ Index builder
def build_index(folder_path, index_path):
    docs = load_documents(folder_path)
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = []
    for doc in docs:
        chunks.extend(splitter.split_documents([doc]))
    
    if not chunks:
        print("⚠️ No chunks to embed — skipping FAISS index creation.")
        return None

    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(index_path)
    return vectorstore

# ✅ Main logic: Load or Rebuild with hash check
current_hash = calculate_folder_hash(FOLDER_PATH)
saved_hash = load_saved_hash()

if not os.path.exists(INDEX_PATH) or current_hash != saved_hash:
    print("📄 Changes detected or index missing: Rebuilding FAISS index...")
    vectorstore = build_index(FOLDER_PATH, INDEX_PATH)
    save_hash(current_hash)
else:
    print("✅ No changes detected. Loading existing FAISS index...")
    # vectorstore = FAISS.load_local(INDEX_PATH, embeddings)
    vectorstore = FAISS.load_local(INDEX_PATH, embeddings, allow_dangerous_deserialization=True)


# ✅ Retrieval function
def retrieve_context(query, k=3):
    if not vectorstore:
        return "⚠️ No knowledge base available yet."
    docs = vectorstore.similarity_search(query, k=k)
    return "\n".join([doc.page_content for doc in docs])
