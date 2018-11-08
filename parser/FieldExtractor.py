from enum import Enum
import xlrd
import datetime

class FieldOffset(Enum):
    """
    A definition of the possible location of
    the value compared to the field name
    """
    RIGHT = 0
    TOP = 1
    LEFT = 2
    BOTTOM = 3


class FieldType(Enum):
        """
        A definition of the possible cell type
        """
        DATE = 0



class FieldExtractor:
    """
    A class to extract a serie of fields from an Excel File
    """

    offset = {FieldOffset.RIGHT: (0, 1),
              FieldOffset.TOP: (-1, 0),
              FieldOffset.LEFT: (0, -1),
              FieldOffset.BOTTOM: (1, 0)}

    def __init__(self, field_definition):
        """
        Construc
        :param field_definition: a map of field to extract. Each field
                contains a map with:
                The spreadsheet name
                The field name
                The offset of the data (default, right) relative to the field name
        """

        self.fieldDefinition = field_definition

    def extract(self, file_path):
        """
        Extract field data from an excel fileFieldExtractor.py
        :param file_path: path to the excel file
        :return:
        """

        results = dict()

        with xlrd.open_workbook(filename=file_path) as workbook:

            for key, field in self.fieldDefinition.items():

                xl_sheet = workbook.sheet_by_name(field['sheet'])

                for row_num in range(xl_sheet.nrows):
                    row_value = xl_sheet.row_values(row_num)

                    for col_num, cell in enumerate(row_value):

                        if type(cell) is str:
                            if cell.lower() == field['field'].lower():

                                if 'offset' in field:
                                    cell = xl_sheet.cell(row_num +
                                                        FieldExtractor.offset[field['offset']][0],
                                                        col_num +
                                                        FieldExtractor.offset[field['offset']][1])
                                    results[field['field']] = cell.value

                                else:
                                    cell = xl_sheet.cell(row_num,
                                                         col_num + 1)
                                    results[field['field']] = cell.value

                                if 'type' in field:
                                    if field['type'] == FieldType.DATE:
                                        results[field['field']] = datetime.datetime(*xlrd.xldate_as_tuple(results[field['field']], workbook.datemode))


                                break


                if field['field'] not in results:
                    results[field['field']] = None


        return results
