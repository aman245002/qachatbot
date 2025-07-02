
# 🤖 QA ChatBot: Multi-Step Question Answering from Manuals

This is an intelligent **QA Bot** that can read technical manuals (PDF, DOCX, TXT), understand user queries, and return clear, **multi-step answers** from different perspectives within the document using **LLMs and semantic search**.

It uses:
- ✅ Document parsing (PDF/DOCX/TXT)
- ✅ Chunking & Embedding
- ✅ Vector similarity search with **ChromaDB**
- ✅ Multi-perspective response generation using **Groq LLaMA 3**
- ✅ A clean Streamlit frontend for upload + chat

---

## 🚀 Features

- 📂 **Upload** a user manual (PDF, DOCX, TXT)
- 🔍 **Ask a question** about how to do something in the manual
- 💡 **Get 2–5 multi-step answers** pulled from different relevant sections
- 🧠 **Ranking** by semantic similarity (cosine distance)
- 🌐 Fully deployable via **Render** or local Docker

---

## 📁 Project Structure

```
qachatbot/
├── backend/
│   ├── streamlit_app.py         # Main Streamlit app
│   ├── requirements.txt         # Python dependencies
│   ├── Dockerfile               # For deployment on Render
│   ├── ingestion/               # Text extraction + chunking
│   ├── vectorstore/             # Embedding + ChromaDB queries
│   ├── qa/                      # Answer generation using Groq
```

---

## 🧪 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/qachatbot.git
cd qachatbot/backend
```



### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Add Your Groq API Key

Create a `.env` file in `backend/`:

```
GROQ_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 5. Run the App

```bash
streamlit run streamlit_app.py
```

Then go to `http://localhost:8501`

---

## 📦 `requirements.txt`

```txt
streamlit
sentence-transformers
chromadb==0.4.14
protobuf==3.20.3
scikit-learn
python-dotenv
pdfplumber
python-docx
requests
```



---

## 🧠 Example Usage

1. Upload a PDF manual  
2. Ask: _"How do I install the software?"_  
3. Get multiple structured answers like:

```markdown
### Perspective 1 (similarity: 0.85):
1. Go to Setup Menu...
2. Click Install...
...

### Perspective 2 (similarity: 0.81):
1. From the dashboard...
```

---

## 📊 Evaluation (Optional)

You can add a CSV like:

| Query               | Answer Quality | Time Taken (s) |
|---------------------|----------------|----------------|
| How to configure X? | Good (4/5)      | 3.2            |
| How to reset?       | Excellent (5/5) | 2.8            |

---




