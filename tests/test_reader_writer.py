import unittest
from unittest.mock import Mock
from src.reader_writer import ReaderWriter
from tests.lock_test_helper import LockTestHelper

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

    def test_multiple_readers(self):
        """Test that multiple readers can acquire the ReadLock simultaneously"""
        mock1, mock2 = Mock(), Mock()

        with self.reader_writer.ReadLock(self.reader_writer):
            mock1()
            with self.reader_writer.ReadLock(self.reader_writer):
                mock2()

        mock1.assert_called_once()
        mock2.assert_called_once()

    def test_single_writer(self):
        """Test that a single writer can acquire the WriteLock"""
        mock = Mock()

        with self.reader_writer.WriteLock(self.reader_writer):
            mock()

        mock.assert_called_once()

    def test_writer_blocks_readers(self):
        """Ensure that readers wait while a writer holds the lock."""
        reader_helper = LockTestHelper(self.reader_writer.ReadLock)

        with self.reader_writer.WriteLock(self.reader_writer):
            # Start the reader thread while holding the write lock
            reader_helper.start_thread(self.reader_writer)

            self.assertTrue(reader_helper.attempted.wait())

            # Ensure the reader does NOT acquire the lock while the writer holds it
            acquired_while_blocked = reader_helper.acquired.wait(timeout=0.1)
            self.assertFalse(acquired_while_blocked, "Reader acquired lock while writer was holding it!")

        reader_helper.join_thread()
        self.assertTrue(reader_helper.acquired.is_set()) # Now it should have acquired the lock

if __name__ == '__main__':
    unittest.main()

    # def test_reader_blocks_writer(self):
    #     """Ensure that a writer waits until all readers release the lock"""
    #     mock = Mock()

    #     with self.reader_writer.ReadLock(self.reader_writer):
    #         self.assertFalse(self.reader_writer.writers_allowed())
    #         mock()

    #     mock.assert_called_once()

    # def test_multiple_writers(self):
    #     """Ensure that only one writer can hold the lock at a time"""
    #     mock1, mock2 = Mock(), Mock()

    #     with self.reader_writer.WriteLock(self.reader_writer):
    #         mock1()
    #         with self.assertRaises(RuntimeError):
    #             with self.reader_writer.WriteLock(self.reader_writer):
    #                 mock2()

    #     mock1.assert_called_once()
    #     mock2.assert_not_called()
