from ..helpers import extract_sections, get_stat_function, tokenize
from sklearn.base import BaseEstimator
import pisco.knife.adapters as adapter
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
import types


def patch(pipeline):
    def get_feature_names(pipeline):
        return ["cyclomatic_complexity"]
    pipeline.get_feature_names = types.MethodType(get_feature_names, pipeline)


def build(stat='mean'):
    transformer = CyclomaticComplexity(stat=stat)
    pipeline = Pipeline([('transformer', transformer),
                         ('min_max_scaler', MinMaxScaler())])
    patch(pipeline)
    return ('cyclomatic_complexity', pipeline)


def param_grid():
    return {'union__cyclomatic_complexity__transformer__stat':
            ['mean']}


class CyclomaticComplexity(BaseEstimator):
    def __init__(self, stat='mean'):
        self.stat = stat

    def fit(self, submissions, y):
        return self

    def transform(self, raw_submissions):
        return map(lambda x: self._transform(x), raw_submissions)

    def _transform(self, raw_submission):
        stat = get_stat_function(self.stat)
        sections = extract_sections(raw_submission)
        complexities = map(lambda x: self.__transform(x), sections)
        complexities = [y for x in complexities for y in x]
        return [stat(complexities)]

    def __transform(self, section):
        methods = adapter.methods(section)
        if methods:
            complexities = []
            for ms in methods:
                complexities.extend(map(lambda m:
                                        cyclomatic_complexity(m['codeBlock']),
                                        ms))
            return complexities
        else:
            return [0]


def cyclomatic_complexity(method):
    complexity = 1
    keywords = ["if", "else", "while", "case", "for", "switch", "do",
                "continue", "break", "&&", "||", "?", ":", "catch", "finally",
                "throw", "throws", "default", "return"]
    for token in tokenize(method):
        if token in keywords:
            complexity += 1
    return complexity
