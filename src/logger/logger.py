import datetime, time
import sqlite3

class Logger:
    def logEvent(self, type, value, timeStamp=None):
        pass

    def getEvents(self, type, fromTimeStamp=0, toTimeStamp=None):
        pass

    def countEvents(self, type, fromTimeStamp=0, toTimeStamp=None):
        pass

    def purgeEvents(self, type, fromTimeStamp=0, toTimeStamp=None):
        pass

class PrintLogger(Logger):
    logFormat = "@ {ts}: {type}: {value}"

    def logEvent(self, type, value, timeStamp=None):
        timeStamp = timeStamp or int(time.time())
        print PrintLogger.logFormat.format(
            ts=PrintLogger.__convertTS(timeStamp), type=type, value=value
        )

    @staticmethod
    def __convertTS(timeStamp):
        return str(datetime.datetime.fromtimestamp(timeStamp))

class DBLogger(Logger):

    def __init__(self, db):
        self.con = sqlite3.connect(db)

        res = self.con.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            """
        )
        if not res.fetchone():
            DBLogger.__initializeDB(self.con)

    def __del__(self):
        self.con.commit()
        self.con.close()

    def logEvent(self, type, value, timeStamp=None):
        timeStamp = timeStamp or int(time.time())
        self.con.execute(
            "INSERT INTO event_log VALUES (?, ?, ?)",
            (timeStamp, type, value)
        )

    def getEvents(self, type, fromTimeStamp=0, toTimeStamp=None):
        toConstraint = ""
        binding = (type, fromTimeStamp)
        if toTimeStamp:
            toConstraint = "AND timestamp <= ?"
            binding += (toTimeStamp,)

        return self.con.execute(
            """
            SELECT timestamp, data
            FROM event_log
            WHERE type = ? AND timestamp >= ?
            """ + toConstraint,
            binding
        ).fetchall()

    def countEvents(self, type, fromTimeStamp=0, toTimeStamp=None):
        # Unfortunately, sqlite3 does not support cursor.rowcount
        # http://docs.python.org/2/library/sqlite3.html#sqlite3.Cursor.rowcount
        return len(
            self.getEvents(type, fromTimeStamp, toTimeStamp )
        )

    def purgeEvents(self, type, fromTimeStamp=0, toTimeStamp=None):
        toConstraint = ""
        binding = (type, fromTimeStamp)

        if toTimeStamp:
            toConstraint = "AND timestamp <= ?"
            binding += (toTimeStamp,)

        self.con.execute(
            """
            DELETE FROM event_log
            WHERE type = ? AND timestamp >= ?
            """ + toConstraint,
            binding
        )

    @staticmethod
    def __initializeDB(con):
        con.execute(
            """
            CREATE TABLE event_log(
                timestamp INTEGER PRIMARY KEY,
                type TEXT,
                data TEXT
            )
            """
        )
