from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline


def ngram_ranges(begin, end):
    ngram_range = []
    for b in range(begin, end + 1):
        for e in range(b, end + 1):
            ngram_range.append((b, e))
    return ngram_range


def param_grid():
    return {'union__unigram__vec__ngram_range': ngram_ranges(1, 10)}


def build():
    pipeline = Pipeline([('vec', CountVectorizer(ngram_range=(4, 5)))])
    return ('unigram', pipeline)
