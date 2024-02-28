import numpy as np

# Создаем класс линейной регрессии CustomLinearReg
# Для данных небольшого размера будем пользоваться аналитическим расчетом коэффициентов
class CustomLinearReg:
    # создаем конструктор класса
    def __init__(self):
        self.w = [[]]
    # создаем метод обучения fit
    def fit(self, X, y):
        X = np.insert(np.array(X), 0, 1, axis=1)
        y = np.array(y).reshape(-1, 1)
        # вычисляем коэффициенты линейной регрессии
        self.w = np.linalg.inv(X.T.dot(X)).dot(X.T).dot(y)

    # создаем метод предсказания predict
    def predict(self, X):
        # подставим в ур-е линейной регрессии коэффициенты и массив на основе которого сделаем предсказание
        Y_model = self.w[1][0]*np.array(X).reshape(-1) + self.w[0][0]
        return Y_model

#  Для обучения большого коли-ва данных для подбора коэфф будем использовать градиентный спуск
class GradientLinearReg:

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

            if len(self.score) > n_features and self.score[-1] <= self.toller:
                key = False
            elif abs(self.score[-1]) >= abs(self.score[-2]):
                self.weights = np.zeros(n_features)
                key = False

    def r2(self, predict, y):
        return 1 - np.sum((predict - y)**2) / (np.sum((y.mean() - y)**2) + 1e-15)

    def predict(self, X):
        X = np.concatenate((np.ones((X.shape[0], 1)), X), axis=1)
        return X.dot(self.weights)
