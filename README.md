# Streamlit Course

## Introduction

This repository contains the code for the applications developed in the Streamlit course. There are three applications, which can be found at the following paths:

- [MNIST Analysis](mnist_analisis.py): Application that allows analysis of the [MNIST dataset](https://en.wikipedia.org/wiki/MNIST_database). It loads the test set of the MNIST dataset, allowing users to explore the images and their labels. Additionally, images can be filtered by label, and the pixel value distributions are shown divided by label.
- [MNIST Prediction](mnist_prediccion.py): Application that allows users to draw on a canvas and predict the number they have drawn. This uses a pre-trained MNIST image classification model.
- [PDF Document Q&A](qa.py): Application that allows users to upload a PDF document and ask questions about it. This uses the OpenAI API, which allows for text-based questions. In this case, the text is the content of the PDF document. The [PyPDF](https://pypi.org/project/pypdf/) library is used to extract text from the PDF. The [Sentence Transformers](https://www.sbert.net/) library is used to generate embeddings for both the PDF content and the questions. This library generates embeddings for phrases, which are used to calculate similarity between questions and answers. Finally, the [ChromaDB](https://www.trychroma.com/) library is used to store embeddings and search for answers.

## Execution

To run the different applications, execute the following command:

```bash
streamlit run <application_path>
```

### Requirements

To run the applications, you must install the dependencies specified in the [requirements.txt](requirements.txt) file. The Python version used is `3.9`. It's recommended to use a virtual environment for installing the necessary packages. There are several options for this; here, installation with [conda](https://docs.conda.io/en/latest/) is shown.

```bash
conda create --name <name> python==3.9
conda activate <name>
pip install -r requirements.txt
```


## Deployment

For deployment, we suggest using Docker in combination with the provider that best suits the user's needs. Docker is a tool that allows for the creation of application containers, which are isolated runtime environments containing everything necessary to run an application. This allows the application to run in any environment, regardless of differences between the development and execution environments.

Using [Docker with Streamlit](https://docs.streamlit.io/knowledge-base/tutorials/deploy/docker) is straightforward. You need to create a Dockerfile, which you can find in this repository ([here](Dockerfile)). This file specifies the base image, which in this case is the official Streamlit image, and copies the application file to the container’s working directory. To build the image and run the container, use the following commands:

```bash
docker build -t st-sentiment .
docker run -p 8501:8501 st-sentiment
```

Note that you need to specify the OPENAI_API_KEY environment variable, which is the OpenAI API key. This key can be obtained on the [OpenAI website](https://openai.com/).

# To-Dos

- [x] Check sentiment analysis app: App and Requirements
- [ ] Check QA app: App and Requirements
- [x] Check Deployment - Docker
- [ ] Environment setup: `requirements.txt` and pre-commit hooks explained