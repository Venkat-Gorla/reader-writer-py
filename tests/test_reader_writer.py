import unittest
from src.reader_writer import ReaderWriter

class TestReaderWriter(unittest.TestCase):
    def setUp(self):
        """Runs before each test case"""
        self.reader_writer = ReaderWriter()

    def test_single_reader(self):
        """Test that a single ReadLock can be acquired and released"""
        with self.reader_writer.ReadLock(self.reader_writer):
            self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
