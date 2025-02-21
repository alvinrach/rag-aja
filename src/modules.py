from dotenv import load_dotenv
load_dotenv()

import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, PromptTemplate
from llama_index.embeddings.fastembed import FastEmbedEmbedding
from llama_index.llms.gemini import Gemini
from llama_index.core import Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
import chromadb

def rag_query_nonload(query):
    documents = SimpleDirectoryReader("data").load_data()
    embed_model = FastEmbedEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
    llm = Gemini(
        model="models/gemini-2.0-flash"
    )

    Settings.llm = llm
    Settings.embed_model = embed_model


    db = chromadb.PersistentClient(path="./chroma_db")
    chroma_collection = db.get_or_create_collection("seconddoc")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        embed_model=embed_model
    )

    query_engine = index.as_query_engine()

    qa_prompt_tmpl_str = (
        "Informasi konteks ada di bawah ini.\n"
        "---------------------\n"
        "{context_str}\n"
        "---------------------\n"
        "Berdasarkan informasi konteks dan bukan pengetahuan sebelumnya, "
        "jawablah pertanyaan berikut.\n"
        "Pertanyaan: {query_str}\n"
        "Jawaban: "
    )
    qa_prompt_tmpl = PromptTemplate(qa_prompt_tmpl_str)

    query_engine.update_prompts(
        {"response_synthesizer:text_qa_template": qa_prompt_tmpl}
    )
    response = query_engine.query(query)

    res = {
        "response" : response.response,
        "score": response.source_nodes[0].score,
        "metadata" : list(list(response.metadata.values())[0].values())
    }

    print(res)
    return res

def rag_query(query):
    documents = SimpleDirectoryReader("data").load_data()
    embed_model = FastEmbedEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
    llm = Gemini(
        model="models/gemini-2.0-flash"
    )

    Settings.llm = llm
    Settings.embed_model = embed_model


    db = chromadb.PersistentClient(path="./chroma_db")
    chroma_collection = db.get_or_create_collection("firstdoc")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        embed_model=embed_model
    )

    query_engine = index.as_query_engine()
    response = query_engine.query(query)

    return response.response