import pytest
from datetime import datetime
import sys
import os
from pathlib import Path
from src.dao.TcpSensorDao import TcpSensorDao
from src.dao.SQLiteTempDao import SQLiteTempDao


sys.path.insert(0, os.path.join(Path(__file__).resolve().parent.parent, "TempSrc"))

@pytest.fixture(scope="session")
def dbName():
	dateFormat = "%Y%m%d-%H%M%S"
	dbName = "testDB_" + datetime.strftime(datetime.now(), dateFormat) + ".sqlite3"
	print("Fixture creating db with name: " + dbName)

	yield dbName

	os.remove(os.path.join(sys.path[0], dbName))


@pytest.fixture(scope="session")
def sensorSetup(dbName):
	sensorDao = TcpSensorDao(dbName)
	sensorId = sensorDao.storeSensor("192.168.1.10", True)
	additionalSensorId = sensorDao.storeSensor("192.168.1.12", True)	
	
	yield [sensorId, additionalSensorId]

	sensorDao.deleteSensors()
	sensorDao.closeDBConnection()

@pytest.fixture(scope="session")
def tempSetup(dbName):
	tempDao = SQLiteTempDao(dbName)

	yield tempDao
	
	tempDao.deleteRecords()
	tempDao.closeDBConnection()

	

def test_DBConnectedWithOverriddenConstructor (tempSetup):
	assert tempSetup.isConnected()

def test_NewDBEmpty(tempSetup):
	assert tempSetup.isEmpty()

def test_DBNotEmptyAfterCommit(sensorSetup, tempSetup):
	tempSetup.storeRecord(sensorSetup[0], 100)
	assert not tempSetup.isEmpty()
	tempSetup.deleteRecords()

def test_SingleEntryCommittedCorrectlyRetrieved (sensorSetup, tempSetup):
	val = 100.0
	tempSetup.storeRecord(sensorSetup[0], val)
	records = tempSetup.getAllRecords()
	assert (val == records[0][2]) and (sensorSetup[0] == records[0][1])
	tempSetup.deleteRecords()


def test_SingleEntryCommittedDoesntMatchIncorrectValueWhenRetrieved (sensorSetup, tempSetup):
	val = 100
	tempSetup.storeRecord(sensorSetup[0], val)
	records = tempSetup.getAllRecords()
	assert not ((val + 1) == records[0][2]) and not ((sensorSetup[0] + "!") == records[0][1])
	tempSetup.deleteRecords()

def test_MultipleEntriesCommitedReturnCorrectNumber (sensorSetup, tempSetup):
	for i in range(100):
		tempSetup.storeRecord(sensorSetup[0], 100)
	
	records = tempSetup.getAllRecords()
	assert len(records) == 100
	tempSetup.deleteRecords()

def test_MultipleEntriesCommitedDoesntReturnIncorrectNumber (sensorSetup, tempSetup):
	for i in range(100):
		tempSetup.storeRecord(sensorSetup[0], 100)
	
	records = tempSetup.getAllRecords()
	assert not len(records) == 1
	tempSetup.deleteRecords()

def test_CorrectTempEntriesRetrievedFromMany (sensorSetup, tempSetup):
	targetTemp = 100
	numEntries = 5
	for i in range(numEntries):
		tempSetup.storeRecord(sensorSetup[0], targetTemp)
	for i in range(10):
		tempSetup.storeRecord(sensorSetup[0], 75)
	for i in range(numEntries):
		tempSetup.storeRecord(sensorSetup[0], targetTemp)

	targetRecords = tempSetup.getRecordsByTempRange(targetTemp - 1, targetTemp + 1)
	assert len(targetRecords) == (numEntries * 2)
	tempSetup.deleteRecords()

def test_CorrectSensorEntriesRetrievedFromMany (sensorSetup, tempSetup):
	numEntries = 5
	for i in range(numEntries):
		tempSetup.storeRecord(sensorSetup[0], 100)
	for i in range(20):
		tempSetup.storeRecord(sensorSetup[1], 75)
	for i in range(numEntries):
		tempSetup.storeRecord(sensorSetup[0], 100)

	targetRecords = tempSetup.getRecordsBySensor(sensorSetup[0])
	assert len(targetRecords) == (numEntries * 2)
	tempSetup.deleteRecords()
