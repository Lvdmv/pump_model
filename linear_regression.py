import numpy as np


class CustomLinearReg:
    """
    Класс линейной регрессии CustomLinearReg
    Для данных небольшого размера будем пользоваться аналитическим расчетом коэффициентов

    """
    def __init__(self):
        self.w = [[]]  # Инициализируем веса коэффициентов

    # создаем метод обучения fit
    def fit(self, X, y):
        """
        Обучает модель линейной регрессии

        Parameters
        ----------
        X: np.array, shape(n_samples, n_features)
            Входные признаки
        y: np.array, shape(n_samples, n_features)
            Целевая переменная

        Return
        ----------
        self : объект
        """
        X = np.insert(np.array(X), 0, 1, axis=1)
        y = np.array(y).reshape(-1, 1)
        self.w = np.linalg.inv(X.T.dot(X)).dot(X.T).dot(y)  # вычисляем коэффициенты линейной регрессии
        return self

    # создаем метод предсказания predict
    def predict(self, X):
        """
        Производит предсказания на основе входных данных X

        Parameters
        ----------
        X: np.array, shape(n_samples, n_features)
            Входные признаки

        Return
        ----------
        Y_model : np.array, shape(n_samples, )
        """
        # подставим в ур-е линейной регрессии коэффициенты и массив на основе которого сделаем предсказание
        Y_model = self.w[1][0]*np.array(X).reshape(-1) + self.w[0][0]
        return Y_model


#  Для обучения большого коли-ва данных для подбора коэфф будем использовать градиентный спуск
class GradientLinearReg:
    def __init__(self, lr=0.1, toller=0.01):
        """
        Инициализация модели линейной регрессии методом градиентного спуска.

        Parameters:
        lr : float, по умолчанию 0.1
            Скорость обучения (learning rate)
        toller : float, по умолчанию 0.01
            Пороговое значение для критерия остановки обучения
        """
        self.lr = lr
        self.toller = toller
        self.weights = []  # Веса модели
        self.score = [np.inf]  # Метрика качества модели

    def fit(self, X, y):
        """
        Обучение модели линейной регрессии методом градиентного спуска.

        Parameters:
        X : np.array, shape (n_samples, n_features)
            Входные признаки
        y : np.array, shape (n_samples,)
            Целевая переменная
        """
        X = np.concatenate((np.ones((X.shape[0], 1)), X), axis=1)  # Добавление столбца из единиц в X
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)  # Инициализация весов нулями
        key = True
        while key:
            indexes = np.random.choice(n_features, int(0.5 * n_features), replace=False)  # Случайный выбор индексов
            predict = X.dot(self.weights)  # Предсказание
            error = predict - y  # Расчет ошибки

            dw = 2 / n_samples * X[:, indexes].T.dot(error)  # Градиент
            self.weights[indexes] -= dw * self.lr  # Обновление весов

            self.score.append(self.r2(predict, y))  # Расчет метрики качества

            if len(self.score) > n_features and self.score[-1] <= self.toller:
                key = False  # Проверка критерия остановки
            elif abs(self.score[-1]) >= abs(self.score[-2]):
                self.weights = np.zeros(n_features)  # Обнуление весов в случае ухудшения метрики
                key = False

    def r2(self, predict, y):
        """
        Рассчитывает коэффициент детерминации модели.

        Parameters:
        predict : np.array
            Предсказанные значения
        y : np.array
            Фактические значения

        Return:
        r2 : float
            Коэффициент детерминации модели
        """
        return 1 - np.sum((predict - y) ** 2) / (np.sum((y.mean() - y) ** 2) + 1e-15)

    def predict(self, X):
        """
        Производит предсказания на основе входных данных X.

        Parameters:
        X : np.array, shape (n_samples, n_features)
            Входные признаки

        Return:
        y : np.array, shape (n_samples,)
            Предсказанные значения
        """
        X = np.concatenate((np.ones((X.shape[0], 1)), X), axis=1)  # Добавление столбца из единиц в X
        return X.dot(self.weights)  # Предсказание
