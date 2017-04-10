import unittest
import cast.analysers.test


class Test(unittest.TestCase):
    def testRegisterPlugin(self):
        # create a DotNet analysis
        analysis = cast.analysers.test.UATestAnalysis('ApacheCamel')
        # DotNet need a selection of a csproj or sln
        analysis.add_selection("camel-cdi")
        # analysis.add_database_table()
        analysis.set_verbose()
        analysis.run()

if __name__ == "__main__":
    unittest.main()
