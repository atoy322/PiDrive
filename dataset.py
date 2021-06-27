import joblib
import numpy as np



def load(filename):
    X, y = joblib.load(filename)
    X = np.array(X, dtype=np.float32)
    y = np.array(y, dtype=np.float32)

    X /= 255

    return X, y