import unittest
import tempfile
import os
from server import Server
from client import Client


class TestDatabaseSystem(unittest.TestCase):

    def setUp(self):
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        tmp.close()
        self.file = tmp.name
        self.server = Server(self.file)

    def tearDown(self):
        os.unlink(self.file)

    def test_basic_write_and_read(self):
        writer = Client(self.server, "W1")
        reader = Client(self.server, "R1")

        self.assertTrue(writer.acquire_write())
        writer.write("x", 10)
        self.assertEqual(writer.read("x"), 10)
        writer.release()

        self.assertTrue(reader.acquire_read())
        self.assertEqual(reader.read("x"), 10)
        reader.release()

    def test_writer_blocks_reader(self):
        writer = Client(self.server, "W")
        reader = Client(self.server, "R")

        self.assertTrue(writer.acquire_write())
        self.assertFalse(reader.acquire_read())  # should fail since writer holds lock
        writer.release()

        self.assertTrue(reader.acquire_read())
        reader.release()


if __name__ == "__main__":
    unittest.main()
