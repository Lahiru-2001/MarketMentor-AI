from lime.lime_text import LimeTextExplainer

def explain_sentiment(model, vectorizer, text):
    explainer = LimeTextExplainer(class_names=["Negative", "Positive"])
    exp = explainer.explain_instance(
        text,
        lambda x: model.predict_proba(vectorizer.transform(x)),
        num_features=5
    )
    return exp.as_list()
