import os
import unittest

from flattools.fbs.parser import load
from flattools.lang.kt.generate import generate_kt
from flattools.lang.py.generate import generate_py
from flattools.lang.rust.generate import generate_rust
from flattools.lang.swift.generate import generate_swift
from pathlib import Path


class CodeGeneratorTests(unittest.TestCase):
    TEST_CASE = "tests/parser-cases/color.fbs"
    TESTS_DIR = Path(__file__).parent.parent.absolute()

    def setUp(self):
        self.maxDiff = None
        os.chdir(self.TESTS_DIR)

    def tearDown(self):
        os.rmdir("color")
        pass

    def test_rust(self):
        generate_rust(self.TEST_CASE, load(self.TEST_CASE))
        with open("color/color.rs") as f1:
            os.remove("color/color.rs")
            with open("tests/expected/golden-color.rs") as f2:
                self.assertEqual(f2.read(), f1.read())

    def test_kotlin(self):
        generate_kt(self.TEST_CASE, load(self.TEST_CASE))
        with open("color/color.kt") as f1:
            os.remove("color/color.kt")
            with open("tests/expected/golden-color.kt") as f2:
                self.assertEqual(f2.read(), f1.read())

    def test_swift(self):
        generate_swift(self.TEST_CASE, load(self.TEST_CASE))
        with open("color/color.swift") as f1:
            os.remove("color/color.swift")
            with open("tests/expected/golden-color.swift") as f2:
                self.assertEqual(f2.read(), f1.read())

    def test_py(self):
        generate_py(self.TEST_CASE, load(self.TEST_CASE))
        with open("color/color.py") as f1:
            os.remove("color/color.py")
            os.remove("color/__init__.py")
            with open("tests/expected/golden-color.py") as f2:
                self.assertEqual(f2.read(), f1.read())


if __name__ == "__main__":
    unittest.main()
