# 
# Main program that collects temperature data.
#    - currently set up to gather data once and then end.  Will be modified for temperature collection/storage every minute.
#

import random
import time
import threading
import json
import requests
import sys
import signal
import logging
from dao.SQLiteTempDao import SQLiteTempDao
from dao.TcpSensorDao import TcpSensorDao
from sensor.SensorInterface import SensorInterface
from sensor.TCPSensor import TcpSensor
from util.DelayedKeyboardInterrupt import DelayedKeyboardInterrupt
from util.ReturnValueThread import TemperatureThread

#from logging.config import fileConfig

class TemperatureServer:
  
	def __init__(self, sensorDaoName, tempDaoName):
		
		self.logger = self.setupLogging(logging.getLogger("TemperatureServer"))
		self.logger.info("Logging setup completed")

		self.sensorDao = self.setupSensorDatabase(sensorDaoName)
		self.tempDao = self.setupTemperatureDatabase(tempDaoName)

		self.sensors = []

		
		self.logger.info("Initialization complete")
 
	def setupLogging(self, logger):

		tempFormat = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

		streamHandler = logging.StreamHandler(sys.stdout)
		streamHandler.setFormatter(tempFormat)
		streamHandler.setLevel(logging.INFO)

		fileHandler = logging.FileHandler('..\\logs\\temperatures.log')
		fileHandler.setFormatter(tempFormat)
		fileHandler.setLevel(logging.DEBUG)

		logger.setLevel(logging.DEBUG)
		logger.addHandler(streamHandler)
		logger.addHandler(fileHandler)

		return logger


	def setupSensorDatabase(self, sensorDaoName: str):
		sensorDao = TcpSensorDao(sensorDaoName)

		# if sensorDao:
		# 	sensorDao.storeSensor("test {0}".format(random.randint(0, 100)), "192.168.1.{0}".format(random.randint(0,999)), True)

		return sensorDao if sensorDao.isConnected() else None
	
	def getSensors(self):
		if self.sensors is not None and len(self.sensors) is 0 and self.sensorDao:
			self.sensors = self.sensorDao.getAllSensors()
		return self.sensors


	def setupTemperatureDatabase(self, tempDaoName: str):
		tempDao = SQLiteTempDao(tempDaoName)
		return tempDao if tempDao.isConnected() else None

	def logTemp(self, sensor, tempValue):
		# Call the database handler to store a temperature value from a remote sensor into an SQLite database
		if self.tempDao:
			self.tempDao.storeRecord(sensor.id, tempValue)


	def collectData(self):
		threads = []

		for x in self.sensors:
			if x.enabled:
				thread = TemperatureThread(target=TcpSensor.getTemperature, args=(x,))
				threads.append(thread)
				thread.start()

		for x in range(len(threads)):
			temp = threads[x].join()

			if temp is not None:
				self.logTemp(self.sensors[x], temp)
		return


	def _run(self):

		print("Sensors:")
		for sensor in self.getSensors():
			print("\t{0}".format(sensor))

		while True:
			self.collectData()
			time.sleep(60)


	def _shutdown(self, reason: str):
		if self.logger:
			self.logger.info("Shutting down Temp Server.  Reason: {0}".format(reason))
		
		if self.tempDao:
			self.tempDao.closeDBConnection
		
		if self.sensorDao:
			self.sensorDao.closeDBConnection
		
		if self.logger:
			self.logger.info("Database connections closed")

def main():
	
	tempServer = None

	try:
		# Shield _start() from termination.
		try:
			with DelayedKeyboardInterrupt():
				tempServer = TemperatureServer('tempBhuti.sqlite3.db', 'tempBhuti.sqlite3.db')

		# If there was an attempt to terminate the application,
		# the KeyboardInterrupt is raised AFTER the _start() finishes
		# its job.
		#
		# In that case, the KeyboardInterrupt is re-raised and caught in
		# exception handler below and _stop() is called to clean all resources.
		#
		# Note that it might be generally unsafe to call stop() methods
		# on objects that are not started properly.
		# This is the main reason why the whole execution of _start()
		# is shielded.

		except KeyboardInterrupt:
			print(f'!!! got KeyboardInterrupt during start')
			tempServer._shutdown("Keyboard interrupt during start")
			raise

		# Application is started now and is running.
		# Wait for a termination event infinitelly.
		tempServer._run()

	except KeyboardInterrupt:
		# The _stop() is also shielded from termination.
		try:
			with DelayedKeyboardInterrupt():
				tempServer._shutdown("Keyboard interrupt during normal operation")
		except KeyboardInterrupt:
			print(f'!!! got KeyboardInterrupt during stop')


if __name__ == "__main__":
	main()