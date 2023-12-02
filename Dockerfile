from sklearn.model_selection import train_test_split

def split_train_dev_test(X, y, test_size, dev_size):
    # Split into train+dev and test sets first
    X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=test_size)

    # Compute actual dev size relative to the combined train+dev set
    actual_dev_size = dev_size / (1 - test_size)
    
    # Split the train+dev set into separate training and dev sets
    X_train, X_dev, y_train, y_dev = train_test_split(X_temp, y_temp, test_size=actual_dev_size)

    return X_train, X_dev, X_test, y_train, y_dev, y_test
