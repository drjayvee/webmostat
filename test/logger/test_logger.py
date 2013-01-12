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
        self.assertEqual(0, self.dbl.countEvents("nope"))

        self.dbl.logEvent("hi", "no way")
        self.assertEqual(2, self.dbl.countEvents("hi"))
        self.assertEqual(0, self.dbl.countEvents("no way"))

    def test_countEvents(self):
        # create some events
        self.dbl.logEvent("hi", "hi 1", 1)
        self.dbl.logEvent("yo", "yo 1", 2)
        self.dbl.logEvent("yo", "yo 2", 3)
        self.dbl.logEvent("hi", "hi 2", 4)
        self.dbl.logEvent("hi", "hi 3", 5)
        self.dbl.logEvent("yo", "yo 3", 6)

        self.assertEqual(3, self.dbl.countEvents("hi"))
        self.assertEqual(3, self.dbl.countEvents("yo"))

        self.assertEqual(2, self.dbl.countEvents("hi", 2))
        self.assertEqual(0, self.dbl.countEvents("hi", 2, 3))
        self.assertEqual(0, self.dbl.countEvents("hi", 10))


    def test_purgeEvents(self):
        # create three events
        self.dbl.logEvent("hi", "ev1", 1)
        self.dbl.logEvent("hi", "ev2", 3)
        self.dbl.logEvent("hi", "ev3", 10)
        self.assertEqual(3, self.dbl.countEvents("hi"))

        # purge other event type
        self.dbl.purgeEvents("nope")
        self.assertEqual(3, self.dbl.countEvents("hi"))

        # purge events older than existing
        self.dbl.purgeEvents("hi", 11)
        self.assertEqual(3, self.dbl.countEvents("hi"))

        # purge last event
        self.dbl.purgeEvents("hi", 10)
        self.assertEqual(2, self.dbl.countEvents("hi"))

        # purge all events
        self.dbl.purgeEvents("hi")
        self.assertEqual(0, self.dbl.countEvents("hi"))

        # create three events
        self.dbl.logEvent("hi", "ev1", 1)
        self.dbl.logEvent("hi", "ev2", 3)
        self.dbl.logEvent("hi", "ev3", 10)
        self.dbl.logEvent("hi", "ev4", 11)

        # purge from 3 - 10
        self.dbl.purgeEvents("hi", 3, 10)
        self.assertEqual(2, self.dbl.countEvents("hi"))

if __name__ == "__main__":
    unittest.main()
