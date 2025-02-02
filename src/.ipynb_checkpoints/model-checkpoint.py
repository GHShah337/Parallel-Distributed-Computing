from sklearn.ensemble import RandomForestClassifier

def train_model(X_train, y_train):
    """
    Trains a RandomForestClassifier.
    Args:
        X_train (pandas.DataFrame): Training features.
        y_train (pandas.Series): Training labels.
    Returns:
        RandomForestClassifier: Trained model.
    """
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    return model
