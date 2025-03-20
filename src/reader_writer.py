from threading import Semaphore

class ReaderWriter:
    def __init__(self):
        self.__reader_count = 0
        self.__reader_mutex = Semaphore(1)
        self.__reader_writer_mutex = Semaphore(1)

    def increment_reader(self):
        self.__reader_count += 1
        return self.__reader_count

    def decrement_reader(self):
        self.__reader_count -= 1
        return self.__reader_count

    class ReadLock:
        def __init__(self, reader_writer):
            self.outer = reader_writer

        def __enter__(self):
            with self.outer.__reader_mutex:
                readers = self.outer.increment_reader()
                if readers == 1:
                    self.outer.__reader_writer_mutex.acquire()

            return self

        def __exit__(self, exc_type, exc_value, traceback):
            with self.outer.__reader_mutex:
                readers = self.outer.decrement_reader()
                if readers == 0:
                    self.outer.__reader_writer_mutex.release()

            return False  # Allow exceptions to propagate

# vegorla remove after testing
# Example Usage
reader_writer = ReaderWriter()
with reader_writer.ReadLock(reader_writer):
    print("Reading data safely!")
