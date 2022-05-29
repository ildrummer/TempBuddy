# SQLite implementation of the TempDaoInterface
#
# @author ildrummer
# @version 0.1

import sqlite3
from datetime import datetime
import os
import sys
import logging
from pathlib import Path
from tokenize import String
from src.dao.TempDaoInterface import TempDaoInterface

sys.path.insert(0, os.path.join(Path(__file__).resolve().parent.parent.parent, "database"))

@TempDaoInterface.register
class SQLiteTempDao:

	def __init__(self, dbName: str):

		self.logger = self.setupLogging(logging.getLogger("SQLiteTempDao"))
		self.logger.info("Attempting to connect to Temp DB: {0}".format(os.path.join(sys.path[0], dbName)))

		self.dbConn = None
		self.cursor = None
		self.dbName = ""
		self.tableName = "TEMPERATURES"
		self.dateFormat = "%Y-%m-%d %H:%M:%S"
		self.currentTime = None

		try:
			self.dbConn = sqlite3.connect(os.path.join(sys.path[0], dbName))
			self.dbName = dbName
		except Exception as e:
			print(e)

		if self.isConnected():
			self.cursor = self.dbConn.cursor()
			self.cursor.execute('''
				CREATE TABLE IF NOT EXISTS "{0}" (
					"RECORD_ID" INTEGER PRIMARY KEY AUTOINCREMENT,
					"DATETIME" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
					"TEMP" REAL NOT NULL DEFAULT 0,
					"SENSOR_ID" VARCHAR(50) NOT NULL DEFAULT '0',
					CONSTRAINT "SENSOR_ID" FOREIGN KEY ("SENSOR_ID") REFERENCES "SENSORS" ("ID")
				);'''.format(self.tableName))
			self.cursor.execute('''PRAGMA journal_mode = WAL''')
			self.cursor.execute('''PRAGMA foreign_keys = ON;''')

			self.logger.info("Connected")

	def setupLogging(self, logger):

		tempFormat = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

		streamHandler = logging.StreamHandler(sys.stdout)
		streamHandler.setFormatter(tempFormat)
		streamHandler.setLevel(logging.INFO)

		fileHandler = logging.FileHandler('..\\logs\\sqlitetempdao.log')
		fileHandler.setFormatter(tempFormat)
		fileHandler.setLevel(logging.DEBUG)

		logger.setLevel(logging.DEBUG)
		logger.addHandler(streamHandler)
		logger.addHandler(fileHandler)

		return logger

	def isConnected (self):
		return self.dbConn != None

	def closeDBConnection(self):
		if self.dbConn != None:
			self.dbConn.commit()
			self.dbConn.close()
			self.dbConn = None
			self.cursor = None
			self.tableName = ""

	def isEmpty(self):
		if not self.isConnected():
			raise sqlite3.DatabaseError("Database not connected") 

		self.cursor.execute("SELECT RECORD_ID FROM {0}".format(self.tableName))
		numRecords = len(self.cursor.fetchall())
		return numRecords == 0
		

    # Store a the passed temperature and sensor address.  Add a datetime stamp in an accepted SQLite format
	def storeRecord(self, sensorId: str, tempValue: float):
		if not self.isConnected():
			raise sqlite3.DatabaseError("Database not connected")

		insertParams = '''INSERT INTO {0} (SENSOR_ID, TEMP) VALUES (?,?);'''.format(self.tableName)
		self.cursor.execute(insertParams, (sensorId, tempValue))
		self.dbConn.commit()

	def getAllRecords(self):
		if not self.isConnected():
			raise sqlite3.DatabaseError("Database not connected")

		return self.cursor.execute('SELECT RECORD_ID, SENSOR_ID, TEMP, DATETIME FROM {0};'.format(self.tableName)).fetchall()

	def getRecordsBySensor (self, sensorId: str):
		if not self.isConnected():
			raise sqlite3.DatabaseError("Database not connected")

		selectParams = '''SELECT RECORD_ID, TEMP, DATETIME FROM {0} WHERE SENSOR_ID = ?;'''.format(self.tableName)
		self.cursor.execute(selectParams, [sensorId])
		return self.cursor.fetchall()

	def getRecordsByDateTimeRange (self, startTime: datetime, endTime: datetime):
		if not self.isConnected():
			raise sqlite3.DatabaseError("Database not connected")

		# need some timestamp format validation here

		selectParams = '''SELECT RECORD_ID, SENSOR_ID, TEMP, DATETIME FROM {0} WHERE DATETIME BETWEEN ? AND ?;'''.format(self.tableName)
		self.cursor.execute(selectParams, [startTime, endTime])
		return self.cursor.fetchall()

	def getRecordsByTempRange (self, lowTemp: float, highTemp: float):
		if not self.isConnected():
			raise sqlite3.DatabaseError("Database not connected")

		selectParams = '''SELECT RECORD_ID, SENSOR_ID, TEMP, DATETIME FROM {0} WHERE TEMP BETWEEN ? AND ?;'''.format(self.tableName)
		self.cursor.execute(selectParams, [lowTemp, highTemp])
		return self.cursor.fetchall()	

	def deleteRecords(self):
		if not self.isConnected():
			raise sqlite3.DatabaseError("Database not connected")

		self.cursor.execute('DELETE FROM {0};'.format(self.tableName))

	def deleteRecordsByDateTimeRange  (self, startTime: datetime, endTime: datetime):
		if not self.isConnected():
			raise sqlite3.DatabaseError("Database not connected")

		# need some timestamp format validation here

		selectParams = ''''DELETE FROM {0} WHERE DATETIME BETWEEN ? AND ?;'''.format(self.tableName)
		self.cursor.execute(selectParams, [startTime, endTime])
