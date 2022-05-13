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
from dao.SQLiteTempDao import TemperatureDatabaseHandler
from util.DelayedKeyboardInterrupt import DelayedKeyboardInterrupt
from util.ReturnValueThread import TemperatureThread

#from logging.config import fileConfig


class TemperatureServer:

	kill_now = False
  
	def __init__(self):
		signal.signal(signal.SIGINT, self.exit_gracefully)
		signal.signal(signal.SIGTERM, self.exit_gracefully)

	def exit_gracefully(self, *args):
    	self.kill_now = True


tempHosts = ["192.168.1.10", "192.168.1.11", "192.168.1.12"]
logger = logging.getLogger(__name__)
dbConn = None
dateFormat = "%Y-%m-%d %H:%M:%S"


def setupLogging():

	tempFormat = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

	streamHandler = logging.StreamHandler(sys.stdout)
	streamHandler.setFormatter(tempFormat)
	streamHandler.setLevel(logging.WARNING)

	fileHandler = logging.FileHandler('.\\Logs\\temperatures.log')
	fileHandler.setFormatter(tempFormat)
	fileHandler.setLevel(logging.DEBUG)

	logger.setLevel(logging.DEBUG)
	logger.addHandler(streamHandler)
	logger.addHandler(fileHandler)


# Call the database handler to store a temperature value from a remote sensor into an SQLite database
def logTemp(address, tempValue):
	if dbConn:
		dbConn.logTemp(address, tempValue)



# Call a REST API function on a remote temperature sensor and extract the temperature value from the JSON response
def getTemp(address):


	logger.info('Polling remote temp station ' + address)

	remoteTemp = -400

	try:
		response = requests.get("http://" + address + "/temperature", timeout=10)

	except requests.Timeout as err:
		logger.error("Connection to " + address + " timed out")
	except requests.RequestException as err:
		logger.error("Connection error (Request Exception) for " + address)
	except:
		logger.exception("Exception when connecting to " + str(address))

	else:
		if response.status_code == 200:
			#print (address + " temp: " + response.json()['value'])
			remoteTemp = response.json()['value']
			
		else:
			logger.error("Error code from " + address + ": " + str(response.status_code))

	return remoteTemp


def collectDataLoop():
	threads = []

	for x in sensors:

		thread = TemperatureThread(target=getTemp, args=(x,))
		threads.append(thread)
		thread.start()

	for x in range(len(threads)):
		logTemp(sensors[x], threads[x].join())
	return



def main():
	setupLogging()
	setupDatabase()

	recordTemperatures()
	dbConn = TemperatureDatabaseHandler('test.sql')

	for i in range(3):
		print("Collecting temps (iteration " + str(i) + ")")
		collectDataLoop()
		time.sleep(5)
	
	
	print ("Finished storing temperatures")

	print("All records from database:")
	print(dbConn.getAllRecords())


	dbConn.closeDBConnection()


def main():
	
	tempServer = None

	try:
		# Shield _start() from termination.
		try:
			with DelayedKeyboardInterrupt():
				tempServer = TemperatureServer()

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
			raise

		# Application is started now and is running.
		# Wait for a termination event infinitelly.
		tempServer._run()

	except KeyboardInterrupt:
		# The _stop() is also shielded from termination.
		try:
			with DelayedKeyboardInterrupt():
				tempServer._stop()
		except KeyboardInterrupt:
			print(f'!!! got KeyboardInterrupt during stop')


if __name__ == "__main__":
	main()