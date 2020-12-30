#
# Database handler to decouple the database implementation from the rest of the program logic.
#    Not yet implemented - temperature retrieval method.
# 

import sqlite3
from datetime import datetime


class TemperatureDatabaseHandler:

	dbConn = None
	tableName = "tempHistory"
	dateFormat = "%Y-%m-%d %H:%M:%S"
	currentTime = None


	def __init__(self, dbAddress):
		try:
			self.dbConn = sqlite3.connect(dbAddress)
		except Error as e:
			print(e)

		if self.isConnected():
			cur = self.dbConn.cursor()
			cur.execute('''CREATE TABLE IF NOT EXISTS main.tempHistory(date DATETIME, host VARCHAR, tempValue REAL)''')
			cur.execute('''PRAGMA journal_mode = WAL''')
	
	def isConnected (self):
		return self.dbConn != None

	def closeDBConnection(self):
		if self.dbConn != None:
			self.dbConn.commit()
			self.dbConn.close()
			self.dbConn = None
			self.tableName = ""

	def isEmpty(self):
		if not self.isConnected():
			raise sqlite3.DatabaseError("Database not connected") 

		cur = self.dbConn.cursor()
		cur.execute("SELECT * FROM " + self.tableName)
		return cur.fetchone() == None
		

    # Store a the passed temperature and sensor address.  Add a datetime stamp in an accepted SQLite format
	def logTemp(self, address, tempValue):
		if not self.isConnected():
			raise sqlite3.DatabaseError("Database not connected")

		self.currentTime = datetime.now(tz=None)
		cur = self.dbConn.cursor()

		sqliteInsertWithParams = '''INSERT INTO tempHistory VALUES (?, ?, ?)'''
		dataTuple = (self.currentTime.strftime(self.dateFormat), address, tempValue)
		cur.execute(sqliteInsertWithParams, dataTuple)
		self.dbConn.commit()


	def getAllRecords(self):
		if not self.isConnected():
			raise sqlite3.DatabaseError("Database not connected")

		cur = self.dbConn.cursor()
		return cur.execute('SELECT * from tempHistory;').fetchall()