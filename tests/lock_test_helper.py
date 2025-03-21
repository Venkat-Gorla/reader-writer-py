import threading

class LockTestHelper:
    """Helper class to test reader/writer locks in a controlled way."""
    def __init__(self, lock_class):
        self.lock_class = lock_class
        self.attempted = threading.Event()  # Set when the thread attempts to acquire the lock
        self.acquired = threading.Event()   # Set when the thread successfully acquires the lock
        self.thread = None

    def start_thread(self, reader_writer):
        """Starts the lock task in a separate thread."""
        self.thread = threading.Thread(target=self._lock_task, args=(reader_writer,))
        self.thread.start()

    def join_thread(self):
        """Waits for the thread to complete."""
        if self.thread:
            self.thread.join()

    def _lock_task(self, reader_writer):
        """Task to acquire the given lock type."""
        self.attempted.set()  # Mark that the thread is attempting to acquire the lock
        with self.lock_class(reader_writer):
            self.acquired.set()  # Mark that the lock was successfully acquired
