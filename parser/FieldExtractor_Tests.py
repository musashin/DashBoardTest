import unittest
import datetime
from . import FieldExtractor


class FieldExtractorNormal(unittest.TestCase):
    """
    Test in normal conditions
    """

    def setUp(self):

        self.extractor = FieldExtractor.FieldExtractor({'top': {'sheet': 'toto',
                                                                'field': 'top',
                                                                'offset': FieldExtractor.FieldOffset.TOP},
                                                        'bottom': {'sheet': 'toto',
                                                                    'field': 'bottom',
                                                                    'offset': FieldExtractor.FieldOffset.BOTTOM},
                                                        'default': {'sheet': 'toto',
                                                                    'field': 'default'},
                                                        'right': { 'sheet': 'tata',
                                                                    'field': 'right',
                                                                    'offset': FieldExtractor.FieldOffset.RIGHT},
                                                        'left': {'sheet': 'tata',
                                                                'field': 'left',
                                                                'offset': FieldExtractor.FieldOffset.LEFT},
                                                        'Not found': {'sheet': 'toto',
                                                                   'field': 'nothere',
                                                                   'offset': FieldExtractor.FieldOffset.BOTTOM},
                                                        'Date': {'sheet': 'toto',
                                                                 'field': 'date',
                                                                  'type': FieldExtractor.FieldType.DATE
                                                                  }
                                                        })

    def test_default_field_location(self):

        result = self.extractor.extract(r'./parser/test_data/sample1.xlsx')

        self.assertEqual(result['default'], 89)

    def test_top_field_location(self):
            result = self.extractor.extract(r'./parser/test_data/sample1.xlsx')

            self.assertEqual(result['top'], 78)

    def test_bottom_field_location(self):
            result = self.extractor.extract(r'./parser/test_data/sample1.xlsx')

            print(result)
            self.assertEqual(result['bottom'], 12)

    def test_right_field_location(self):
        result = self.extractor.extract(r'./parser/test_data/sample1.xlsx')

        self.assertEqual(result['right'], 45)

    def test_left_field_location(self):
            result = self.extractor.extract(r'./parser/test_data/sample1.xlsx')

            self.assertEqual(result['left'], 56)

    def test_notfound_field(self):
        result = self.extractor.extract(r'./parser/test_data/sample1.xlsx')

        self.assertEqual(result['nothere'], None)

    def test_date_field(self):
        result = self.extractor.extract(r'./parser/test_data/sample1.xlsx')

        self.assertEqual(result['date'], datetime.datetime(2018, 1, 4, 0, 0))


if __name__ == '__main__':
    unittest.main()