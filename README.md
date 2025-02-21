# rag-aja

## RAG using llama-index and streamlit.

Query your search and get the explanation from inputted document.

![alt text](image.png)

Ingest your data first by doing


```
python ingestion/iterate_metadata.py
```

## To run:

```
streamlit run dashboard.py
```

## Preprocessing Step

- Assumption : There are several parts that dont have topik or level, so we assume these data points have those topic and level

## Code Formatter:

- Black – Automatically formats code according to PEP 8 standards