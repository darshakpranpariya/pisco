from pisco.transformers.helpers import extract_sections, get_stat_function
from sklearn.base import BaseEstimator
import pisco.knife.adapters as adapter
from sklearn.pipeline import Pipeline
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import types


def patch(pipeline):
    def get_feature_names(pipeline):
        return ["length_of_local_variable_names_in_methods"]
    pipeline.get_feature_names = types.MethodType(get_feature_names, pipeline)


def build(stat='mean'):
    pipeline = Pipeline([('transformer',
                          LengthOfLocalVariableNamesInMethods(stat=stat)),
                         ('min_max_scaler', MinMaxScaler())])
    patch(pipeline)
    return ('length_of_local_variable_names_in_methods', pipeline)


def param_grid():
    return {'union__length_of_local_variable_names_in_methods__transformer__stat':
            ['mean', 'variance', 'range']}


class LengthOfLocalVariableNamesInMethods(BaseEstimator):
    def __init__(self, stat='mean'):
        self.stat = stat

    def fit(self, submissions, y):
        return self

    def transform(self, raw_submissions):
        return map(lambda x: self._transform(x), raw_submissions)

    def _transform(self, raw_submission):
        stat = get_stat_function(self.stat)
        sections = extract_sections(raw_submission)
        section_stats = map(lambda x: self.__transform(x),
                            sections)
        stats = map(lambda x: stat(x), section_stats)
        a = [np.mean(stats)]
        return a

    def __transform(self, section):
        methods = adapter.methods(section)
        if methods:
            ret_val = []
            for clazz in methods:
                if clazz:
                    for method in clazz:
                        for variable_name in method['variables']:
                            ret_val.append(len(variable_name))
            if not ret_val:
                ret_val = [0]
            return ret_val

        else:
            return [0]
