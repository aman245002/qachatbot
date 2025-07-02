from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def store_embeddings(text_chunks, embeddings, collection):
    for i, (text, embedding) in enumerate(zip(text_chunks, embeddings)):
        collection.add(
            documents=[text],
            embeddings=[embedding.tolist()],
            ids=[f"chunk_{i}"]
        )
    print(f"✅ Stored {len(text_chunks)} chunks into ChromaDB.")


def query_similar_chunks(query_text, embedder, collection, top_k=3):
    # Embed the query
    query_vec = embedder.encode([query_text])[0]

    # Query top_k candidates
    results = collection.query(
        query_embeddings=[query_vec.tolist()],
        n_results=top_k,
        include=["documents", "embeddings"]  # Required for manual similarity
    )

    documents = results["documents"][0]
    embeddings = results["embeddings"][0]

    # Compute true cosine similarity for each retrieved chunk
    chunk_score_pairs = []
    for doc, emb in zip(documents, embeddings):
        score = cosine_similarity([query_vec], [emb])[0][0]
        chunk_score_pairs.append((doc, score))  # score ∈ [-1, 1]

    return chunk_score_pairs
