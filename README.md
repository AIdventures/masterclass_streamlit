# Streamlit Course

## Index

- [Introduction](#introduction)
- [Execution](#execution)
- [Requirements](#requirements)
- [Deployment](#deployment)
- [Environment Setup](#environment-setup)
  - [Installing Dependencies](#installing-dependencies)
  - [Configuring Pre-Commit Hooks](#configuring-pre-commit-hooks)
- [Notes](#notes)

## Introduction

This repository contains the code for the applications developed in the Streamlit course. There are two applications, which can be found at the following paths:

- [Sentiment Analysis](sentiment_analysis.py): Application that performs sentiment analysis on text using a Hugging Face pipeline. It allows users to input text and get a sentiment analysis result, which is visualized using Plotly.
- [PDF Document Q&A](qa.py): Application that allows users to upload a PDF document and ask questions about it. This uses the OpenAI API, which allows for text-based questions. The [PyMuPDF](https://pypi.org/project/PyMuPDF/) library is used to extract text from the PDF. The [Sentence Transformers](https://www.sbert.net/) library is used to generate embeddings for both the PDF content and the questions. Finally, the [ChromaDB](https://www.trychroma.com/) library is used to store embeddings and search for answers.

## Execution

To run the different applications, execute the following command:

```bash
streamlit run <application_path>
```

### Requirements

To run the applications, you must install the dependencies specified in the respective requirements files. The Python version used is `3.11`. It's recommended to use a virtual environment for installing the necessary packages. There are several options for this; here, installation with [conda](https://docs.conda.io/en/latest/) is shown.

```bash
conda create --name <name> python==3.11
conda activate <name>
pip install -r requirements_sentiment.txt  # For Sentiment Analysis
pip install -r requirements_qa.txt  # For PDF Document Q&A
```

## Deployment

For deployment, we suggest using Docker in combination with the provider that best suits the user's needs. Docker is a tool that allows for the creation of application containers, which are isolated runtime environments containing everything necessary to run an application. This allows the application to run in any environment, regardless of differences between the development and execution environments.

Using [Docker with Streamlit](https://docs.streamlit.io/knowledge-base/tutorials/deploy/docker) is straightforward. You need to create a Dockerfile, which you can find in this repository ([here](Dockerfile)). This file specifies the base image, which in this case is the official Streamlit image, and copies the application file to the container’s working directory. To build the image and run the container, use the following commands:

```bash
docker build -t st-sentiment .
docker run -p 8501:8501 st-sentiment
```

## Environment Setup

To set up the environment, you need to install the dependencies and configure pre-commit hooks. The pre-commit hooks ensure code quality and consistency by running various checks and formatters before each commit.

### Installing Dependencies

Install the dependencies specified in the requirements files:

```bash
pip install -r requirements_sentiment.txt  # For Sentiment Analysis
pip install -r requirements_qa.txt  # For PDF Document Q&A
```

### Configuring Pre-Commit Hooks

Install pre-commit and set up the hooks:

```bash
pip install pre-commit
pre-commit install
```

The pre-commit configuration is specified in the [.pre-commit-config.yaml](.pre-commit-config.yaml) file. It includes hooks for checking code formatting, linting, and other quality checks.

## Notes

- You need to specify the `OPENAI_API_KEY` environment variable, which is the OpenAI API key. This key can be obtained on the [OpenAI website](https://openai.com/).
