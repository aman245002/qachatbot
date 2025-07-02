from ingestion.parse_pdf import extract_text_from_pdf
from ingestion.chunking import chunk_text

# Path to the sample document
file_path = "../data/example2.pdf"

# Step 1: Extract raw text from the PDF
text = extract_text_from_pdf(file_path)

# Step 2: Chunk the extracted text
chunks = chunk_text(text, chunk_size=100, overlap=20)

# Step 3: Print some outputs
print(f"\nTotal chunks created: {len(chunks)}")
print("\nFirst chunk preview:\n")
print(chunks[0])

from vectorstore.embedder import get_embeddings
from vectorstore.store import store_embeddings, query_similar_chunks
from sentence_transformers import SentenceTransformer

# Step 4: Embed the chunks
embeddings = get_embeddings(chunks)

# Step 5: Store in ChromaDB
store_embeddings(chunks, embeddings)

# Step 6: Query test
model = SentenceTransformer('all-MiniLM-L6-v2')
query = "How do I install the software?"
similar_chunks = query_similar_chunks(query, model)

print("\n🔍 Top matching chunks:\n")
for i, chunk in enumerate(similar_chunks):
    print(f"Chunk {i+1}:\n{chunk}\n{'-'*50}")

from qa.answer_generator import generate_multistep_answer

print("\n🧠 Generating multi-step answer using GPT...\n")
answer = generate_multistep_answer(query, similar_chunks)

print("✅ Final Answer:\n")
print(answer)
