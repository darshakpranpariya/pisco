import codecs
import unittest

import numpy as np

from tests import number_of_empty_classes


def read_submission(filename):
    with codecs.open(filename, 'r', encoding='ISO-8859-1') as f:
        return f.read()


submission5 = read_submission('tests/resources/submission5.txt')
submission3 = read_submission('tests/resources/submission3.txt')
submission6 = read_submission('tests/resources/submission6.txt')
submission7 = read_submission('tests/resources/submission7.txt')


class NumberOfEmptyClassesTest(unittest.TestCase):
    def setUp(self):
        self.transformer = number_of_empty_classes
        self.submissions = [submission5, submission3, submission6, submission7]

    def test_feature_extraction(self):
        # returns the following counts:
        # 1) [[0], [1]] -> 0.5
        # 2) [[0, 0], [0]] -> 0
        # 3) [[0], [0]] -> 0
        # 4) [[0], [1], [0]] -> 0.33
        np.testing.assert_almost_equal(self.transformer.transform(self.submissions), [[0.5], [0], [0], [0.33]],
                                       decimal=2)

        if __name__ == '__main__':
            unittest.main()
