#
# Database handler to decouple the database implementation from the rest of the program logic.
#    Not yet implemented - temperature retrieval method.
# 

import sqlite3
from datetime import datetime
import os
import sys
from pathlib import Path
sys.path.insert(0, os.path.join(Path(__file__).resolve().parent.parent, "Database"))

class TemperatureDatabaseHandler:

	dbConn = None
	dbName = ""
	tableName = "tempHistory"
	dateFormat = "%Y-%m-%d %H:%M:%S"
	currentTime = None


	def __init__(self, givenName):
		try:
			self.dbConn = sqlite3.connect(os.path.join(sys.path[0], givenName))
			dbName = givenName
		except Error as e:
			print(e)

		if self.isConnected():
			cur = self.dbConn.cursor()
			cur.execute('''CREATE TABLE IF NOT EXISTS main.tempHistory(date DATETIME NOT NULL, host VARCHAR NOT NULL, tempValue REAL NOT NULL)''')
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
		numRecords = len(cur.fetchall())
		return numRecords == 0
		

    # Store a the passed temperature and sensor address.  Add a datetime stamp in an accepted SQLite format
	def logTemp(self, address, tempValue):
		if not self.isConnected():
			raise sqlite3.DatabaseError("Database not connected")

		self.currentTime = datetime.now(tz=None)
		cur = self.dbConn.cursor()

		insertParams = '''INSERT INTO tempHistory VALUES (?, ?, ?)'''
		dataTuple = (self.currentTime.strftime(self.dateFormat), address, tempValue)
		cur.execute(insertParams, dataTuple)
		self.dbConn.commit()

	def getRecordCount(self):
		if not self.isConnected():
			raise sqlite3.DatabaseError("Database not connected")

		cur = self.dbConn.cursor()
		cur.execute("SELECT * FROM " + self.tableName)
		return len(cur.fetchall())

	def getAllRecords(self):
		if not self.isConnected():
			raise sqlite3.DatabaseError("Database not connected")

		cur = self.dbConn.cursor()
		return cur.execute('SELECT * from tempHistory;').fetchall()

	def getRecordsByHost (self, address):
		if not self.isConnected():
			raise sqlite3.DatabaseError("Database not connected")

		cur = self.dbConn.cursor()
		selectParams = '''SELECT * FROM tempHistory WHERE host = ?'''
		cur.execute(selectParams, [address])
		return cur.fetchall()

	def getRecordsByTemp (self, temp):
		if not self.isConnected():
			raise sqlite3.DatabaseError("Database not connected")

		cur = self.dbConn.cursor()
		selectParams = '''SELECT * FROM tempHistory WHERE tempValue = ?'''
		cur.execute(selectParams, [temp])
		return cur.fetchall()	

	def deleteAllRecords(self):
		if not self.isConnected():
			raise sqlite3.DatabaseError("Database not connected")

		cur = self.dbConn.cursor()
		cur.execute('DELETE from tempHistory;').fetchall()