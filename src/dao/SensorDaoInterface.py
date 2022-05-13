import abc

# Temperature Sensor Dao template (interface)
#
# @author ildrummer
# @version 0.1

class SensorDaoInterface(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (
                hasattr(subclass, 'storeSensor') and callable(subclass.storeSensor) and 

                hasattr(subclass, 'getAllSensors') and callable(subclass.getAllSensors) and 

                # Get sensor by ID
                hasattr(subclass, 'getSensor') and callable(subclass.getSensor) and 

                hasattr(subclass, 'updateSensorPath') and callable(subclass.updateSensorPath) and

                hasattr(subclass, 'updateSensorStatus') and callable(subclass.updateSensorStatus) and

                hasattr(subclass, 'deleteSensors') and callable(subclass.deleteSensors) and

                # Delete sensor by ID
                hasattr(subclass, 'deleteSensor') and callable(subclass.deleteSensor)
         )