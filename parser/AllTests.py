import unittest

loader = unittest.TestLoader()
tests = loader.discover('.', pattern="*_Tests.py")
testRunner = unittest.runner.TextTestRunner()
testRunner.run(tests)