import numpy as np


# Создаем класс линейной регрессии CustomLinearReg
class CustomLinearReg:

    def __init__(self, lr=0.1, toller=0.01):
        self.lr = lr
        self.toller = toller
        self.weights = []
        self.score = [np.inf]

    def fit(self, X, y):
        X = np.concatenate((np.ones((X.shape[0], 1)), X), axis=1)
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        key = True
        while key:
            indexes = np.random.choice(n_features, int(0.5 * n_features), replace=False)
            predict = X.dot(self.weights)
            error = predict - y

            dw = 2 / n_samples * X[:, indexes].T.dot(error)
            self.weights[indexes] -= dw * self.lr
            self.score.append(self.r2(predict, y))

            if abs(self.score[-1]) <= self.toller:
                key = False
            elif abs(self.score[-1]) >= abs(self.score[-2]):
                self.weights = np.zeros(n_features)
                key = False

    def r2(self, predict, y):
        return 1 - np.sum((predict - y)**2) / (np.sum((y.mean() - y)**2) + 1e-15)

    def predict(self, X):
        X = np.concatenate((np.ones((X.shape[0], 1)), X), axis=1)
        return X.dot(self.weights)