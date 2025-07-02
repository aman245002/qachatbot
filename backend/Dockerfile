FROM python:3.10-slim

WORKDIR /app

# COPY only the backend folder contents into /app
COPY backend/ /app

# Now /app has requirements.txt and other files
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
