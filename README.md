# Project Description

In the police force, a textual description of a perpetrator is sent to the officers via the computers in their police cars. Often, the description is hidden in amongst the other information about the crime. It is difficult for the officers to quickly glance at the screen and get mental picture of the perpetrator.

The text is written by a human and is often transcribed from the 000 call; hence it is unstructured in nature. However, the description is short, direct, and much simpler than say the description of a character in a book. For example: “..... Desc: Caucasian Male, white shoes, blue jeans, black hoodie, brown backpack.".

The system reads the textual description and converts it into an image to reduce the cognitive load of the officers.

# Approach in Machine Learning

In modern language, there are many ways to describe a person; hardcoded matching rules might not be effective in classifying text. Therefore, a machine learning algorithm might be more robust as it learns the general rules from the dataset. The software used in machine learning is shown in following:

| Machine Learning | Development         | Deployment                                    |
| ---------------- | ------------------- | --------------------------------------------- |
| PyTorch          | Google Colaboratory | Flask, gunicorn, Docker, Google Cloud Service |

We udopt pretrained model, A Robustly Optimized BERT Pretraining Approach (roBERTa) [1].

1. Preprocessing the text
2. Feed into roBERTa
3. 1d covolution layer for classification, there are 13 appearance categories (top, acceccearies...etc) and categories has 35 classes (color, styles ..etc)

Flask python package is used to expose our machine learning model as a REST API. However, Flask is not a complete production-ready server. Hence, we will use gunicorn, a python HTTP server, to expose our REST API.

The model is delpoyed with docker and hosted in Google Cloud Service.

The following link is the API entry point:

https://mci-75aymfmqxq-km.a.run.app/predict?text="RP%20states%20male%20is%20out%20front%20of%20his%20address,%20throwing%20glass%20bottles%20at%20passing%20cars/pedestrians.%20Appears%20drug%20affected.%20Male%20described%20as%20cauc,%20wearing%20a%20grey%20hoodie,%20black%20track%20pants,%20addidas%20sneakers,%20red%20cap."

# Contributions:

1. model/TransformerAppearanceClassifier.py

   This is the architecture of the machine learning model, where I utilise the pre-trained model RoBERTa for text classification tasks.

2. utils.py

   This is the until script for the data-preprocessing, testing, training, validating and model initialisation.

3. train.py & test.py

   This is the training and testing script that with customized arguments:

   --input: Dataset Directory

   --dataset: Name of the dataset

   --epoch: Number of epochs

   --learning_rate: Learning rate

   --batch_size: Numbers of batches

   --train: is training required?

   --tensorboard: enable to log tensorboard

   --google_colab: enable to run on google colab

4. modelDriver.ipynb

   The main driver script to run the model.

5. Tdeployment/flask/

   Contain the flask web application, trained model, dependencies, configuration and Dockerfile for deployment.
