import abc

#
# Sensor Interface
#

class SensorInterface(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, 'getTemperature') and callable(subclass.getTemperature) and
            hasattr(subclass, '__str__') and callable(subclass.__str__)
         )