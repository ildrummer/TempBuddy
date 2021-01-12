import sqlite3
import pytest
from datetime import datetime
import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.join(Path(__file__).resolve().parent.parent, "TempSrc"))
from dbHandler import TemperatureDatabaseHandler

@pytest.fixture(scope="session")
def dbSetup():
	dateFormat = "%Y%m%d-%H%M%S"
	dbName = "testDB_" + datetime.strftime(datetime.now(), dateFormat) + ".sql"
	print("Fixture creating db with name: " + dbName)
	db = TemperatureDatabaseHandler(dbName)
	yield db
	db.closeDBConnection()
	os.remove(os.path.join(sys.path[0], dbName))


def test_DBConnectedWithOverriddenConstructor (dbSetup):
	assert dbSetup.isConnected()

def test_NewDBEmpty(dbSetup):
	assert dbSetup.isEmpty()

def test_DBNotEmptyAfterCommit(dbSetup):
	dbSetup.logTemp("192.168.1.10", 100)
	assert not dbSetup.isEmpty()
	dbSetup.deleteAllRecords()

def test_SingleEntryCommittedCorrectlyRetrieved (dbSetup):
	address = "192.168.1.10"
	val = 100
	dbSetup.logTemp(address, val)
	records = dbSetup.getAllRecords()
	assert (val == records[0][2]) and (address == records[0][1])
	dbSetup.deleteAllRecords()

def test_MultipleEntriesCommitedReturnCorrectNumber (dbSetup):
	for i in range(100):
		dbSetup.logTemp(100, "192.168.1.10")
	assert dbSetup.getRecordCount() == 100
	dbSetup.deleteAllRecords()

def test_CorrectTempEntriesRetrievedFromMany (dbSetup):
	targetTemp = 100
	numEntries = 5
	for i in range(numEntries):
		dbSetup.logTemp('192.168.1.10', targetTemp)
	for i in range(10):
		dbSetup.logTemp('192.168.1.12', 75)
	for i in range(numEntries):
		dbSetup.logTemp('192.168.1.10', targetTemp)

	targetRecords = dbSetup.getRecordsByTemp(targetTemp)
	assert len(targetRecords) == (numEntries * 2)
	dbSetup.deleteAllRecords()

def test_CorrectTempEntriesRetrievedFromMany (dbSetup):
	targetAddress = '192.168.1.12'
	numEntries = 5
	for i in range(numEntries):
		dbSetup.logTemp(targetAddress, 100)
	for i in range(10):
		dbSetup.logTemp('192.168.1.10', 75)
	for i in range(numEntries):
		dbSetup.logTemp(targetAddress, 100)

	targetRecords = dbSetup.getRecordsByHost(targetAddress)
	assert len(targetRecords) == (numEntries * 2)
	dbSetup.deleteAllRecords()

def test_DBConnectionAfterClosed(dbSetup):
	dbSetup.closeDBConnection();
	assert not dbSetup.isConnected() 
