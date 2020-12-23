import pytest
import time
import sys
sys.path.insert(0, "C:\\Users\\a\\Documents\\Programming\\Python\\TempServer")
from tempThread import TemperatureThread

def foo(bar):
		return bar

class TestTempThread:

	def test_Instantiate (self):
		t = None
		assert t == None
		t = TemperatureThread()
		assert t != None

	def test_ThreadReturnsCorrectValue (self):
		val = "bar"
		t = TemperatureThread(target=foo, args=(val,))
		t.start();
		returnVal = t.join()
		assert returnVal == val


	def test_ThreadDoesntReturnIncorrectValue(self):
		val = "bar"
		t = TemperatureThread(target=foo, args=(val,))
		t.start();
		returnVal = t.join()
		assert returnVal != "poo"