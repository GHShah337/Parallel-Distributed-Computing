from src.data_loader import load_data
from src.preprocessing import split_data

def test_split_data():
    """
    Tests data splitting into training and test sets.
    """
    data = load_data()
    X_train, X_test, y_train, y_test = split_data(data)
    assert len(X_train) > 0, "Training data should not be empty"
    assert len(X_test) > 0, "Test data should not be empty"
