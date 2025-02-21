import streamlit as st
from src.modules import rag_query_nonload

st.title("Rag Agent")

query = st.text_input("Input Your Question")
if query:
    result = rag_query_nonload(query)

    st.write("The result for your question:")

    if result["score"]>=0.3:
        st.markdown("""
            <style>
                .tag {
                    display: inline-block;
                    background-color: #e0e0e0;
                    color: black;
                    padding: 5px 10px;
                    border-radius: 15px;
                    margin-right: 5px;
                    font-size: 14px;
                    font-weight: bold;
                }
            </style>
        """, unsafe_allow_html=True)
        tags = result["metadata"]
        tag_html = " ".join([f"<span class='tag'>{tag}</span>" for tag in tags])
        st.markdown(tag_html, unsafe_allow_html=True)

    st.write(result["response"])

