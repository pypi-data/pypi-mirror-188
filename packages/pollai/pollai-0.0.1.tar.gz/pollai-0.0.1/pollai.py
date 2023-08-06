from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import markdown2

class RuleBased_Model:
    """POLLAI implementation of a Rule Based Model
    
    params: training_data (should be dict)
    For example:
    
    {
        "hello": ["hello", "whats up", "yo"]
    } # Running the model (if ran properly) should return the name of the example (we can call as bucket). in this case, the model should return "hello"

    """
    def __init__(self, training_data):
        self.training_data = training_data
        self.vectorizer = TfidfVectorizer()
        self.classifier = LogisticRegression()
        self.training_examples = []
        self.training_labels = []

        # Concatenate examples for each class into a single string
        for label, examples in self.training_data.items():
            self.training_examples.append(" ".join(examples))
            self.training_labels.append(label)

        self.tfidf_matrix = self.vectorizer.fit_transform(self.training_examples)
        self.classifier.fit(self.tfidf_matrix, self.training_labels)

    def run_model(self, text):
        """Runs the model based on the training data

        Params: text
        """
        text = [text]
        tfidf_matrix = self.vectorizer.transform(text)
        prediction = self.classifier.predict(tfidf_matrix)
        return prediction[0]

class ML_Model:
    """Machine learning model implemented with sklearn
    
    PollAI machine learning model implementation
    params: training_data: dict
    For example:
    
    {
        "hello": ["hello", "whats up", "yo"]
    } # Running the model (if ran properly) should return the name of the example (we can call as bucket), for this example, it should return "hello"

    """
    def __init__(self, training_data):
        self.training_data = training_data
        self.finished_training = False
        self.model = Pipeline([
            ('vectorizer', TfidfVectorizer()),
            ('classifier', LogisticRegression())
        ])
    
    def train(self):
        """Trains the model.
        
        Params: (no parameters required)
        
        Explanation: First, the function defines a local variables X and y.
        Then, the for loop iterates over items in the training data and extends the X and y list.
        Then it calls self.model.fit to train the model.
        
        P.S: This may take a few seconds to complete."""
        X = []
        y = []
        for label, examples in self.training_data.items():
            X.extend(examples)
            y.extend([label] * len(examples))
        self.model.fit(X, y)
        self.finished_training = True

    def finished_training_yet(self):
        return self.finished_training

    class TrainingException(Exception):
        def __init__(self, message="Model has not finished training or has not been trained yet. Error source: ML_Model"):
            self.message = message
        
        def __str__(self):
            return self.message
    
    def predict(self, text: str):
        """Predicts what text the model was given
        
        Params: text
        
        Explanation: For the prediction, first the function calls: self.model.predict with the parameters as a list.
        the list contains the text.
        Then, it returns the prediction with an index of 0 (the first item in the list) as a dict"""
        if self.finished_training:
            prediction = self.model.predict([text])
            return {
                "predicted_label": prediction[0]
            }
        else:
            raise self.TrainingException()

def documentation():
    with open("docs.md", "r") as docs:
        text = docs.read()
    text = markdown2.markdown(text)
    return text