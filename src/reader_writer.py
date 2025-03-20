from threading import Semaphore

class ReaderWriter:
    def __init__(self):
        self.__reader_count = 0
        self.__reader_mutex = Semaphore(1)
        self.__reader_writer_mutex = Semaphore(1)

# vegorla any further cleanup?
    class ReadLock:
        def __init__(self, reader_writer):
            self.outer = reader_writer

        def __enter__(self):
            self.outer.__reader_mutex.acquire()

            self.outer.__reader_count += 1
            if self.outer.__reader_count == 1:
                self.outer.__reader_writer_mutex.acquire()

            self.outer.__reader_mutex.release()

            return self

        def __exit__(self, exc_type, exc_value, traceback):
            self.outer.__reader_mutex.acquire()

            self.outer.__reader_count -= 1
            if self.outer.__reader_count == 0:
                self.outer.__reader_writer_mutex.release()

            self.outer.__reader_mutex.release()

            return True  # Suppress exception (exception will not propagate)

