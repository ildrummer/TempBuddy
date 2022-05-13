from asyncio.windows_events import NULL
import sqlite3
from attr import NOTHING
import pytest
from datetime import datetime
import sys
import os
from pathlib import Path
from src.dao.TcpSensorDao import TcpSensorDao


sys.path.insert(0, os.path.join(Path(__file__).resolve().parent.parent, "TempSrc"))


@pytest.fixture(scope="session")
def dbSetup():
	dateFormat = "%Y%m%d-%H%M%S"
	dbName = "testDB_" + datetime.strftime(datetime.now(), dateFormat) + ".sqlite3"
	print("Fixture creating db with name: " + dbName)
	sensorDao = TcpSensorDao(dbName)

	yield sensorDao

	sensorDao.closeDBConnection()
	os.remove(os.path.join(sys.path[0], dbName))


def test_DBConnectedWithOverriddenConstructor (dbSetup):
	assert dbSetup.isConnected()

def test_NewDBEmpty(dbSetup):
	assert dbSetup.isEmpty()

def test_DBNotEmptyAfterCommit(dbSetup):
	dbSetup.storeSensor( "Test Sensor", "192.168.1.10", True)
	assert not dbSetup.isEmpty()
	dbSetup.deleteSensors()


def test_SingleEntryCommittedCorrectlyRetrieved (dbSetup):
	sensorPath = "192.168.1.10"
	enabled = False
	dbSetup.storeSensor("Test Sensor", sensorPath, enabled)
	sensors = dbSetup.getAllSensors()
	assert len(sensors) == 1
	assert (enabled == sensors[0].enabled) and (sensorPath == sensors[0].path)
	dbSetup.deleteSensors()


def test_SingleEntryCommittedDoesntMatchIncorrectValueWhenRetrieved (dbSetup):
	sensorPath = "192.168.1.10"
	enabled = False
	dbSetup.storeSensor("Test Sensor", sensorPath, enabled)
	sensors = dbSetup.getAllSensors()
	assert len(sensors) == 1
	assert (enabled == sensors[0].enabled) and (sensorPath != sensors[0].path + "_test")
	dbSetup.deleteSensors()


def test_retrieveSensorBySensorId (dbSetup):
	sensorPath = "192.168.1.10"
	enabled = False
	id = dbSetup.storeSensor("Test Sensor", sensorPath, enabled)
	sensor = dbSetup.getSensor(id)
	assert sensor[0].path == sensorPath and sensor[0].enabled == enabled
	dbSetup.deleteSensors()


def test_multipleSensorsCommitedReturnCorrectNumber (dbSetup):
	for i in range(100):
		dbSetup.storeSensor("Test Sensor", "192.168.1.{0}".format(i), True)
	
	records = dbSetup.getAllSensors()
	assert len(records) == 100
	dbSetup.deleteSensors()


def test_updateSensorPath (dbSetup):
	sensorPath = "192.168.1.10"
	enabled = False
	id = dbSetup.storeSensor("Test Sensor", sensorPath, enabled)
	sensor = dbSetup.getSensor(id)
	assert sensor[0].path == sensorPath

	changedPath = sensorPath + "_changed"
	dbSetup.updateSensorPath(id, changedPath)
	
	sensor = dbSetup.getSensor(id)
	assert sensor[0].path != sensorPath and sensor[0].path == changedPath
	dbSetup.deleteSensors()


def test_updateSensorStatus (dbSetup):
	sensorPath = "192.168.1.10"
	enabled = True
	id = dbSetup.storeSensor("Test Sensor", sensorPath, enabled)
	sensor = dbSetup.getSensor(id)
	assert sensor[0].path == sensorPath

	disabled = not enabled
	dbSetup.updateSensorStatus(id, disabled)
	
	sensor = dbSetup.getSensor(id)
	assert sensor[0].enabled != enabled and sensor[0].enabled == disabled
	dbSetup.deleteSensors()

def test_updateSensorName (dbSetup):
	sensorPath = "192.168.1.10"
	sensorName = "Test Sensor"
	enabled = True
	id = dbSetup.storeSensor(sensorName, sensorPath, enabled)
	sensor = dbSetup.getSensor(id)
	assert sensor[0].path == sensorPath

	differentName = "Different Sensor"
	dbSetup.updateSensorName(id, differentName)
	
	sensor = dbSetup.getSensor(id)
	assert sensor[0].enabled != enabled and sensor[0].enabled == differentName
	dbSetup.deleteSensors()


def test_deleteSensorById (dbSetup):
	sensorPath = "192.168.1.10"
	enabled = True
	id = dbSetup.storeSensor("Test Sensor", sensorPath, enabled)
	sensor = dbSetup.getSensor(id)
	assert sensor != NULL and id != NULL

	dbSetup.deleteSensor(id)
	deletedSensor = dbSetup.getSensor(id)
	assert len(deletedSensor) == 0

def test_DBConnectionAfterClosed(dbSetup):
	dbSetup.closeDBConnection()
	assert not dbSetup.isConnected() 
