FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

COPY requirements_sentiment.txt requirements.txt
COPY sentiment_analysis.py sentiment_analysis.py

RUN pip3 install -r requirements.txt

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "sentiment_analysis.py", "--server.port=8501", "--server.address=0.0.0.0"]