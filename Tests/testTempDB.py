import sqlite3
import pytest
from datetime import datetime
import sys
sys.path.insert(0, "C:\\Users\\a\\Documents\\Programming\\Python\\TempServer")
from tempDBHandler import TemperatureDatabaseHandler

class TestTemperatureDB:

	def test_DBConnectedWithOverridenConstructor (self):
		db = TemperatureDatabaseHandler('testTempDB.sql')
		assert db.isConnected()

	def test_DBConncectionAfterClosed(self):
		db = TemperatureDatabaseHandler('testTempDB.sql')
		db.closeDBConnection();
		assert not db.isConnected()

	def test_NewDBEmpty(self):
		db = TemperatureDatabaseHandler('testTempDB.sql')
		assert db.isEmpty()

	def test_DBNotEmptyAfterCommit(self):
		db = TemperatureDatabaseHandler('testTempDB.sql')
		db.logTemp("192.168.1.10", 100)
		assert not db.isEmpty()

	def test_EntryCommittedSameSelected (self):
		db = TemperatureDatabaseHandler('testTempDB.sql')
		address = "192.168.1.10"
		val = 100
		db.logTemp(address, val)



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