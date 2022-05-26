# 
# Main program that collects temperature data.
#    - currently set up to gather data once and then end.  Will be modified for temperature collection/storage every minute.
#

import time
import threading
import json
import requests
import sys
import signal
import logging
from dao.SQLiteTempDao import SQLiteTempDao
from dao.TcpSensorDao import TcpSensorDao
from util.DelayedKeyboardInterrupt import DelayedKeyboardInterrupt
from util.ReturnValueThread import TemperatureThread

#from logging.config import fileConfig


class TemperatureServer:
  
	def __init__(self, sensorDbName, tempDbName):
		
		self.logger = self.setupLogging(logging.getLogger(__name__))
		self.logger.info("Logging setup completed")

		time.sleep(3)

		self.sensorDb = self.setupSensorDatabase(sensorDbName)
		self.tempDb = self.setupTemperatureDatabase(tempDbName)

		self.logger.info("Initialization complete")
 
	def setupLogging(self, logger):

		tempFormat = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

		streamHandler = logging.StreamHandler(sys.stdout)
		streamHandler.setFormatter(tempFormat)
		streamHandler.setLevel(logging.INFO)

		fileHandler = logging.FileHandler('.\\logs\\temperatures.log')
		fileHandler.setFormatter(tempFormat)
		fileHandler.setLevel(logging.DEBUG)

		logger.setLevel(logging.DEBUG)
		logger.addHandler(streamHandler)
		logger.addHandler(fileHandler)

		return logger


	def setupSensorDatabase(self, sensorDbName: str):
		sensorDb = TcpSensorDao(sensorDbName)
		return sensorDb if sensorDb.isConnected() else None
	
	def setupTemperatureDatabase(self, tempDbName: str):
		tempDb = SQLiteTempDao(tempDbName)
		return tempDb if tempDb.isConnected() else None

	def logTemp(self, sensorId, tempValue):
		# Call the database handler to store a temperature value from a remote sensor into an SQLite database
		if self.tempDb:
			self.tempDb.storeRecord(sensorId, tempValue)


	def collectDataLoop(self):
		threads = []

		for x in sensors:

			thread = TemperatureThread(target=getTemp, args=(x,))
			threads.append(thread)
			thread.start()

		for x in range(len(threads)):
			self.logTemp(sensors[x], threads[x].join())
		return



	def _run(self):
		
		while True:
			print ("Running!")
			time.sleep(2)

		# for i in range(3):
		# 	self.logger.info("Starting temperature collection")
		# 	self.collectDataLoop()
		# 	time.sleep(5)

	def _shutdown(self, reason: str):
		if self.logger:
			self.logger.info("Shutting down Temp Server.  Reason: {0}".format(reason))
		
		if self.tempDb:
			self.tempDb.closeDBConnection
		
		if self.sensorDb:
			self.sensorDb.closeDBConnection
		
		if self.logger:
			self.logger.info("Database connections closed")

def main():
	
	tempServer = None

	try:
		# Shield _start() from termination.
		try:
			with DelayedKeyboardInterrupt():
				tempServer = TemperatureServer('tempSensors.sql', 'temperatures.sql')

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