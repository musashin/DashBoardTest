from parser import FieldExtractor


class Invoice(FieldExtractor.FieldExtractor):
    """
    This class is responsible to import data from a customer invoice
    It simply uses FieldExtractor Extract data from an Excel invoice
    """
    #todo different fields for unit tests

    config = {'cpi': {  'sheet': 'details',
                        'field': 'cpi'},
              'value': {'sheet': 'details',
                        'field': 'value'},
               'budget': {'sheet': 'details',
                          'field': 'budget'},
                'hours': {'sheet': 'details',
                          'field': 'hours'},
               'date': {'sheet': 'details',
                         'field': 'date',
                          'type': FieldExtractor.FieldType.DATE}}

    @staticmethod
    def add_engineers(result):

        result['bodies'] = result['hours']/40.0
        return result

    def __init__(self):
        FieldExtractor.FieldExtractor.__init__(self,
                                               Invoice.config)

        self.data_producers = [Invoice.add_engineers]

    def extract(self, file_path):
        res = super(Invoice, self).extract(file_path)

        for prod in self.data_producers:
            res = prod(res)

        return res

    @staticmethod
    def get_colums():
        x = list(Invoice.config.keys())
        x.append('bodies')
        return x


