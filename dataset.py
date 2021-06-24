import joblib
import numpy as np



def load(filename):
    X, y = joblib.load(filename)
    X = np.array(X, dtype=np.float32)
    y = np.array(y, dtype=np.float32)

    X /= X.max()

    return X, y