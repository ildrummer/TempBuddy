import threading
import json
import requests
import sys
import logging
from tempDBHandler import TemperatureDatabaseHandler
from tempThread import TemperatureThread

#from logging.config import fileConfig


tempHosts = ["192.168.1.10", "192.168.1.11", "192.168.1.12"]
logger = logging.getLogger(__name__)
dbConn = None
dateFormat = "%Y-%m-%d %H:%M:%S"


def setupLogging():

	tempFormat = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

	streamHandler = logging.StreamHandler(sys.stdout)
	streamHandler.setFormatter(tempFormat)
	streamHandler.setLevel(logging.WARNING)

	fileHandler = logging.FileHandler('temperatures.log')
	fileHandler.setFormatter(tempFormat)
	fileHandler.setLevel(logging.DEBUG)

	logger.setLevel(logging.DEBUG)
	logger.addHandler(streamHandler)
	logger.addHandler(fileHandler)

	return

def logTemp(address, tempValue):
	if dbConn:
		dbConn.logTemp(address, tempValue)





def getTemp(address):


	logger.info('Polling remote temp station ' + address)

	remoteTemp = -400

	try:
		response = requests.get("http://" + address + "/temperature", timeout=10)

	except requests.Timeout as err:
		logger.error("Connection to ESP32 " + address + " timed out")
	except requests.RequestException as err:
		logger.error("Connection error for ESP32 " + address)
	except:
		logger.exception("Exception when connecting to " + str(address))

	else:
		if response.status_code == 200:
			#print (address + " temp: " + response.json()['value'])
			remoteTemp = response.json()['value']
			
		else:
			logger.error("Error code from ESP32 " + address + ": " + str(response.status_code))

	return remoteTemp


def main():
	setupLogging()
	dbConn = TemperatureDatabaseHandler('test.sql')

	threads = []
	
	for x in tempHosts:

		#tempThread = threading.Thread(target=getAndPrintTemp, args=(dbConn.cursor(),x,))
		tempThread = TemperatureThread(target=getTemp, args=(x,))
		threads.append(tempThread)
		tempThread.start()

	for x in threads:
		print (x.join())
	return


if __name__ == "__main__":
	main()
