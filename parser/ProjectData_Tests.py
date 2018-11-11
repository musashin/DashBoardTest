import unittest
from . import ProjectData
import pandas as pd
import numpy as np


class ProjectDataTests(unittest.TestCase):
    """
    Test in normal conditions
    """

    def setUp(self):
        self.project = ProjectData.CustomerProject('test')
        self.project.load_data(r'./parser/test_data/invoices')

    def test_loaded_project_field(self):
        self.assertEqual(self.project.get_value(pd.Timestamp('20180404 0:0:0'), 'cpi').item(), 10)
        self.assertEqual(self.project.get_value(pd.Timestamp('20180304 0:0:0'), 'budget').item(), 300.0)

    def test_computed_project_field(self):
        self.assertTrue(np.isnan(self.project.get_value(pd.Timestamp('20180204 0:0:0'), 'bodies').item()))

    def test_computed_missing_field(self):
        self.assertEqual(self.project.get_value(pd.Timestamp('20180304 0:0:0'), 'bodies').item(), 2.125)

if __name__ == '__main__':
    unittest.main()