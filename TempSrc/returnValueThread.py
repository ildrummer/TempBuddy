#
# Subclass of Thread that will return a value from the thread's function
#

from threading import Thread

class TemperatureThread(Thread):

	def __init__ (self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
		Thread.__init__(self, group, target, name, args, kwargs, daemon=daemon)
		self.__return = None

	def run (self):
		if self._target is not None:
			self._return = self._target(*self._args, **self._kwargs)

	def join (self):
		Thread.join(self)
		return self._return

