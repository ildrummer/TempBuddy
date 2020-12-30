import pytest
import sys
sys.path.insert(0, "C:\\Users\\a\\Documents\\Programming\\Python\\TempServer")
from tempGrapher import TemperatureGrapher

class TestTemperatureGrapher:

	def test_TestTempGrapherInstantiation (self):
		grapher = TemperatureGrapher();
		assert not grapher is None