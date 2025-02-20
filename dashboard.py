import streamlit as st
from src.modules import rag_query

st.title("Rag Agent")

query = st.text_input("Input Your Question")
if query:
    result = rag_query(query)

    st.write("The result for your question:")
    st.write(result)