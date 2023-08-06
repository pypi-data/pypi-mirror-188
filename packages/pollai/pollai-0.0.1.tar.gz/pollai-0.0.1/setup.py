from setuptools import setup, find_packages

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Education",
    "Operating System :: OS Independent",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3"
]

setup(
    name="pollai",
    version="0.0.1",
    description="AI models simplified and implemented",
    long_description="""
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
For example, Machine Learning requires lots of computational resources and Rule based models are constantly inaccurate.""",
    long_description_content_type='text/markdown',
    url="",
    author="ByteVolx",
    author_email="onions193@gmail.com",
    license="MIT",
    classifiers=classifiers,
    keywords='ai',
    packages=find_packages(),
    install_requires=["numpy", "scikit-learn"]
)