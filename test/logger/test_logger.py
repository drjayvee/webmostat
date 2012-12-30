import os, time
import unittest
from logger import logger

class TestDBLogger(unittest.TestCase):
    def setUp(self):
        self.testDB = open("test.db", "w")
        self.dbl = logger.DBLogger(self.testDB.name)

    def tearDown(self):
        del self.dbl
        self.testDB.close()
        os.unlink(self.testDB.name)

    def test_logEvent(self):
        self.dbl.logEvent("hi", "Howdy world!", 1)
        self.assertEqual(1, self.dbl.countEvents("hi"))
        self.assertEqual(0, self.dbl.countEvents("hi", 2))
        self.assertEqual(0, self.dbl.countEvents("nope"))

        self.dbl.logEvent("hi", "no way", int(time.time()))
        self.assertEqual(2, self.dbl.countEvents("hi"))
        self.assertEqual(0, self.dbl.countEvents("no way"))

        self.dbl.purgeEvents(1337, "nope")
        # assert two rows

        self.dbl.purgeEvents(1337, "hi")
        # assert one row

        self.dbl.purgeEvents("hi")
        # assert no rows


if __name__ == "__main__":
    unittest.main()
