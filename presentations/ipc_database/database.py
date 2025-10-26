import json
import os
import threading
import time
from typing import Any, Dict, Optional

MAX_READERS = 10


class PermissionError(Exception):
    pass


class Database:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self._data: Dict[str, Any] = {}

        self._state_lock = threading.Lock()
        self._cond = threading.Condition(self._state_lock)

        self._readers = set()
        self._writer: Optional[str] = None

        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    self._data = json.load(f)
                print(f"[DB] Loaded existing data.")
            except:
                self._data = {}
        else:
            self._sync_to_disk()

    def _sync_to_disk(self):
        tmp = self.filepath + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2, ensure_ascii=False)
        os.replace(tmp, self.filepath)
        print(f"[DB] Data written to disk.")

    def acquire_read(self, pid: str, timeout: Optional[float] = None) -> bool:
        with self._cond:
            start = time.time()
            while True:
                if self._writer is None and (len(self._readers) < MAX_READERS or pid in self._readers):
                    self._readers.add(pid)
                    print(f"[DB] READ granted to {pid}.")
                    return True

                remaining = None if timeout is None else timeout - (time.time() - start)
                if remaining is not None and remaining <= 0:
                    print(f"[DB] READ timeout for {pid}.")
                    return False
                self._cond.wait(remaining)

    def acquire_write(self, pid: str, timeout: Optional[float] = None) -> bool:
        with self._cond:
            start = time.time()
            while True:
                if self._writer is None and len(self._readers) == 0:
                    self._writer = pid
                    print(f"[DB] WRITE granted to {pid}.")
                    return True

                remaining = None if timeout is None else timeout - (time.time() - start)
                if remaining is not None and remaining <= 0:
                    print(f"[DB] WRITE timeout for {pid}.")
                    return False
                self._cond.wait(remaining)

    def release(self, pid: str):
        with self._cond:
            if pid in self._readers:
                self._readers.remove(pid)
                print(f"[DB] {pid} released READ.")
            elif self._writer == pid:
                self._writer = None
                print(f"[DB] {pid} released WRITE.")
            else:
                raise PermissionError(f"{pid} has no permission to release.")
            self._cond.notify_all()

    def read(self, pid: str, key: str):
        with self._state_lock:
            if pid not in self._readers and pid != self._writer:
                raise PermissionError(f"{pid} does not have read permission.")
            print(f"[DB] {pid} read key={key}.")
            return self._data.get(key)

    def write(self, pid: str, key: str, value: Any):
        with self._state_lock:
            if pid != self._writer:
                raise PermissionError(f"{pid} does not have write permission.")
            self._data[key] = value
            print(f"[DB] {pid} wrote key={key}, value={value}.")
            self._sync_to_disk()
