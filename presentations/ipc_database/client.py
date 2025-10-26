class Client:

    def __init__(self, server, pid: str):
        self.server = server
        self.pid = pid

    def read(self, key):
        return self.server.read_key(self.pid, key)

    def write(self, key, value):
        return self.server.write_key(self.pid, key, value)

    def acquire_read(self):
        return self.server.request_read_access(self.pid)

    def acquire_write(self):
        return self.server.request_write_access(self.pid)

    def release(self):
        return self.server.release_access(self.pid)
