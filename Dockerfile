FROM python:3.12.8-slim

WORKDIR /app

# Install dependencies first for better caching
COPY requirements-lite.txt .
RUN pip install --no-cache-dir -r requirements-lite.txt

# Copy only necessary files
COPY dashboard.py .
COPY ingestion/ ingestion/
COPY data/ data/
COPY src/ src/
COPY .env .env  

# Run preprocessing script
RUN python ingestion/iterate_metadata.py

# Expose Streamlit port
EXPOSE 8501

# Start the Streamlit app
CMD ["streamlit", "run", "dashboard.py", "--server.address=0.0.0.0"]
