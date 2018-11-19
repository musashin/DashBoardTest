import unittest
from . import ProjectData
import pandas as pd
import numpy as np


class ProjectDataTests(unittest.TestCase):
    """
    Test in normal conditions
    """

    def setUp(self):
        self.project = ProjectData.CustomerProject('customer name', 'project name')
        self.project.load_data(r'./parser/test_data/invoices')

    def test_loaded_project_field(self):
        self.assertEqual(self.project.get_value(pd.Timestamp('20180404 0:0:0'), 'cpi').item(), 10)
        self.assertEqual(self.project.get_value(pd.Timestamp('20180304 0:0:0'), 'budget').item(), 300.0)

    def test_computed_project_field(self):
        self.assertTrue(np.isnan(self.project.get_value(pd.Timestamp('20180204 0:0:0'), 'bodies').item()))

    def test_computed_missing_field(self):
        self.assertEqual(self.project.get_value(pd.Timestamp('20180304 0:0:0'), 'bodies').item(), 2.125)

    def test_computed_nonexistent_field(self):
        self.assertEqual(self.project.get_value(pd.Timestamp('20180304 0:0:0'), 'none'), None)

    def test_activity(self):
        self.assertFalse(self.project.is_active_project(pd.Timestamp('20180404 0:0:0')+pd.Timedelta(3, unit='M')))
        self.assertTrue(self.project.is_active_project(pd.Timestamp('20180404 0:0:0') + pd.Timedelta(3, unit='M')-pd.Timedelta(1, unit='m')))
        self.assertTrue(self.project.is_active_project(pd.Timestamp('20180304 0:0:0')))
        self.assertTrue(self.project.is_active_project(pd.Timestamp('20180104 0:0:0')))
        self.assertFalse(self.project.is_active_project(pd.Timestamp('20180103 0:0:0')))

    def test_cpi_warning(self):
        pass

    def test_budget_warning(self):
        pass


if __name__ == '__main__':
    unittest.main()