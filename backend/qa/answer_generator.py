import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-8b-8192"  # You may also try mistral-7b-8k

headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

def generate_multistep_answer(query, chunk_score_pairs):
    all_answers = []

    # Sort by similarity (higher = more similar)
    sorted_chunks = sorted(chunk_score_pairs, key=lambda x: x[1], reverse=True)

    for i, (chunk, similarity) in enumerate(sorted_chunks):
        # Normalize similarity score from [-1, 1] to [0, 1]
        similarity_score = round((similarity + 1) / 2, 2)

        prompt = f"""You are a helpful assistant. Based on the following documentation snippet, answer the question in a clear, step-by-step format.

Context:
\"\"\"
{chunk}
\"\"\"

Question: {query}

Answer in 2 to 5 clear, numbered steps:
"""

        payload = {
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.4,
            "max_tokens": 512,
            "top_p": 0.9
        }

        try:
            response = requests.post(API_URL, headers=headers, json=payload)
            if response.status_code == 200:
                content = response.json()["choices"][0]["message"]["content"].strip()
                all_answers.append(
                    f"### Perspective {i+1} (similarity: {similarity_score:.2f}):\n{content}"
                )
            else:
                all_answers.append(
                    f"### Perspective {i+1}:\n❌ Error: {response.status_code} - {response.text}"
                )
        except Exception as e:
            all_answers.append(f"### Perspective {i+1}:\n❌ Exception: {str(e)}")

    return "\n\n".join(all_answers)
