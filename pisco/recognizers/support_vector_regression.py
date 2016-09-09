from sklearn.svm import SVR
from sklearn.pipeline import Pipeline


def param_grid():
    return {'recognizer__support_vector_regression__C': [1e-3, 1e-2, 1e-1, 1, 1e1, 1e2, 1e3],
            'recognizer__support_vector_regression__kernel': ['rbf', 'linear', 'poly', 'sigmoid'],
            'recognizer__support_vector_regression__degree': [2, 3, 4, 5],
            'recognizer__support_vector_regression__epsilon': [1e-3, 1e-2, 1e-1],
            'recognizer__support_vector_regression__gamma': ['auto', 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1, 10]}


def build():
    pipeline = Pipeline([(
        'support_vector_regression',
        SVR(C=1e-1, cache_size=200, coef0=0.0, degree=3, epsilon=1e-1, gamma='auto', kernel='rbf', max_iter=-1, shrinking=True, tol=0.001, verbose=False))])
    return ('recognizer', pipeline)