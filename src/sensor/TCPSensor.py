#
# TCP Sensor
#

from logging import Logger

import requests
from sensor.SensorInterface import SensorInterface


@SensorInterface.register
class Sensor():

    def __init__(self, id: str, name: str, path: str, enabled: bool, logger: Logger):
        self.id = id
        self.name = name
        self.path = path
        self.enabled = enabled
        self.logger = logger
    
    def getTemperature(self):
    # Call a REST API function on a remote temperature sensor and extract the temperature value from the JSON response
        self.logger.info('Polling TCP sensor {0}'.format(self.name))

        remoteTemp = -400

        try:
            response = requests.get("http://{0}/temperature".format(self.path), timeout=10)

        except requests.Timeout as err:
            self.logger.error("Connection to TCP sensor {0} timed out".format(self.path))
        except requests.RequestException as err:
            self.logger.error("Connection error (Request Exception) for {0}".format(self.name))
        except:
            self.logger.exception("Exception when connecting to {0}".format(self.name))

        else:
            if response.status_code == 200:
                remoteTemp = response.json()['value']
                self.logger.info("Sensor {0} returned temperature: {1}".format(self.name, remoteTemp))
                
            else:
                self.logger.error("Error code from {0}: {1}".format(self.name, response.status_code))

        return remoteTemp