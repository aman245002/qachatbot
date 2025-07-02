import os
import streamlit as st
from dotenv import load_dotenv
from ingestion.parse_pdf import extract_text_from_pdf
from ingestion.parse_docx import extract_text_from_docx
from ingestion.parse_txt import extract_text_from_txt
from ingestion.chunking import chunk_text
from vectorstore.embedder import get_embeddings
from vectorstore.store import store_embeddings, query_similar_chunks
from qa.answer_generator import generate_multistep_answer
from sentence_transformers import SentenceTransformer
import chromadb

# ========================================
# Setup
# ========================================
os.environ["STREAMLIT_WATCH_DIRECTORIES"] = "false"
load_dotenv()
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# Setup vector DB
DB_PATH = "../vector_db"
client = chromadb.PersistentClient(path=DB_PATH)

# ========================================
# Streamlit UI
# ========================================
st.set_page_config(page_title="QA Bot", page_icon="🤖", layout="centered")
st.title("📘 QA Bot for Technical Manuals")
st.markdown("Upload a manual and ask multi-step 'how-to' questions.")

# Upload + Question Input
uploaded_file = st.file_uploader("Upload a file", type=["pdf", "docx", "txt"])
query = st.text_input("Ask a question:")

if uploaded_file and query:
    # Save file temporarily
    temp_path = f"temp_{uploaded_file.name}"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.read())

    # Clear old collection and create new
    if "manual_chunks" in [c.name for c in client.list_collections()]:
        client.delete_collection("manual_chunks")
    collection = client.get_or_create_collection("manual_chunks")

    # Document parsing
    with st.spinner("🔍 Extracting and embedding document..."):
        if uploaded_file.name.endswith(".pdf"):
            raw_text = extract_text_from_pdf(temp_path)
        elif uploaded_file.name.endswith(".docx"):
            raw_text = extract_text_from_docx(temp_path)
        elif uploaded_file.name.endswith(".txt"):
            raw_text = extract_text_from_txt(temp_path)
        else:
            st.error("Unsupported file format.")
            st.stop()

        # Chunking and embedding
        chunks = chunk_text(raw_text, chunk_size=100, overlap=20)
        embeddings = get_embeddings(chunks)
        store_embeddings(chunks, embeddings, collection)

    # Answer generation
    with st.spinner("💬 Generating answer using Groq..."):
        top_chunk_scores = query_similar_chunks(query, embed_model, collection)
        answer = generate_multistep_answer(query, top_chunk_scores)


    # Display
    st.subheader("🧠 Answer:")
    st.markdown(answer)

    # Cleanup
    os.remove(temp_path)
