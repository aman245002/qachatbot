from sentence_transformers import SentenceTransformer

# Load pre-trained model (small and fast)
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embeddings(text_chunks):
    return model.encode(text_chunks, show_progress_bar=True)
