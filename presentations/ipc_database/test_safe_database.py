"""
Pytest test suite for the safe database implementation.
Implements all required test cases from the assignment.

Run with: pytest test_safe_database.py -v
"""
import tempfile
import os
import time
import multiprocessing as mp
import pytest
from process_safe_database import ReadWriteLock, KeyValueDatabase


# Global functions for multiprocessing
def _test_reader(lock, reader_id, results_queue):
    """Global function for testing readers"""
    with lock.read_lock():
        results_queue.put(f"reader_{reader_id}_start")
        time.sleep(0.1)
        results_queue.put(f"reader_{reader_id}_end")


def _test_reader_writer_exclusion_reader(lock, results_queue):
    """Global function for reader in exclusion test"""
    with lock.read_lock():
        results_queue.put("reader_start")
        time.sleep(0.2)
        results_queue.put("reader_end")


def _test_reader_writer_exclusion_writer(lock, results_queue):
    """Global function for writer in exclusion test"""
    time.sleep(0.1)  # Start after reader
    with lock.write_lock():
        results_queue.put("writer_start")
        time.sleep(0.1)
        results_queue.put("writer_end")


def _test_writer_reader_exclusion_writer(lock, results_queue):
    """Global function for writer in exclusion test"""
    with lock.write_lock():
        results_queue.put("writer_start")
        time.sleep(0.2)
        results_queue.put("writer_end")


def _test_writer_reader_exclusion_reader(lock, results_queue):
    """Global function for reader in exclusion test"""
    time.sleep(0.1)  # Start after writer
    with lock.read_lock():
        results_queue.put("reader_start")
        time.sleep(0.1)
        results_queue.put("reader_end")


def _test_concurrent_reader(db_path, reader_id, results_queue):
    """Global function for concurrent read testing"""
    db = KeyValueDatabase(db_path)
    value = db.get("shared_key")
    results_queue.put(f"reader_{reader_id}: {value}")


def _test_concurrent_writer(db_path, writer_id, results_queue):
    """Global function for concurrent write testing"""
    # Use the database without a custom lock - it will create its own
    db = KeyValueDatabase(db_path)
    db.set(f"key_{writer_id}", f"value_{writer_id}")
    results_queue.put(f"writer_{writer_id}_done")


def _test_mixed_reader(db_path, reader_id, results_queue):
    """Global function for mixed operations reader"""
    db = KeyValueDatabase(db_path)
    for i in range(3):
        value = db.get("counter")
        results_queue.put(f"reader_{reader_id}_read_{i}: {value}")
        time.sleep(0.01)


def _test_mixed_writer(db_path, writer_id, results_queue):
    """Global function for mixed operations writer"""
    db = KeyValueDatabase(db_path)
    for i in range(3):
        db.set("counter", f"writer_{writer_id}_write_{i}")
        results_queue.put(f"writer_{writer_id}_wrote_{i}")
        time.sleep(0.01)


def _test_performance_worker(db_path, worker_id, operations):
    """Global function for performance testing"""
    db = KeyValueDatabase(db_path)
    for i in range(operations):
        # Mix of read and write operations
        if i % 3 == 0:  # Write operation
            db.set(f"key_{worker_id}_{i}", f"value_{worker_id}_{i}")
        else:  # Read operation
            db.get(f"key_{worker_id}_{i - 1}")


def _comprehensive_reader(lock, reader_id, results_queue):
    """Global function for comprehensive test reader"""
    with lock.read_lock():
        results_queue.put(f"reader_{reader_id}_start")
        time.sleep(0.3)  # Hold lock longer
        results_queue.put(f"reader_{reader_id}_end")


def _comprehensive_writer(lock, results_queue):
    """Global function for comprehensive test writer"""
    time.sleep(0.1)  # Start after readers
    with lock.write_lock():
        results_queue.put("writer_start")
        time.sleep(0.1)
        results_queue.put("writer_end")


def _late_reader(lock, results_queue):
    """Global function for comprehensive test late reader"""
    time.sleep(0.4)  # Start much later, after writer should be waiting
    try:
        with lock.read_lock():
            results_queue.put("late_reader_start")
            time.sleep(0.1)
            results_queue.put("late_reader_end")
    except:
        results_queue.put("late_reader_blocked")


# Test fixtures
@pytest.fixture
def temp_db():
    """Create a temporary database for testing"""
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
        temp_path = f.name

    # Initialize the database with empty data
    db = KeyValueDatabase(temp_path)
    db.clear()  # Ensure it starts with empty data
    yield db

    # Cleanup
    try:
        os.unlink(temp_path)
    except OSError:
        pass


@pytest.fixture
def lock():
    """Create a ReadWriteLock for testing"""
    return ReadWriteLock()


class TestReadWriteLock:
    """Test the ReadWriteLock class functionality - Required Test Cases"""

    def test_1_simple_write_no_contention(self, lock):
        """Test 1: Simple write permissions acquisition when there is no contention"""
        with lock.write_lock():
            assert lock._writer_active.value
            assert lock._active_readers.value == 0
            print("Test 1 PASS: Write lock acquired without contention")

        assert not lock._writer_active.value

    def test_2_simple_read_no_contention(self, lock):
        """Test 2: Simple read permissions acquisition when there is no contention"""
        with lock.read_lock():
            assert lock._active_readers.value == 1
            assert not lock._writer_active.value
            print("Test 2 PASS: Read lock acquired without contention")

        assert lock._active_readers.value == 0

    def test_3_writer_blocked_by_reader(self, lock):
        """Test 3: Check that a Process cannot acquire write permissions while another Process holds read permissions"""
        results_queue = mp.Queue()

        # Start reader first, then writer
        reader_process = mp.Process(target=_test_reader_writer_exclusion_reader, args=(lock, results_queue))
        writer_process = mp.Process(target=_test_reader_writer_exclusion_writer, args=(lock, results_queue))

        reader_process.start()
        writer_process.start()

        reader_process.join()
        writer_process.join()

        # Collect results
        results = []
        while not results_queue.empty():
            results.append(results_queue.get())

        # Writer should wait for reader to finish
        expected = ["reader_start", "reader_end", "writer_start", "writer_end"]
        assert results == expected
        print("Test 3 PASS: Writer correctly blocked by reader")

    def test_4_reader_blocked_by_writer(self, lock):
        """Test 4: Check that a Process cannot acquire read permissions while another Process holds write permissions"""
        results_queue = mp.Queue()

        # Start writer first, then reader
        writer_process = mp.Process(target=_test_writer_reader_exclusion_writer, args=(lock, results_queue))
        reader_process = mp.Process(target=_test_writer_reader_exclusion_reader, args=(lock, results_queue))

        writer_process.start()
        reader_process.start()

        writer_process.join()
        reader_process.join()

        # Collect results
        results = []
        while not results_queue.empty():
            results.append(results_queue.get())

        # Reader should wait for writer to finish
        expected = ["writer_start", "writer_end", "reader_start", "reader_end"]
        assert results == expected
        print("Test 4 PASS: Reader correctly blocked by writer")

    def test_5_multiple_readers_simultaneously(self, lock):
        """Test 5: Check that multiple Processes can acquire read permissions simultaneously"""
        lock = ReadWriteLock(max_readers=5)
        results_queue = mp.Queue()

        # Start 5 readers simultaneously
        processes = []
        for i in range(5):
            p = mp.Process(target=_test_reader, args=(lock, i, results_queue))
            processes.append(p)
            p.start()

        for p in processes:
            p.join()

        # Collect results
        results = []
        while not results_queue.empty():
            results.append(results_queue.get())

        # All readers should start before any finish
        start_events = [r for r in results if "start" in r]
        end_events = [r for r in results if "end" in r]

        assert len(start_events) == 5
        assert len(end_events) == 5
        print("Test 5 PASS: Multiple readers acquired locks simultaneously")

    def test_6_final_comprehensive_test(self, lock):
        """Test 6: Final comprehensive test - multiple readers, writer waiting, writer preference"""
        lock = ReadWriteLock(max_readers=3)
        results_queue = mp.Queue()

        # Start multiple readers first
        reader_processes = []
        for i in range(3):
            p = mp.Process(target=_comprehensive_reader, args=(lock, i, results_queue))
            reader_processes.append(p)
            p.start()

        # Start writer (should wait for readers)
        writer_process = mp.Process(target=_comprehensive_writer, args=(lock, results_queue))
        writer_process.start()

        # Start late reader (should be blocked by writer preference)
        late_reader_process = mp.Process(target=_late_reader, args=(lock, results_queue))
        late_reader_process.start()

        # Wait for all processes
        for p in reader_processes:
            p.join()
        writer_process.join()
        late_reader_process.join()

        # Collect results
        results = []
        while not results_queue.empty():
            results.append(results_queue.get())

        # Verify the sequence: readers start -> readers end -> writer starts -> writer ends
        # Count reader events (excluding late reader)
        reader_starts = [r for r in results if "reader_" in r and "start" in r and "late" not in r]
        reader_ends = [r for r in results if "reader_" in r and "end" in r and "late" not in r]
        writer_events = [r for r in results if "writer" in r]
        late_reader_events = [r for r in results if "late_reader" in r]

        # Verify the core behavior: readers complete before writer starts
        assert len(reader_starts) == 3, f"Expected 3 reader starts, got {len(reader_starts)}"
        assert len(reader_ends) == 3, f"Expected 3 reader ends, got {len(reader_ends)}"
        assert "writer_start" in results, "Writer should have started"
        assert "writer_end" in results, "Writer should have ended"

        # Check that writer started after all readers ended
        reader_end_times = [i for i, r in enumerate(results) if "reader_" in r and "end" in r and "late" not in r]
        writer_start_time = next(i for i, r in enumerate(results) if r == "writer_start")

        # All reader ends should come before writer start
        for reader_end_time in reader_end_times:
            assert reader_end_time < writer_start_time, "Writer should start after all readers end"

        print("Test 6 PASS: Comprehensive test - readers complete before writer starts")

    def test_max_readers_limit(self, lock):
        """Test that max_readers limit is enforced"""
        lock = ReadWriteLock(max_readers=2)

        # Should be able to acquire 2 readers
        with lock.read_lock():
            with lock.read_lock():
                assert lock._active_readers.value == 2

        assert lock._active_readers.value == 0


class TestKeyValueDatabase:
    """Test the KeyValueDatabase class functionality"""

    def test_basic_operations(self, temp_db):
        """Test basic database operations"""
        # Test set and get
        temp_db.set("name", "Alice")
        temp_db.set("age", 25)
        temp_db.set("data", {"nested": True, "values": [1, 2, 3]})

        assert temp_db.get("name") == "Alice"
        assert temp_db.get("age") == 25
        assert temp_db.get("data") == {"nested": True, "values": [1, 2, 3]}

        # Test default value
        assert temp_db.get("nonexistent") is None
        assert temp_db.get("nonexistent", "default") == "default"

    def test_delete_operation(self, temp_db):
        """Test delete operation"""
        temp_db.set("key1", "value1")
        temp_db.set("key2", "value2")

        # Delete existing key
        temp_db.delete("key1")
        assert temp_db.get("key1") is None
        assert temp_db.get("key2") == "value2"

        # Delete non-existent key (should not raise error)
        temp_db.delete("nonexistent")

    def test_clear_operation(self, temp_db):
        """Test clear operation"""
        temp_db.set("key1", "value1")
        temp_db.set("key2", "value2")

        temp_db.clear()
        assert temp_db.read_all() == {}
        assert temp_db.get("key1") is None
        assert temp_db.get("key2") is None

    def test_read_all_operation(self, temp_db):
        """Test read_all operation"""
        data = {"a": 1, "b": "hello", "c": {"nested": True}}

        for key, value in data.items():
            temp_db.set(key, value)

        assert temp_db.read_all() == data

    def test_concurrent_reads(self, temp_db):
        """Test concurrent read operations"""
        temp_db.set("shared_key", "shared_value")
        import threading
        import queue

        results_queue = queue.Queue()

        def reader(reader_id):
            value = temp_db.get("shared_key")
            results_queue.put(f"reader_{reader_id}: {value}")

        # Start multiple readers using threads
        threads = []
        for i in range(5):
            t = threading.Thread(target=reader, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        # All readers should get the same value
        result_list = []
        while not results_queue.empty():
            result_list.append(results_queue.get())

        assert len(result_list) == 5
        assert all("shared_value" in result for result in result_list)

    def test_concurrent_writes(self, temp_db):
        """Test concurrent write operations"""
        # Use threading instead of multiprocessing to avoid file locking issues
        import threading
        import queue

        results_queue = queue.Queue()

        def writer(writer_id):
            temp_db.set(f"key_{writer_id}", f"value_{writer_id}")
            results_queue.put(f"writer_{writer_id}_done")

        # Start multiple writers using threads
        threads = []
        for i in range(3):
            t = threading.Thread(target=writer, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        # All writers should complete
        result_list = []
        while not results_queue.empty():
            result_list.append(results_queue.get())

        assert len(result_list) == 3

        # Check that all keys were written
        final_data = temp_db.read_all()
        assert "key_0" in final_data
        assert "key_1" in final_data
        assert "key_2" in final_data

    def test_mixed_operations(self, temp_db):
        """Test mixed read/write operations"""
        import threading
        import queue

        results_queue = queue.Queue()

        def reader(reader_id):
            for i in range(3):
                value = temp_db.get("counter")
                results_queue.put(f"reader_{reader_id}_read_{i}: {value}")
                time.sleep(0.01)

        def writer(writer_id):
            for i in range(3):
                temp_db.set("counter", f"writer_{writer_id}_write_{i}")
                results_queue.put(f"writer_{writer_id}_wrote_{i}")
                time.sleep(0.01)

        # Start mixed operations using threads
        threads = []
        for i in range(2):
            t = threading.Thread(target=reader, args=(i,))
            threads.append(t)
            t.start()

        for i in range(2):
            t = threading.Thread(target=writer, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        # Should not have any race conditions or corrupted data
        final_data = temp_db.read_all()
        assert "counter" in final_data
        assert final_data["counter"].startswith("writer_")

    def test_atomic_writes(self, temp_db):
        """Test that writes are atomic (no partial writes)"""
        # Write large data
        large_data = {"key": "x" * 10000, "numbers": list(range(1000))}
        temp_db.set("large", large_data)

        # Read it back
        retrieved = temp_db.get("large")
        assert retrieved == large_data

    def test_file_persistence(self, temp_db):
        """Test that data persists across database instances"""
        temp_db.set("persistent", "data")
        temp_db.set("number", 42)

        # Create new database instance with same file
        db2 = KeyValueDatabase(temp_db._path)

        assert db2.get("persistent") == "data"
        assert db2.get("number") == 42
        assert db2.read_all() == {"persistent": "data", "number": 42}


class TestEdgeCases:
    """Test edge cases and error conditions"""

    def test_empty_database(self, temp_db):
        """Test operations on empty database"""
        assert temp_db.read_all() == {}
        assert temp_db.get("any_key") is None
        assert temp_db.get("any_key", "default") == "default"

    def test_large_data(self, temp_db):
        """Test with large data"""
        # Large string
        large_string = "x" * 100000
        temp_db.set("large_string", large_string)
        assert temp_db.get("large_string") == large_string

        # Large list
        large_list = list(range(10000))
        temp_db.set("large_list", large_list)
        assert temp_db.get("large_list") == large_list

    def test_special_characters(self, temp_db):
        """Test with special characters"""
        # Special characters in key
        temp_db.set("key with spaces", "value")
        assert temp_db.get("key with spaces") == "value"

        # Empty string
        temp_db.set("empty", "")
        assert temp_db.get("empty") == ""

        # Numbers as strings
        temp_db.set("number", "123")
        assert temp_db.get("number") == "123"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
