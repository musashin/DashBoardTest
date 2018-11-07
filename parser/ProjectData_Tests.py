import unittest
from . import ProjectData


class ProjectDataTests(unittest.TestCase):
    """
    Test in normal conditions
    """

    def setUp(self):
        self.project = ProjectData.CustomerProject()

    def test_notfound_field(self):
        self.project.load_data(r'./parser/test_data/invoices')

        #self.assertEqual(result['nothere'], None)


if __name__ == '__main__':
    unittest.main()