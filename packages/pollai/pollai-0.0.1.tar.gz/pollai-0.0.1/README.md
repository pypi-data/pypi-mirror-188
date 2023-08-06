PollAI is an implementation of how AI can be made easy for beginners

# Documentation for the PollAI module

Table of contents:
# Get Started with AI
- What is AI?
- Difference between Rule based models and Machine learning models
# RuleBased_Model class
- Functions
- Parameters
# ML_Model class
- Functions
- Parameters
- Exceptions
# Imperfections of AI
- How there are many imperfections in AI

# What are you waiting for? Let's get started!

## What is AI?
AI which stands for Artificial Intelligence, is a concept in which a computer can get near the intelligence of a human.
The term was first coined in 1956. Major milestones of AI include: The making of ELIZA (the first chatbot), IBM Deep Blue beating a
World Chess Champion, and Voice Assistants.

## Difference between rule based models and Machine Learning models
The difference between a rule based model and a Machine Learning model is very significant.
A rule based model is based on its training data and cannot learn. The only time the model learns is when its trained!
A machine learning model is based on its training data and can learn. It is significantly more accurate than a rule based model.
In terms of computational resources, a rule based model is more efficient than a Machine Learning model but a machine learning model is more accurate.

# RuleBased_Model class

## How to initialize the class:

from pollai import RuleBased_Model # Can also be *

model = RuleBased_Model(training_data) # params: self, training_data

## How to run the model

from pollai import RuleBased_Model

model = RuleBased_Model(training_data) # you should initialize the model first

model.run_model(text) # params: self, text

# ML_Model class:

## How to initialize the ML_Model class:

from pollai import ML_Model # Can also be * (which imports all classes and functions)

model = ML_Model(training_data) # params: self, training_data

## Training the model

from pollai import ML_Model # Can also be * (which imports all classes and functions)

model = ML_Model(training_data) # initialize the model first

model.train() # no params required. trains the model

## Running the model

from pollai import ML_Model # Can also be * (which imports all classes and functions)

model = ML_Model(training_data) # initialize the model first

model.train() # train the model first to avoid the TrainingException exception.

## Exceptions:
### TrainingException:
Exception when training is incomplete or not implemented at all.
The model needs to be trained to produce the expected accurate results.

# Imperfections in AI
Don't get me wrong, AI is amazing. However, it could use improvements. PollAI is imperfect too!
Machine learning, Rule based, any AI model has imperfections and can be improved.
For example, Machine Learning requires lots of computational resources and Rule based models are constantly inaccurate.