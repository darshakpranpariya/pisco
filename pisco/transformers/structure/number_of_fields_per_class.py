from ..helpers import extract_sections, get_stat_function
from sklearn.base import BaseEstimator
import pisco.knife.adapters as adapter
from sklearn.pipeline import Pipeline
import numpy as np


def build(stat='variance'):
    pipeline = Pipeline([('transformer',
                          NumberOfFieldsPerClass(stat=stat))])
    return ('number_of_fields_per_class', pipeline)


def param_grid():
    return {'union__number_of_fields_per_class__transformer__stat':
            ['mean', 'variance', 'range']}


class NumberOfFieldsPerClass(BaseEstimator):
    def __init__(self, stat='mean'):
        self.stat = stat

    def fit(self, submissions, y):
        return self

    def transform(self, raw_submissions):
        return map(lambda x: self._transform(x), raw_submissions)

    def _transform(self, raw_submission):
        stat = get_stat_function(self.stat)
        sections = extract_sections(raw_submission)
        clazz_stats = map(lambda x: self.__transform(x),
                          sections)
        return [np.mean(map(lambda x: stat(x), clazz_stats))]

    def __transform(self, section):
        clazzes = adapter.classes(section)
        if clazzes:
            ret_val = []
            for clazz in clazzes:
                ret_val.append(len(clazz['fields']))
            return ret_val
        else:
            return [0]
