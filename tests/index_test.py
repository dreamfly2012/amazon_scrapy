import unittest
import sys

sys.path.append("..")
import index
import logging


class IndexTest(unittest.TestCase):
    def test_check_availability(self):
        # content = "test"
        content = "Currently unavailabl"
        result = index.check_availability(content)

        if index.check_availability(content):
            self.assertEqual(result, True)
        else:
            self.assertEqual(result, True)

    def test_read_result(self):
        result = ""
        with open("result.txt", "r") as f:
            for line in f:
                line = line.rstrip("\n")
                line = line.rstrip("\r")
                result += line

        logging.info(result)


if __name__ == "__main__":
    unittest.main()
