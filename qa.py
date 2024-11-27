""" Demonstration oh how to create a chatbot with Streamlit

Execution: streamlit run qa.py

References:
    - https://streamlit.io/generative-ai
    - https://docs.streamlit.io/library/api-reference/chat/st.chat_message
    - https://docs.streamlit.io/library/api-reference/chat/st.chat_input
"""

import os
import uuid
import fitz  # PyMuPDF
import tempfile
import chromadb
import streamlit as st
from sentence_transformers import SentenceTransformer

from openai import OpenAI
from chonkie import SentenceChunker
from autotiktokenizer import AutoTikTokenizer

########################################################################################
# Initial Configuration ################################################################
########################################################################################
# Split documents into smaller chunks
tokenizer = AutoTikTokenizer.from_pretrained("gpt2")
TEXT_SPLITTER = SentenceChunker(
    tokenizer=tokenizer, chunk_size=512, chunk_overlap=128, min_sentences_per_chunk=1
)

MODEL_EMBEDDINGS = SentenceTransformer("all-MiniLM-L6-v2")

DB_CLIENT = chromadb.Client()
DB_COLLECTION = DB_CLIENT.get_or_create_collection(name="streamlit_course")

SYSTEM_PROMPT = """
You are an exceptional reader that gently answers questions.
"""

USER_TEMPLATE = """
You are an exceptional reader that gently answers questions.

You know the following context information:

{chunks_formatted}

Answer the following question from a customer.
Use only information from the previous context information.
Do not invent information.

Question: {query}

Answer:
"""


LLM = OpenAI()

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "How can I help you?"}
    ]


st.write("# 🤖 Talk with your data")
# Sidebar
st.sidebar.title("ℹ️ About")
st.sidebar.info(
    "This app uses ChromaDB to store and retrieve information from a PDF document. "
    "To start, upload a PDF file and ask a question."
)

########################################################################################
# Data Processing ######################################################################
########################################################################################
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
if uploaded_file is None:
    st.stop()  # Stop the script execution if no file is uploaded

pid = str(uuid.uuid4())

with st.spinner("Loading and splitting the document..."):
    # Load the PDF file uploaded by the user and split it
    temp_dir = tempfile.TemporaryDirectory()
    temp_filepath = os.path.join(temp_dir.name, uploaded_file.name)
    with open(temp_filepath, "wb") as f:
        f.write(uploaded_file.getvalue())

    loader = fitz.open(temp_filepath)

    loader = fitz.open(temp_filepath)
    doc = ""
    for page_num in range(len(doc)):  # Extract text from each page
        page = doc[page_num]
        doc += f"{page.get_text()}\n"

    chunks = TEXT_SPLITTER.chunk(doc)
    st.success("Document loaded and split successfully")

# Add generated chunks to our ChromaDB database
with st.spinner("Adding documents to the database..."):
    for chunk in chunks:
        chunk_embedded = MODEL_EMBEDDINGS.encode(chunk.text)

        # We don't need to handle the state of the app because the collection
        # is stored on disk and its state is "preserved" between runs
        DB_COLLECTION.add(
            documents=[chunk.text],
            embeddings=[chunk_embedded.tolist()],
            metadatas=[{"pid": pid}],
            ids=[str(uuid.uuid4())],
        )
    st.success("Documents added to ChromaDB!")
    # Show the number of documents in the database
    st.info(f"The database contains {DB_COLLECTION.count()} documents")


########################################################################################
# Chat with user #######################################################################
########################################################################################
# Ask the user
st.title("💬 Chatbot")
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Using walrus operator: assigns and evaluates an expression simultaneously
if query := st.chat_input():
    st.chat_message("user").write(query)

    query_embedded = MODEL_EMBEDDINGS.encode(query)
    similar_chunks = DB_COLLECTION.query(
        query_embeddings=[query_embedded.tolist()], n_results=3, where={"pid": pid}
    )
    retrieved_chunks = [chunk for chunk in similar_chunks["documents"][0]]

    # Format the prompt
    chunks_formatted = "\n\n".join(retrieved_chunks)
    user_prompt = USER_TEMPLATE.format(chunks_formatted=chunks_formatted, query=query)

    # Generate answer
    response = (
        LLM.chat.completions.create(  # Change the method
            model="gpt-4o-mini",
            messages=[  # Change the prompt parameter to messages parameter
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0,
        )
        .choices[0]
        .message.content
    )
    st.chat_message("assistant").write(response)

    # Save the conversation
    st.session_state.messages.append({"role": "user", "content": query})
    st.session_state.messages.append({"role": "assistant", "content": response})
