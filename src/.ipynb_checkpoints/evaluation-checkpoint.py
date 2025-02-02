from sklearn.metrics import classification_report

def evaluate_model(model, X_test, y_test):
    """
    Evaluates a model and generates a classification report.
    Args:
        model: Trained model.
        X_test (pandas.DataFrame): Test features.
        y_test (pandas.Series): Test labels.
    Returns:
        str: Classification report.
    """
    predictions = model.predict(X_test)
    return classification_report(y_test, predictions)
