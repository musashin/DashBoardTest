from . import FieldExtractor


class Invoice(FieldExtractor.FieldExtractor):
    """
    This class is responsible to import data from a customer invoice
    It simply uses FieldExtractor Extract data from an Excel invoice
    """

    def __init__(self):
        FieldExtractor.FieldExtractor.__init__(self, {'CPI': {  'sheet': 'details',
                                                                'field': 'cpi'},
                                                      'date': {'sheet': 'details',
                                                                'field': 'date'}
                                                })

