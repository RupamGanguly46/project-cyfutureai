import os
import hashlib
from dotenv import load_dotenv
# from langchain.document_loaders import (
#     TextLoader, PDFPlumberLoader, Docx2txtLoader,
#     UnstructuredPowerPointLoader, UnstructuredExcelLoader, CSVLoader
# )
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
    # for filename in os.listdir(folder_path):
        # path = os.path.join(folder_path, filename)
   
    for root, _, files in os.walk(folder_path):
        for filename in files:
            path = os.path.join(root, filename)

            ext = filename.lower().split('.')[-1]
            try:
                if ext in ["txt","md"]:
                    docs.extend(TextLoader(path, encoding="utf-8").load())
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
                import traceback
                print(f"Failed to load {filename}: {repr(e)}")
                traceback.print_exc()
    return docs

import re
def clean_markdown_and_extract_links(text):
    """Extract links but PRESERVE other markdown formatting for LLM context"""
    urls = []
    
    # Only extract links, keep everything else
    def replacer(match):
        label, url = match.groups()
        urls.append((label, url))
        return f"[{label}]({url})"  # Keep the markdown link format
    
    text = re.sub(r'\[(.*?)\]\((.*?)\)', replacer, text)
    
    # Don't remove headers, bold, etc. - LLM needs this context!
    # Only clean up excessive whitespace
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)  # Max 2 consecutive newlines
    
    return text.strip(), urls


# ✅ Azure OpenAI Embeddings Setup
embeddings = AzureOpenAIEmbeddings(
    azure_deployment="embed",
    # model="text-embedding-3-large",
    azure_endpoint=os.getenv("EMBED_ENDPOINT"),
    openai_api_key=os.getenv("EMBED_API_KEY"),
    openai_api_version="2024-02-01"
)

from langchain.schema import Document
from langchain.text_splitter import MarkdownHeaderTextSplitter, CharacterTextSplitter

# ✅ Hybrid split & clean
def build_index(folder_path, index_path):
    docs = load_documents(folder_path)
    chunks = []
    char_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    md_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=[
        ("#", "H1"),
        ("##", "H2"),
        ("###", "H3"),
        ]
    )

    for doc in docs:
        if doc.metadata.get('source', '').lower().endswith('.md'):
            splits = md_splitter.split_text(doc.page_content)
            for split in splits:
                cleaned, urls = clean_markdown_and_extract_links(split.page_content)
                if cleaned:
                    chunks.append(Document(
                        page_content=cleaned,
                        metadata={"urls": urls}
                    ))

        else:
            char_chunks = char_splitter.split_documents([doc])
            for chunk in char_chunks:
                cleaned, urls = clean_markdown_and_extract_links(chunk.page_content)
                if cleaned:
                    chunks.append(Document(
                        page_content=cleaned,
                        metadata={"urls": urls}
                    ))

    if not chunks:
        print("⚠️ No chunks created — index build skipped.")
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

def strip_bold(text):
    return re.sub(r'\*\*(.*?)\*\*', r'\1', text)

# ✅ Retrieval function
# def retrieve_context(query, k=3):
#     if not vectorstore:
#         return "⚠️ No knowledge base available yet."
#     docs = vectorstore.similarity_search(query, k=k)
#     # return "\n".join([doc.page_content for doc in docs])
#     results = []
#     for doc in docs:
#         text = strip_bold(doc.page_content)
#         urls = doc.metadata.get("urls", [])
#         # Replace link text with "label (url)"
#         for label, url in urls:
#             text = text.replace(label, f"{label} ({url})")
#         results.append(text)
#     return "\n\n".join(results)

# def retrieve_context(query, k=3):
#     if not vectorstore:
#         return "⚠️ No knowledge base available yet."

def retrieve_context(query, k=3):
    """Return context WITH markdown formatting for LLM"""
    if not vectorstore:
        return "⚠️ No knowledge base available yet."

    docs = vectorstore.similarity_search(query, k=k)
    results = []
    for doc in docs:
        text = doc.page_content  # Keep ALL formatting
        urls = doc.metadata.get("urls", [])

        # Ensure links are properly formatted
        for label, url in urls:
            if f"[{label}]({url})" not in text:
                text = re.sub(rf'(?<!\w){re.escape(label)}(?!\w)', f"[{label}]({url})", text)

        results.append(text)

    return "\n\n".join(results)