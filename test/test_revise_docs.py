import importlib.util, pathlib, unittest

path=pathlib.Path(__file__).parents[1]/"scripts"/"revise_docs.py"
spec=importlib.util.spec_from_file_location("revise_docs",path); module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)

class ReviseDocsTest(unittest.TestCase):
    def test_extracts_source_pr(self):
        self.assertEqual(module.referenced_source_pr("See https://github.com/acme/app/pull/42"),("acme/app",42))
    def test_rejects_unsafe_path(self):
        with self.assertRaises(ValueError): module.safe_path("../outside.md")
        with self.assertRaises(ValueError): module.safe_path("script.py")

if __name__=="__main__": unittest.main()
