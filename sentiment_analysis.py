""" A simple sentiment analysis app using Hugging Face's pipeline. 

Execution: streamlit run sentiment_analysis.py

Try using following text to see the sentiment analysis:
- I love using Streamlit to build web applications!
- I love using Streamlit to build web applications! If I were dead!
- I love using Streamlit to build web applications! If I were dead! And revived in heaven :D
- I love using Streamlit to build web applications! If I were dead! And revived in heaven :D If heaven is the worst place on earth :O
"""

import time
import random
import streamlit as st
import pandas as pd
from transformers import pipeline
import plotly.graph_objs as go

# Set page config
st.set_page_config(page_title="Sentiment Analyzer", layout="wide")

########################################################################################
# Definitions and Functions ############################################################
########################################################################################
if "history" not in st.session_state:  # Prediction History
    st.session_state.history = []  # Store the history of sentiment analysis results

if "sentiment" not in st.session_state:  # Store current sentiment for UI purposes
    st.session_state.sentiment = "POSITIVE"  # Store the current sentiment


# Cache the model loading
@st.cache_resource
def load_model():
    return pipeline("sentiment-analysis")


# Define the create_plot function
def create_plot(sentiment_result: dict) -> go.Figure:
    """Create a Plotly plot based on the sentiment analysis result.

    Args:
        sentiment_result (dict): The sentiment analysis result from the pipeline.

    Returns:
        go.Figure: A Plotly figure object.

    Example:
    >>> sentiment_result = {
    >>>     "label": "POSITIVE",
    >>>     "score": 0.9999
    >>> }
    >>> create_plot(sentiment_result)
    """
    label = sentiment_result["label"]
    # set negative_score  and positive_score
    if label == "POSITIVE":
        positive_score = sentiment_result["score"]
        negative_score = 1 - sentiment_result["score"]
    else:
        positive_score = 1 - sentiment_result["score"]
        negative_score = sentiment_result["score"]

    data = [
        go.Bar(
            x=["POSITIVE", "NEGATIVE"],
            y=[positive_score, negative_score],
            marker_color=["#8EF26F", "#FC6868"],
        )
    ]

    layout = go.Layout(
        yaxis=dict(title="Probability"),
    )

    return go.Figure(data=data, layout=layout)


########################################################################################
# User Interface #######################################################################
########################################################################################
classifier = load_model()

# Sidebar
st.sidebar.title("ℹ️ About")
st.sidebar.info("This app uses a Hugging Face pipeline to analyze sentiment in text.")

# Main content
heart = "💔" if st.session_state.sentiment == "NEGATIVE" else "❤️"
title = st.title(f"{heart} Sentiment Analysis App")

# Text input
text_input = st.text_area(
    "Enter text to analyze:", "I love using Streamlit for creating web apps!"
)

# Analyze button
fig = None
if st.button("Analyze Sentiment"):
    progress_bar = st.progress(0)
    for i in range(100):
        # Random delay between 0.25 to 2 seconds total
        time.sleep(random.uniform(0.0025, 0.02))
        progress_bar.progress(i + 1)

    result = classifier(text_input)[0]
    st.session_state.history.append(
        {"text": text_input, "sentiment": result["label"], "score": result["score"]}
    )
    st.session_state.sentiment = result["label"]
    fig = create_plot(result)


heart = "💔" if st.session_state.sentiment == "NEGATIVE" else "❤️"
# TRICK: Recover the title reference, now we have latest sentiment state
title.title(f"{heart} Sentiment Analysis App")


col1, col2 = st.columns(2)

with col1:
    # Display history
    if st.session_state.history:
        st.subheader("Analysis History")
        df = pd.DataFrame(st.session_state.history)
        st.dataframe(df)

with col2:
    # Visualization using Plotly
    if fig is not None:
        st.write("## Sentiment Analysis Result")
        st.write(f"Sentence: `{text_input}`")
        st.plotly_chart(fig, use_container_width=True)
