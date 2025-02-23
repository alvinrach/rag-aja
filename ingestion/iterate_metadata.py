import json
from llama_index.core import VectorStoreIndex, Document, Settings, StorageContext
from llama_index.embeddings.fastembed import FastEmbedEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb


with open("data/linkaja_pair_question_answer.json", "r") as f:
    data = json.load(f)


embed_model = FastEmbedEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
Settings.embed_model = embed_model

db = chromadb.PersistentClient(path="./chroma_db")
chroma_collection = db.get_or_create_collection("seconddoc")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

documents = []
for item in data:
    print(item)
    chunk_text = f"Pertanyaan: {item['question']}\nJawaban: {item['answer']}"
    metadata = {"topik": item["topik"], "level": item["level"]}
    documents.append(Document(text=chunk_text, metadata=metadata))
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context, embed_model=embed_model
)
print(chroma_collection.count())
