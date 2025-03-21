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
        self._assert_lock_blocks_other(self.reader_writer.WriteLock, self.reader_writer.ReadLock)

    def test_reader_blocks_writers(self):
        """Ensure that writers wait while a reader holds the lock."""
        self._assert_lock_blocks_other(self.reader_writer.ReadLock, self.reader_writer.WriteLock)

    def _assert_lock_blocks_other(self, blocking_lock, blocked_lock):
        """Helper method to verify that a lock blocks another."""
        helper = LockTestHelper(blocked_lock)

        with blocking_lock(self.reader_writer):
            # Start the blocked thread while holding the lock
            helper.start_thread(self.reader_writer)

            self.assertTrue(helper.attempted.wait())

            # Ensure the blocked lock does NOT acquire while the blocking lock is held
            acquired_while_blocked = helper.acquired.wait(timeout=0.1)
            self.assertFalse(acquired_while_blocked, "Lock was acquired while it should be blocked!")

        helper.join_thread()
        self.assertTrue(helper.acquired.is_set()) # Now it should have acquired the lock

if __name__ == '__main__':
    unittest.main()

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
