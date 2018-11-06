from enum import Enum
import xlrd


class FieldOffset(Enum):
    """
    A definition of the possible location of
    the value compared to the field name
    """
    RIGHT = 0
    TOP = 1
    LEFT = 2
    BOTTOM = 3


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

        with xlrd.open_workbook(file_path) as workbook:

            for key, field in self.fieldDefinition.items():

                xl_sheet = workbook.sheet_by_name(field['sheet'])

                for row_num in range(xl_sheet.nrows):
                    row_value = xl_sheet.row_values(row_num)
                    for col_num, cell in enumerate(row_value):

                        if cell == field['field']:

                            if 'offset' in field:
                                results[field['field']] = xl_sheet.cell(row_num + FieldExtractor.offset[field['offset']][0],
                                                                        col_num + FieldExtractor.offset[field['offset']][1]).value
                            else:
                                results[field['field']] = xl_sheet.cell(
                                    row_num,
                                    col_num + 1).value



        return results
