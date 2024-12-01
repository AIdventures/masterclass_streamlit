""" Demonstration oh how to create a chatbot with Streamlit

Execution: streamlit run qa.py

References:
    - https://streamlit.io/generative-ai
    - https://docs.streamlit.io/library/api-reference/chat/st.chat_message
    - https://docs.streamlit.io/library/api-reference/chat/st.chat_input
"""

import os
import fitz  # PyMuPDF
import tempfile
import streamlit as st

from openai import OpenAI

########################################################################################
# Initial Configuration ################################################################
########################################################################################
SYSTEM_PROMPT = """
You are an exceptional reader that gently answers questions.

Your task is to answer questions from customers in a concise and informative way.
"""

INITIAL_USER_TEMPLATE = """
Given the following context information:

{document_text}

Answer the following question using only information
from the previous context information.
Do not made up any information.

Question: {query}

Answer:
"""

HISTORY_USER_TEMPLATE = """
Given the following context information:

{document_text}

The conversation so far:

{conversation_history}

Answer the following question using only information
from the previous context information, conversation history, and the new question.

Question: {query}

Answer:
"""

if "doc" not in st.session_state:
    st.session_state["doc"] = ""

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "How can I help you?"}
    ]


st.write("# 🤖 Talk with your data")
# Sidebar
st.sidebar.title("ℹ️ About")
st.sidebar.info("To start, upload a PDF file and ask a question.")

user_openai_key = st.sidebar.text_input(
    "OpenAI API key",
    value=os.environ.get("OPENAI_API_KEY", ""),
    type="password",
)

if not user_openai_key:
    st.warning(
        "Please provide an OpenAI API key to use the chatbot. "
        "You can get one by signing up at https://platform.openai.com"
    )
    st.stop()

LLM = OpenAI(api_key=user_openai_key)


########################################################################################
# Data Processing ######################################################################
########################################################################################
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
if uploaded_file is None:
    st.stop()  # Stop the script execution if no file is uploaded

if st.session_state.doc == "":
    with st.spinner("Loading the document..."):
        # Load the PDF file uploaded by the user and split it
        temp_dir = tempfile.TemporaryDirectory()
        temp_filepath = os.path.join(temp_dir.name, uploaded_file.name)
        with open(temp_filepath, "wb") as f:
            f.write(uploaded_file.getvalue())

        loader = fitz.open(temp_filepath)
        st.session_state.doc = "".join([page.get_text() + "\n" for page in loader])
        st.success("Document loaded successfully")

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

    # Format the prompt
    if len(st.session_state.messages) == 1:  # First question
        user_prompt = INITIAL_USER_TEMPLATE.format(
            document_text=st.session_state.doc, query=query
        )
    else:  # Subsequent questions
        conversation_history = ""
        for msg in st.session_state.messages:
            conversation_history += f"{msg['role']}: {msg['content']}\n"

        user_prompt = HISTORY_USER_TEMPLATE.format(
            document_text=st.session_state.doc,
            conversation_history=conversation_history,
            query=query,
        )

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
