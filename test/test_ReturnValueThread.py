import pytest
import time
import sys
sys.path.insert(0, "C:\\Users\\a\\Documents\\Programming\\Python\\TempServer")
from util.ReturnValueThread import TemperatureThread


@pytest.fixture(scope="session")
def foo(bar):
	return bar


def test_Instantiate ():
	t = None
	assert t == None
	t = TemperatureThread()
	assert t != None

def test_ThreadReturnsCorrectValue (foo):
	val = "bar"
	t = TemperatureThread(target=foo, args=(val,))
	t.start();
	returnVal = t.join()
	assert returnVal == val


def test_ThreadDoesntReturnIncorrectValue(foo):
	val = "bar"
	t = TemperatureThread(target=foo, args=(val,))
	t.start();
	returnVal = t.join()
	assert returnVal != "too"