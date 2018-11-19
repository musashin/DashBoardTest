from . import FieldExtractor


class Invoice(FieldExtractor.FieldExtractor):
    """
    This class is responsible to import data from a customer invoice
    It simply uses FieldExtractor Extract data from an Excel invoice
    """

    @staticmethod
    def add_engineers(result):

        result['bodies'] = result['hours']/40.0
        return result

    def __init__(self):
        FieldExtractor.FieldExtractor.__init__(self, {'CPI': {  'sheet': 'details',
                                                                'field': 'cpi'},
                                                      'value': {'sheet': 'details',
                                                              'field': 'value'},
                                                      'budget': {'sheet': 'details',
                                                              'field': 'budget'},
                                                      'hours': {'sheet': 'details',
                                                                 'field': 'hours'},
                                                      'date': {'sheet': 'details',
                                                                'field': 'date',
                                                                'type': FieldExtractor.FieldType.DATE}
                                                })

        self.data_producers = [Invoice.add_engineers]

    def extract(self, file_path):
        res = super(Invoice, self).extract(file_path)

        for prod in self.data_producers:
            res = prod(res)

        return res
