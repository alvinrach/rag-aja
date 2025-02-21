FROM python:3.12.8-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python ingestion/iterate_metadata.py

EXPOSE 8501

CMD streamlit run dashboard.py --server.address=0.0.0.0