import pisco.transformers.structure.number_of_methods_per_class as number_of_methods_per_class  # noqa
import pisco.transformers.structure.ratio_of_external_libraries as ratio_of_external_libraries  # noqa
import pisco.transformers.style.length_of_methods_per_class as length_of_methods_per_class  # noqa
import pisco.transformers.style.number_of_comments_per_class as number_of_comments_per_class  # noqa
import pisco.transformers.structure.number_of_function_parameters_per_class as number_of_function_parameters_per_class  # noqa
import pisco.transformers.structure.function_name_length as function_name_length  # noqa
import pisco.transformers.structure.function_parameter_name_length as function_parameter_name_length  # noqa
import pisco.transformers.structure.number_of_empty_classes as number_of_empty_classes  # noqa
import pisco.transformers.structure.number_of_fields_per_class as number_of_fields_per_class  # noqa
import pisco.transformers.structure.length_of_field_names as length_of_field_names  # noqa
import pisco.transformers.structure.cyclomatic_complexity as cyclomatic_complexity  # noqa
import pisco.transformers.structure.number_of_local_variables_in_functions as number_of_local_variables_in_functions  # noqa
import pisco.transformers.structure.duplicate_code_measure as duplicate_code_measure  # noqa
import pisco.transformers.structure.length_of_local_variable_names_in_functions as length_of_local_variable_names_in_functions  # noqa
import pisco.transformers.structure.number_of_classes_per_section as number_of_classes_per_section  # noqa
import pisco.transformers.structure.comment_length as comment_length  # noqa
import pisco.transformers.structure.contains_suppress_warnings as contains_suppress_warnings  # noqa
import pisco.transformers.misc.ratio_of_unparsable_sections as ratio_of_unparsable_sections  # noqa
import pisco.transformers.misc.contains_IDE_template_text as contains_IDE_template_text  # noqa
import pisco.recognizers.linear_regression as linear_regression
import pisco.recognizers.nearest_neighbor as nearest_neighbor
from pisco.pipeline.pipeline import pipeline
from pisco.loaders.plain_loader import load
from collections import OrderedDict
import json
import csv


TRANSFORMERS = {'number_of_methods_per_class': number_of_methods_per_class,
                'length_of_methods_per_class': length_of_methods_per_class,
                'number_of_comments_per_class': number_of_comments_per_class,
                'ratio_of_external_libraries': ratio_of_external_libraries,
                'number_of_function_parameters_per_class': number_of_function_parameters_per_class,  # noqa
                'function_parameter_name_length': function_parameter_name_length,  # noqa
                'function_name_length': function_name_length,
                'number_of_empty_classes': number_of_empty_classes,
                'ratio_of_unparsable_sections': ratio_of_unparsable_sections,
                'contains_IDE_template_text': contains_IDE_template_text,
                'number_of_fields_per_class': number_of_fields_per_class,
                'length_of_field_names': length_of_field_names,
                'number_of_local_variables_in_functions': number_of_local_variables_in_functions,  # noqa
                'length_of_local_variable_names_in_functions': length_of_local_variable_names_in_functions,  # noqa
                'duplicate_code_measure': duplicate_code_measure,
                'comment_length': comment_length,
                'number_of_classes_per_section': number_of_classes_per_section,
                'cyclomatic_complexity': cyclomatic_complexity}

RECOGNIZERS = {'Linear Regression': linear_regression,
               'Nearest Neighbor': nearest_neighbor}


def build_recognizer(params_file):
    nfeatures = num_features(params_file)
    recognizer_params = {}
    with open(params_file) as data_file:
        data = json.load(data_file)
        best_params = data[str(nfeatures)+'features']['best_params']
        recognizer_name = data['recognizer_name']
        for k, v in best_params.iteritems():
            splits = k.split('__')
            if splits[0] == 'recognizer':
                if v == u'default':
                    recognizer_params = {}
                else:
                    param_name = splits[2]
                    if param_name not in recognizer_params:
                        recognizer_params = {}
                    recognizer_params[str(param_name)] = v
        return RECOGNIZERS[recognizer_name].build(**recognizer_params)


def build_features(params_file):
    nfeatures = num_features(params_file)
    features = {}
    with open(params_file) as data_file:
        data = json.load(data_file)
        best_params = data[str(nfeatures)+'features']['best_params']
        for k, v in best_params.iteritems():
            splits = k.split('__')
            if splits[0] == 'union':
                transformer_name = splits[1]
                if v == u'default':
                    features[transformer_name] = {}
                else:
                    param_name = splits[3]
                    if transformer_name not in features:
                        features[transformer_name] = {}
                    features[transformer_name][str(param_name)] = str(v)
    feature_instances = []
    for k, v in features.iteritems():
        if not v:
            feature_instances.append(TRANSFORMERS[k].build(**v))
        else:
            feature_instances.append(TRANSFORMERS[k].build())
    return feature_instances


def num_features(configfile):
    with open(configfile) as data_file:
        data = json.load(data_file)
        return int(data.keys()[0].replace("features", ""))


def predict(configs):
    predictions = OrderedDict()
    for dimension, configfile in configs.iteritems():
        X_train, Y_train = load(labels=[dimension])
        features = build_features(configs[dimension])
        recognizer = build_recognizer(configs[dimension])
        nfeatures = num_features(configs[dimension])
        p = pipeline(transformers=features,
                     recognizer=recognizer,
                     number_of_features=nfeatures)
        p.fit(X_train, Y_train)
        X_test, ids = load(corpus_path='data/test', labels=dimension,
                           truth_file=None, return_ids=True)
        Y_pred = p.predict(X_test)
        for y_pred, _id in zip(Y_pred, ids):
            if not predictions.get(_id, None):
                predictions[_id] = OrderedDict()
            predictions[_id][dimension] = y_pred
    return predictions


def write_predictions(predictions, filepath):
    with open(filepath, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        header = ['id'] + predictions[predictions.keys()[0]].keys()
        writer.writerow(header)
        for _id, values in predictions.iteritems():
            ps = []
            for dimension, value in values.iteritems():
                ps.append(values[dimension])
            writer.writerow([_id] + ps)
