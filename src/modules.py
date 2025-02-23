from dotenv import load_dotenv
load_dotenv()

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, PromptTemplate
from llama_index.embeddings.fastembed import FastEmbedEmbedding
from llama_index.llms.gemini import Gemini
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
import chromadb

def get_query_engine(model_name="gemini"):
    embed_model = FastEmbedEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
    if model_name=="gemini":
        llm = Gemini(model="models/gemini-2.0-flash")
    elif model_name=="gpt-4o-mini":
        llm = OpenAI(model="gpt-4o-mini", temperature=0.1)
    else:
        raise Exception("choices for model_name only 'gemini' and 'gpt-4o-mini'")

    Settings.llm = llm
    Settings.embed_model = embed_model

    db = chromadb.PersistentClient(path="./chroma_db")
    chroma_collection = db.get_or_create_collection("seconddoc")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

    index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store,
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

    return query_engine, index, chroma_collection

def get_query_engine_dashboard(query):
    query_engine, _, _ = get_query_engine("gpt-4o")
    response = query_engine.query(query)

    res = {
        "response" : response.response,
        "score": response.source_nodes[0].score,
        "metadata" : list(list(response.metadata.values())[0].values())
    }

    print(res)
    return res
