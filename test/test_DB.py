import sqlite3
import pytest
from datetime import datetime
import sys
import os
from pathlib import Path
from src.dao.SQLiteTempDao import SQLiteTempDao


sys.path.insert(0, os.path.join(Path(__file__).resolve().parent.parent, "TempSrc"))


@pytest.fixture(scope="session")
def dbSetup():
	dateFormat = "%Y%m%d-%H%M%S"
	dbName = "testDB_" + datetime.strftime(datetime.now(), dateFormat) + ".sqlite3"
	print("Fixture creating db with name: " + dbName)
	db = SQLiteTempDao(dbName)
	yield db
	db.closeDBConnection()
	os.remove(os.path.join(sys.path[0], dbName))


def test_DBConnectedWithOverriddenConstructor (dbSetup):
	assert dbSetup.isConnected()

def test_NewDBEmpty(dbSetup):
	assert dbSetup.isEmpty()

def test_DBNotEmptyAfterCommit(dbSetup):
	dbSetup.storeRecord("192.168.1.10", 100)
	assert not dbSetup.isEmpty()
	dbSetup.deleteRecords()

def test_SingleEntryCommittedCorrectlyRetrieved (dbSetup):
	sensor = "192.168.1.10"
	val = 100
	dbSetup.storeRecord(sensor, val)
	records = dbSetup.getAllRecords()
	assert (val == records[0][2]) and (sensor == records[0][1])
	dbSetup.deleteRecords()


def test_SingleEntryCommittedDoesntMatchIncorrectValueWhenRetrieved (dbSetup):
	sensor = "192.168.1.10"
	val = 100
	dbSetup.storeRecord(sensor, val)
	records = dbSetup.getAllRecords()
	assert not ((val + 1) == records[0][2]) and not ((sensor + "!") == records[0][1])
	dbSetup.deleteRecords()

def test_MultipleEntriesCommitedReturnCorrectNumber (dbSetup):
	for i in range(100):
		dbSetup.storeRecord(100, "192.168.1.10")
	
	records = dbSetup.getAllRecords()
	assert len(records) == 100
	dbSetup.deleteRecords()

def test_MultipleEntriesCommitedDoesntReturnIncorrectNumber (dbSetup):
	for i in range(100):
		dbSetup.storeRecord(100, "192.168.1.10")
	
	records = dbSetup.getAllRecords()
	assert not len(records) == 1
	dbSetup.deleteRecords()

def test_CorrectTempEntriesRetrievedFromMany (dbSetup):
	targetTemp = 100
	numEntries = 5
	for i in range(numEntries):
		dbSetup.storeRecord('192.168.1.10', targetTemp)
	for i in range(10):
		dbSetup.storeRecord('192.168.1.12', 75)
	for i in range(numEntries):
		dbSetup.storeRecord('192.168.1.10', targetTemp)

	targetRecords = dbSetup.getRecordsByTempRange(targetTemp - 1, targetTemp + 1)
	assert len(targetRecords) == (numEntries * 2)
	dbSetup.deleteRecords()

def test_CorrectAddressEntriesRetrievedFromMany (dbSetup):
	targetAddress = '192.168.1.12'
	numEntries = 5
	for i in range(numEntries):
		dbSetup.storeRecord(targetAddress, 100)
	for i in range(10):
		dbSetup.storeRecord('192.168.1.10', 75)
	for i in range(numEntries):
		dbSetup.storeRecord(targetAddress, 100)

	targetRecords = dbSetup.getRecordsBySensor(targetAddress)
	assert len(targetRecords) == (numEntries * 2)
	dbSetup.deleteRecords()

def test_DBConnectionAfterClosed(dbSetup):
	dbSetup.closeDBConnection();
	assert not dbSetup.isConnected() 
