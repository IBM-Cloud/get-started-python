
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from joblib import dump
solvers = ['liblinear', 'newton-cg', 'lbfgs', 'sag', 'saga']
for solver in solvers:
    model = LogisticRegression(solver=solver)
    model.fit(X_train, y_train)
    
    # Evaluate the model
    predictions = model.predict(X_test)
    report = classification_report(y_test, predictions)
    print(f"Performance with solver {solver}:\n{report}")
    
    # Save the model
    model_filename = f"{roll_no}_lr_{solver}.joblib"
    dump(model, model_filename)


