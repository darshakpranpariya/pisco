#!/usr/bin/env python
from pisco.recognizers.linear_regression import linear_regression
import pisco.loaders.plain_loader as plain_loader
from pisco.transformers.unigram import unigram
from pisco.configuration import Configuration
from pisco.benchmarks.cv_benchmark import benchmark
import argparse
import logging


def config_argparser():
    argparser = argparse.ArgumentParser(description='Personality Recognition Evaluation')
    argparser.add_argument('-l', '--log-level', dest='log_level', type=str, default='INFO',
                           help='Set log level (DEBUG, INFO, ERROR)')

    argparser.add_argument('-c', '--train_corpus', dest='training_corpus', type=str, required=True,
                           help='Set name of the training corpus used for the evaluation: ' + pretty_list(
                               conf.get_dataset_names()))

    argparser.add_argument('-t', '--test_corpus', dest='test_corpus', type=str, required=False,
                           help='Set name of the test corpus used for the evaluation: ' + pretty_list(
                               conf.get_dataset_names()))

    argparser.add_argument('-r', '--recognizer', dest='recognizer_name', type=str, required=True,
                           help='Name of the invoked recognizer: ' + pretty_list(conf.get_recognizer_names()))

    argparser.add_argument('-f', '--features', dest='feature_names', type=str, required=True,
                           help='Name of the features: ' + pretty_list(conf.get_feature_names()))
    return argparser


def configure(conf):
    @conf.dataset('neuroticism', labels=['neuroticism'])
    @conf.dataset('extroversion', labels=['extroversion'])
    @conf.dataset('agreeableness', labels=['agreeableness'])
    @conf.dataset('openness', labels=['openness'])
    @conf.dataset('conscientiousness', labels=['conscientiousness'])
    def build_dataset(level=None, labels=[]):
        X, y = plain_loader.load(labels=labels)
        return X, y

    @conf.recognizer('linear_regression')
    def build_linear_regression():
        return linear_regression()

    @conf.feature('unigram')
    def build_feature():
        return [unigram()]


def pretty_list(items):
    return ', '.join([x for x in items])


if __name__ == '__main__':
    conf = Configuration()

    argparser = config_argparser()
    args = argparser.parse_args()

    LOGFMT = '%(asctime)s %(name)s %(levelname)s %(message)s'
    logging.basicConfig(level=getattr(logging, args.log_level), format=LOGFMT)

    configure(conf)

    X_train, y_train = conf.get_dataset(args.training_corpus)
    recognizer = conf.get_recognizer(args.recognizer_name)
    features = conf.get_feature(args.feature_names)

    benchmark(X_train, y_train, recognizer, features)
