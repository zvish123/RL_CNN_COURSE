from database import Database


class Server:
    def __init__(self, filepath: str):
        self.db = Database(filepath)

    def request_read_access(self, pid: str, timeout: float = 0.5):
        return self.db.acquire_read(pid, timeout)

    def request_write_access(self, pid: str, timeout: float = 0.5):
        return self.db.acquire_write(pid, timeout)

    def release_access(self, pid: str):
        self.db.release(pid)

    def read_key(self, pid: str, key: str):
        return self.db.read(pid, key)

    def write_key(self, pid: str, key: str, value):
        self.db.write(pid, key, value)
