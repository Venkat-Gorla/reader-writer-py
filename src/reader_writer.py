from threading import Semaphore

class ReaderWriter:
    def __init__(self):
        self.__reader_count = 0
        self._reader_mutex = Semaphore(1)
        self._reader_writer_mutex = Semaphore(1)

    class ReadLock:
        def __init__(self, reader_writer):
            if not isinstance(reader_writer, ReaderWriter):
                raise TypeError("ReadLock must be instantiated with a ReaderWriter instance.")
            self.outer = reader_writer

        def __enter__(self):
            with self.outer._reader_mutex:
                readers = self.outer.increment_reader()
                if readers == 1:
                    self.outer._reader_writer_mutex.acquire()

            return self

        def __exit__(self, exc_type, exc_value, traceback):
            with self.outer._reader_mutex:
                readers = self.outer.decrement_reader()
                if readers == 0:
                    self.outer._reader_writer_mutex.release()

            return False # Allow exceptions to propagate

    def increment_reader(self):
        if self._reader_mutex.acquire(blocking=False):
            raise RuntimeError("Error: Reader mutex was not locked!")
        self.__reader_count += 1
        return self.__reader_count

    def decrement_reader(self):
        if self._reader_mutex.acquire(blocking=False):
            raise RuntimeError("Error: Reader mutex was not locked!")
        self.__reader_count -= 1
        return self.__reader_count

    class WriteLock:
        def __init__(self, reader_writer):
            if not isinstance(reader_writer, ReaderWriter):
                raise TypeError("WriteLock must be instantiated with a ReaderWriter instance.")
            self.outer = reader_writer

        def __enter__(self):
            self.outer._reader_writer_mutex.acquire()
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            self.outer._reader_writer_mutex.release()
            return False  # Allow exceptions to propagate

