# TCP/IP implementation of the SensorInterface
#
# @author ildrummer
# @version 0.1

import sqlite3
from datetime import datetime
import os
import sys
import uuid
import logging
from pathlib import Path
from tokenize import String
from xmlrpc.client import boolean
from src.dao.SensorDaoInterface import SensorDaoInterface

sys.path.insert(0, os.path.join(Path(__file__).resolve().parent.parent.parent, "Database"))

@SensorDaoInterface.register
class TcpSensorDao:

	def __init__(self, dbName):

		self.logger = self.setupLogging(logging.getLogger("TcpSensorDao"))
		self.logger.info("Attempting to connect to Sensor DB: {0}".format(os.path.join(sys.path[0], dbName)))

		self.dbConn = None
		self.cursor = None
		self.dbName = ""
		self.tableName = "SENSORS"
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
				CREATE TABLE IF NOT EXISTS"{0}" (
					"ID" VARCHAR(50) PRIMARY KEY NOT NULL,
					"NAME" VARCHAR(200),
					"PATH" VARCHAR (100) NOT NULL,
					"ENABLED" INTEGER NOT NULL DEFAULT 1
				);'''.format(self.tableName))
			self.cursor.execute('''PRAGMA journal_mode = WAL''')
			self.cursor.execute('''PRAGMA foreign_keys = ON;''')

			self.logger.info("Connected")

	def setupLogging(self, logger):

		tempFormat = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

		streamHandler = logging.StreamHandler(sys.stdout)
		streamHandler.setFormatter(tempFormat)
		streamHandler.setLevel(logging.INFO)

		fileHandler = logging.FileHandler('.\\logs\\tcpsensordao.log')
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

		self.cursor.execute("SELECT ID FROM {0}".format(self.tableName))
		numRecords = len(self.cursor.fetchall())
		return numRecords == 0
		

    # Store a sensor path (hostname) and enabled status
	def storeSensor(self, name: String, path: String, enabled: boolean):
		if not self.isConnected():
			raise sqlite3.DatabaseError("Database not connected")

		sensorId = str(uuid.uuid4())
		insertParams = '''INSERT INTO {0} (ID, NAME, PATH, ENABLED) VALUES (?,?,?,?);'''.format(self.tableName)
		self.cursor.execute(insertParams, [sensorId, name, path, 1 if enabled else 0])
		self.dbConn.commit()
		return sensorId

	def getAllSensors(self):
		if not self.isConnected():
			raise sqlite3.DatabaseError("Database not connected")

		rows = self.cursor.execute('SELECT ID, PATH, ENABLED FROM {0};'.format(self.tableName)).fetchall()

		sensors = []
		for r in rows:
			sensors.append(self.getSensorFromRow(r))

		return sensors

	def getSensor (self, sensorId: String):
		if not self.isConnected():
			raise sqlite3.DatabaseError("Database not connected")

		selectParams = '''SELECT ID, PATH, ENABLED FROM {0} WHERE ID = ?;'''.format(self.tableName)
		self.cursor.execute(selectParams, [sensorId])
		return self.getSensorFromRow(self.cursor.fetchall())

	def updateSensorName(self, sensorId: String, name: String):
		if not self.isConnected():
			raise sqlite3.DatabaseError("Database not connected")

		insertParams = '''UPDATE {0} SET NAME = ? WHERE ID = ?;'''.format(self.tableName)
		self.cursor.execute(insertParams, [name, sensorId])
		self.dbConn.commit()

	def updateSensorPath(self, sensorId: String, path: String):
		if not self.isConnected():
			raise sqlite3.DatabaseError("Database not connected")

		insertParams = '''UPDATE {0} SET PATH = ? WHERE ID = ?;'''.format(self.tableName)
		self.cursor.execute(insertParams, [path, sensorId])
		self.dbConn.commit()
	
	
	def updateSensorStatus(self, sensorId: String, enabled: boolean):
		if not self.isConnected():
			raise sqlite3.DatabaseError("Database not connected")

		insertParams = '''UPDATE {0} SET ENABLED = ? WHERE ID = ?;'''.format(self.tableName)
		self.cursor.execute(insertParams, [1 if enabled else 0, sensorId])
		self.dbConn.commit()


	def deleteSensors(self):
		if not self.isConnected():
			raise sqlite3.DatabaseError("Database not connected")

		self.cursor.execute('DELETE FROM {0};'.format(self.tableName))

	def deleteSensor  (self, sensorId: String):
		if not self.isConnected():
			raise sqlite3.DatabaseError("Database not connected")

		selectParams = '''DELETE FROM {0} WHERE ID = ?;'''.format(self.tableName)
		self.cursor.execute(selectParams, [sensorId])

	def getSensorFromRow (self, row):
		sensor = Sensor()
		sensor.id = row[0]
		sensor.name = row[1]
		sensor.path = row[2]
		sensor.enabled = row[3]

		return sensor