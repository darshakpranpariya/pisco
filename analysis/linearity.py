import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt
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
from pisco.transformers.helpers import extract_sections
from pisco.knife.adapters import classes
import pisco.transformers.misc.word_unigram as word_unigram  # noqa
from pisco.loaders.plain_loader import load

DIMENSION = ['openness']
FEATURES = [
    ('Number of Methods per Class', number_of_methods_per_class),
    ('Length of Methods per Class', length_of_methods_per_class),
    ('Number of Comments per Class', number_of_comments_per_class),
    ('Ration of External Library Usage', ratio_of_external_libraries),
    ('Number of function parameters per class', number_of_function_parameters_per_class),  # noqa
    ('Length of function parameter names', function_parameter_name_length),
    ('Length of Function names (1-dimensional)', function_name_length),
    ('Number of empty classes (1-dimensional)', number_of_empty_classes),
    ('Ratio of unparsable sections', ratio_of_unparsable_sections),
    ('Contains IDE template text (binary)', contains_IDE_template_text),
    ('Number of fields per class', number_of_fields_per_class),
    ('Length of field names', length_of_field_names),
    ('Number of local variables in functions', number_of_local_variables_in_functions),  # noqa
    ('Length of local variable names in functions', length_of_local_variable_names_in_functions),  # noqa
    ('Duplicate Code Measure', duplicate_code_measure),
    ('Comment Length', comment_length),
    ('Number of Classes per Section', number_of_classes_per_section),
    ('Cyclomatic Complexity', cyclomatic_complexity)
]

X, Y = load(labels=DIMENSION)
for x in X:
    sections = extract_sections(x)
    for section in sections:
        classes(section)

Y = [[y] for y in Y]

result = {}
result['recognizers'] = []
for f in FEATURES:
    print "Feature: {}".format(f[0])
    transformer = f[1].build()[1]
    fv = transformer.transform(X)
    results = sm.OLS(Y, sm.add_constant(fv)).fit()
    print results.summary()
    if len(fv[0]) > 1:
        continue
    plt.scatter(fv, Y)
    fv = [y for x in fv for y in x]
    X_plot = np.linspace(min(fv), max(fv), 100)
    plt.plot(X_plot, X_plot*results.params[1] + results.params[0])
    plt.title(f[0] + '{}'.format(DIMENSION))

    plt.show()