import os
import unittest


# The Run with Python Console checkbox in run config has to be unchecked when using PyCharm.
class UnitTestLauncher(object):

    @staticmethod
    def run_tests():

        ls_paths = []

        # Find all relevant subdirectories that contain tests.
        for path, subdirs, files in os.walk('tests'):
            if "pycache" not in path and path != 'tests':
                ls_paths.append(path)

        # Loop through subdirectories and append the suites to suites and run suites.
        suites = unittest.TestSuite()
        for path in ls_paths:
            loader = unittest.TestLoader()
            suite = loader.discover(path)
            suites.addTests(suite)

        unittest.TextTestRunner().run(suites)


UnitTestLauncher.run_tests()
