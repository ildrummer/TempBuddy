import json
import requests
import sys

tempHosts = ["192.168.1.10", "192.168.1.11", "192.168.1.12"]

for address in tempHosts:
	try:
		response = requests.get("http://" + address + "/temperature", timeout=10)

	except requests.Timeout as err:
		print("Connection to ESP32 " + address + " timed out")
	except requests.RequestException as err:
		print("Connection error for ESP32 " + address)
	except:
		print("Exception when connecting to " + str(address))

	else:
		if response.status_code == 200:
			print (address + " temp: " + response.json()['value'])	
		else:
			print("Error code from ESP32 " + address + ": " + str(response.status_code))

