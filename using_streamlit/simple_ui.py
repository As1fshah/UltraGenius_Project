from backend.db.faiss import get_chunks, get_vector_storage
from backend.processor.docs_preprocessing import get_text 
import streamlit as st
from backend.db.faiss import user_input

with st.sidebar:
        st.title("Document ChatBot")
        uploaded_files = st.file_uploader("Upload your PDF Files and Click on the Submit & Process Button", 
                                    type = ['pdf','docx'],
                                    accept_multiple_files=True)
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                text = get_text(uploaded_files)
                chunks = get_chunks(text)
                get_vector_storage(chunks)
                st.success("Done")

user_query = st.text_input("Enter your query here...")
if user_query:
    response = user_input(user_query)
    st.write(response)