from . import FieldExtractor
import datetime

class Invoice(FieldExtractor.FieldExtractor):
    """
    This class is responsible to import data from a customer invoice
    It simply uses FieldExtractor Extract data from an Excel invoice
    """

    def __init__(self):
        FieldExtractor.FieldExtractor.__init__(self, {'CPI': {  'sheet': 'details',
                                                                'field': 'cpi'},
                                                      'date': {'sheet': 'details',
                                                                'field': 'date',
                                                                'type': FieldExtractor.FieldType.DATE}
                                                })

    def extract(self, file_path):
        res = super(Invoice, self).extract(file_path)

        #todo, add self computed fields

        return res
