from backend.db.faiss import get_chunks, get_vector_storage
from backend.processor.docs_preprocessing import get_text 
import streamlit as st
from backend.db.faiss import user_input

if 'messages' not in st.session_state:
     st.session_state['messages'] = []

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
                st.session_state['messages'].append({"role":"system",
                                                     "content": "File Processed Successfully."})
                st.success("Done")

user_query = st.chat_input("Enter your query here...")
if user_query:
    st.session_state['messages'].append({"role":"user",
                                         "content": user_query})
    response = user_input(user_query)
    st.session_state['messages'].append({"role":"assistant",
                                         "content": response})

for message in st.session_state['messages']:
    if message['role'] == 'user':
        st.write(f"**User:** {message['content']}")
    elif message['role'] == 'assistant':
        st.write(f"**Assistant Response:** {message['content']}")
        st.write("*"*50)
    elif message['role'] == 'system':
        st.write(f"**System:** {message['content']}")
        st.write("*"*50)
