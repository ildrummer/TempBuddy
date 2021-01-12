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
	return TemperatureDatabaseHandler(dbName)


def test_DBConnectedWithOverriddenConstructor (dbSetup):
	assert dbSetup.isConnected()

def test_NewDBEmpty(dbSetup):
	assert dbSetup.isEmpty()

def test_DBNotEmptyAfterCommit(dbSetup):
	dbSetup.logTemp("192.168.1.10", 100)
	assert not dbSetup.isEmpty()
	dbSetup.deleteAllRecords()

def test_EntryCommittedSameSelected (dbSetup):
	address = "192.168.1.10"
	val = 100
	dbSetup.logTemp(address, val)
	records = dbSetup.getAllRecords()
	assert (val == records[0][2]) and (address == records[0][1])

def test_DBConnectionAfterClosed(dbSetup):
	dbSetup.closeDBConnection();
	assert not dbSetup.isConnected() 





#cur.execute('''CREATE TABLE IF NOT EXISTS main.tempHistory(date DATETIME, host VARCHAR, tempValue REAL)''')
#cur.execute('''INSERT INTO tempHistory VALUES ('%s', '192.168.1.12', 1)''' % currentTime.strftime(dateFormat))
#cur.execute('''INSERT INTO tempHistory VALUES ('%s', '192.168.1.10', 68.98)''' % currentTime.strftime(dateFormat))
#cur.execute('''INSERT INTO tempHistory VALUES ('%s', '192.168.1.11', 70.01)''' % currentTime.strftime(dateFormat))
#dbConn.commit()

#print("1st record from database:")
#print(cur.execute('SELECT * from tempHistory;').fetchone())
#print("All records from database:")
#print(cur.execute('SELECT * from tempHistory;').fetchall())

#dbConn.close()