from lime.lime_text import LimeTextExplainer  # Import LIME for explaining text classification models

def explain_sentiment(model, vectorizer, text):
    """
    Generate a LIME explanation for the sentiment prediction of a given text.
    
    Parameters:
        model: Trained text classification model with a predict_proba method.
        vectorizer: Text vectorizer (e.g., CountVectorizer, TfidfVectorizer) used to transform text.
        text (str): Input text whose sentiment prediction needs explanation.
        
    Returns:
        list of tuples: Each tuple contains a feature (word) and its contribution to the prediction,
                        sorted by importance. Positive values indicate support for the predicted class.
    """
    
    # Initialize LIME text explainer with class labels
    explainer = LimeTextExplainer(class_names=["Negative", "Positive"])
    
    # Explain the prediction for the input text
    exp = explainer.explain_instance(
        text,  # The text instance to explain
        lambda x: model.predict_proba(vectorizer.transform(x)),  # Function to get prediction probabilities
        num_features=5  # Number of top contributing features to display
    )
    
    # Return explanation as a list of (feature, impact) tuples
    return exp.as_list()