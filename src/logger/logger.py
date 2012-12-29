import datetime
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

	def logEvent(self, timeStamp, type, value):
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
		self.con.close()

	def logEvent(self, timeStamp, type, value):
		self.con.execute(
			"INSERT INTO event_log VALUES (?, ?, ?)",
			(timeStamp, type, value)
		)

	def getEvents(self, type, fromTimeStamp=0, toTimeStamp=None):
		return self.con.execute(
			"SELECT * FROM event_log WHERE type = ?",
			type
		).fetchall()

	def countEvents(self, type, fromTimeStamp=0, toTimeStamp=None):
		timeConstraint = ""
		binding = (type,)
		if fromTimeStamp:
			timeConstraint = "AND timestamp >= ?"
			binding = (type, fromTimeStamp)

		return self.con.execute(
			"""
			SELECT COUNT(timestamp) as count
			FROM event_log
			WHERE type = ?
			""" + timeConstraint,
			binding
		).fetchone()[0]

	def purgeEvents(self, type, fromTimeStamp=0, toTimeStamp=None):
		self.con.execute(
			"DELETE FROM event_log WHERE type = ? AND timestamp < ?",
			(type, fromTimeStamp)
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
