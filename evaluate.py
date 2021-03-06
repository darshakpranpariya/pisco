#!/usr/bin/env python
import argparse
import logging

import pisco.loaders.plain_loader as plain_loader
import pisco.recognizers.linear_regression as linear_regression
import pisco.recognizers.nearest_neighbors_regressor as nearest_neighbors_regressor
import pisco.transformers.misc.contains_IDE_template_text as contains_IDE_template_text  # noqa
import pisco.transformers.misc.number_of_empty_classes as number_of_empty_classes  # noqa
import pisco.transformers.misc.ratio_of_unparsable_sections as ratio_of_unparsable_sections  # noqa
import pisco.transformers.structure.cyclomatic_complexity as cyclomatic_complexity  # noqa
import pisco.transformers.structure.duplicate_code_measure as duplicate_code_measure  # noqa
import pisco.transformers.structure.length_of_methods as length_of_methods  # noqa
import pisco.transformers.structure.number_of_classes as number_of_classes  # noqa
import pisco.transformers.structure.number_of_fields as number_of_fields  # noqa
import pisco.transformers.structure.number_of_local_variables_in_methods as number_of_local_variables_in_methods  # noqa
import pisco.transformers.structure.number_of_method_parameters as number_of_method_parameters  # noqa
import pisco.transformers.structure.number_of_methods as number_of_methods  # noqa
import pisco.transformers.structure.ratio_of_external_libraries as ratio_of_external_libraries  # noqa
import pisco.transformers.style.length_of_field_names as length_of_field_names  # noqa
import pisco.transformers.style.length_of_local_variable_names_in_methods as length_of_local_variable_names_in_methods  # noqa
import pisco.transformers.style.length_of_method_names as length_of_method_names  # noqa
import pisco.transformers.style.length_of_method_parameter_names as length_of_method_parameter_names  # noqa
from pisco.benchmarks.cv_benchmark import benchmark
from pisco.configuration import Configuration


def config_argparser():
    argparser = argparse.ArgumentParser(
        description='Personality Recognition Evaluation'
    )
    argparser.add_argument('-l', '--log-level', dest='log_level',
                           type=str, default='INFO',
                           help='Set log level (DEBUG, INFO, ERROR)')

    argparser.add_argument('-c', '--train_corpus', dest='training_corpus',
                           type=str, required=True,
                           help='Set name of the training corpus: ' +
                           pretty_list(conf.get_dataset_names()))

    argparser.add_argument('-t', '--test_corpus', dest='test_corpus',
                           type=str, required=False,
                           help='Set name of the test corpus: ' +
                           pretty_list(conf.get_dataset_names()))

    argparser.add_argument('-r', '--recognizer', dest='recognizer_name',
                           type=str, required=True,
                           help='Name of the invoked recognizer: ' +
                           pretty_list(conf.get_recognizer_names()))

    argparser.add_argument('-f', '--features', dest='feature_names',
                           type=str, required=True,
                           help='Name of the features: ' +
                           pretty_list(conf.get_feature_names()))
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
        return linear_regression.build()

    @conf.recognizer('nearest_neighbors_regressor')
    def build_nearest_neighbors_regressor():
        return nearest_neighbors_regressor.build()

    @conf.feature('mean_number_of_methods')
    def build_mean_number_of_methods_feature():
        return [number_of_methods.build(stat='mean')]

    @conf.feature('cyclomatic_complexity')
    def build_cylomatic_complexity_feature_feature():
        return [cyclomatic_complexity.build(stat='mean')]

    @conf.feature('mean_number_of_method_parameters')
    def build_mean_number_of_method_parameters():
        return [number_of_method_parameters.build(stat='mean')]

    @conf.feature('mean_length_of_method_parameter_names')
    def build_mean_length_of_method_parameter_names():
        return [length_of_method_parameter_names.build(stat='mean')]

    @conf.feature('mean_length_of_method_names')
    def build_mean_length_of_method_names():
        return [length_of_method_names.build(stat='mean')]

    @conf.feature('mean_number_of_fields')
    def build_mean_number_of_fields():
        return [number_of_fields.build(stat='mean')]

    @conf.feature('mean_length_of_field_names')
    def build_mean_length_of_field_names():
        return [length_of_field_names.build(stat='mean')]

    @conf.feature('mean_number_of_local_variables_in_methods')
    def build_mean_number_of_local_variables_in_methods():
        return [number_of_local_variables_in_methods.build(stat='mean')]

    @conf.feature('mean_number_of_classes')
    def build_mean_number_of_classes():
        return [number_of_classes.build(stat='mean')]

    @conf.feature('mean_length_of_local_variable_names_in_methods')
    def build_mean_length_of_local_variable_names_in_methods():
        return [length_of_local_variable_names_in_methods.build(stat='mean')]

    @conf.feature('mean_number_of_empty_classes')
    def build_mean_number_of_empty_classes():
        return [number_of_empty_classes.build(stat='mean')]

    @conf.feature('mean_length_of_methods')
    def build_mean_length_of_methods_feature():
        return [length_of_methods.build()]

    @conf.feature('ratio_of_unparsable_sections')
    def build_ratio_of_unparsable_sections():
        return [ratio_of_unparsable_sections.build()]

    @conf.feature('contains_IDE_template_text')
    def build_contains_IDE_template_text():
        return [contains_IDE_template_text.build()]

    @conf.feature('ratio_of_external_libraries')
    def build_ratio_of_external_libraries_feature():
        return [ratio_of_external_libraries.build()]

    @conf.feature('duplicate_code_measure')
    def build_duplicate_code_measure_feature():
        return [duplicate_code_measure.build()]

    @conf.feature('all')
    def build_all_features():
        return [number_of_methods.build(),
                length_of_methods.build(),
                ratio_of_external_libraries.build(),
                number_of_method_parameters.build(),
                length_of_method_parameter_names.build(),
                length_of_method_names.build(),
                number_of_empty_classes.build(),
                ratio_of_unparsable_sections.build(),
                contains_IDE_template_text.build(),
                number_of_fields.build(),
                length_of_field_names.build(),
                number_of_local_variables_in_methods.build(),
                length_of_local_variable_names_in_methods.build(),
                duplicate_code_measure.build(),
                number_of_classes.build(),
                cyclomatic_complexity.build()]


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
