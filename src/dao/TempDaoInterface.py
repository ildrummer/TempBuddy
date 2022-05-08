import abc

# Database Access Object template (interface)
#
# @author ildrummer
# @version 0.1

class TempDaoInterface(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (
                # Create temp record
                hasattr(subclass, 'storeRecord') and callable(subclass.storeRecord) and 

                # Get every temp record in DB
                hasattr(subclass, 'getAllRecords') and callable(subclass.getAllRecords) and 

                # Get every temp record from a registered sensor
                hasattr(subclass, 'getRecordsBySensor') and callable(subclass.getRecordsBySensor) and 

                # Get all temp records within two datetimes
                hasattr(subclass, 'getRecordsByDateTimeRange') and callable(subclass.getRecordsByDateTimeRange) and 

                # Get all temp records within a specified temperature range
                hasattr(subclass, 'getRecordsByTempRange') and callable(subclass.getRecordsByTempRange) and

                # Delete all records
                hasattr(subclass, 'deleteRecords') and callable(subclass.deleteRecords) and

                # Delete records within two datetimes
                hasattr(subclass, 'deleteRecordsByDateTimeRange') and callable(subclass.deleteRecordsByDateTimeRange) 
         )