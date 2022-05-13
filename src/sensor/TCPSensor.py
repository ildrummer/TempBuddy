#
# TCP Sensor
#

from sensor.SensorInterface import SensorInterface


@SensorInterface.register
class Sensor():

    def __init__(self):
        self.id = None
        self.name = None
        self.path = None
        self.enabled = False
    
    def getTemperature(self):
        return None