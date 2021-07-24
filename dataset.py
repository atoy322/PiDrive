import joblib
import numpy as np



def load(filename, scale01=True):
    X, y = joblib.load(filename)
    X = np.array(X, dtype=np.float32)
    y = np.array(y, dtype=np.float32)

    if scale01:
        X /= 255

    return X, y