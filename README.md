# Reader-Writer Problem (Python)

This project implements the classic **Reader-Writer problem** using Python’s `threading.Semaphore`. It ensures safe concurrent access to a shared resource with multiple readers and writers in a multithreaded environment.

## ✅ Features

- ✔️ Multiple readers can read concurrently
- ✔️ Writers get exclusive access
- ✔️ Prevents race conditions using semaphores
- ✔️ Clean context-manager support with `with` blocks
- ✔️ Fully tested with comprehensive unit test coverage

## 📊 Design Overview

The core synchronization is handled by the `ReaderWriter` class with two nested context managers: `ReadLock` and `WriteLock`.

### Internal State

- `__reader_count`: Shared counter to track the number of active readers.
- `_reader_mutex`: Semaphore to synchronize access to `__reader_count`.
- `_reader_writer_mutex`: Semaphore that locks access to the resource for both readers and writers.

### Reader Locking (`ReadLock`)

```python
with ReaderWriter.ReadLock(rw):
    # safe to read
```

- First reader acquires `_reader_writer_mutex`
- Last reader releases it

### Writer Locking (`WriteLock`)

```python
with ReaderWriter.WriteLock(rw):
    # safe to write
```

- Writers always acquire `_reader_writer_mutex` for exclusive access

## 🧪 Unit Testing

Tests are located in the `tests/` directory:

- `test_reader_writer.py` — functional and concurrency tests
- `lock_test_helper.py` — utility functions for threading test setup

✅ Covers race conditions, proper semaphore behavior, and exception handling.

Run tests from the project root:

```bash
python -m unittest discover tests
```

📸 **Screenshot of tests in action will be added soon.**

## 📁 Project Structure

```
reader-writer-py/
│
├── src/
│   └── reader_writer.py        # Core logic
│
├── tests/
│   ├── test_reader_writer.py   # Unit tests
│   └── lock_test_helper.py     # Threading test helpers
│
└── README.md
```

## 🚀 Usage Example

```python
from src.reader_writer import ReaderWriter

rw = ReaderWriter()

with rw.ReadLock(rw):
    print("Reading safely")

with rw.WriteLock(rw):
    print("Writing safely")
```

## 👨‍💻 About the Author

I'm a seasoned developer with a passion for design, clean code, and continuous learning. This project was completed as part of my deeper dive into Python concurrency and threading.

Feel free to connect or fork the project — always happy to collaborate or discuss improvements.
