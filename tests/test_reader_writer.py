import unittest
from unittest.mock import Mock
from src.reader_writer import ReaderWriter

class TestReaderWriter(unittest.TestCase):
    def setUp(self):
        """Runs before each test case"""
        self.reader_writer = ReaderWriter()

    def test_single_reader(self):
        """Test that a single ReadLock can be acquired and released"""
        mock = Mock()

        with self.reader_writer.ReadLock(self.reader_writer):
            mock()

        mock.assert_called_once()

if __name__ == '__main__':
    unittest.main()
