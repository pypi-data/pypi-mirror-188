# Documentation
Documentation for the PollAI library

# Changelogs
0.0.1 (First Release)
==============
- First Release
- Rule based model class and ML model class implementation
0.0.2
=========
- Fix pip bug

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
TrainingException:
Exception when training is incomplete or not implemented at all. The model needs to be trained to produce the expected accurate results.

# Imperfections in AI
Don't get me wrong, AI is amazing. However, it could use improvements. PollAI is imperfect too! Machine learning, Rule based, any AI model has imperfections and can be improved. For example, Machine Learning requires lots of computational resources and Rule based models are constantly inaccurate.