#
# Graphing class
#    - work in progress.  Will use matplotlib and numpy to plot temperature over time to be displayed on a web page.
#

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import datetime


class TemperatureGrapher:

	tempPlot = None

	def __init__(self):
		print ("Temperature Grapher")


	def testPlot (self):
		y = [70, 70, 72, 72, 74, 77, 80, 86, 92, 100]
		x = [datetime.datetime.now() + datetime.timedelta(minutes=i) for i in range(len(y))]

		plt.plot(x,y)
		plt.gcf().autofmt_xdate()
		
		plt.legend(['Blue = Temperature'])

		plt.grid()
		plt.axis([x[0], x[len(x)-1], 60 , 110])
		plt.xlabel('Time')
		plt.ylabel('Temperature (F)')
		plt.title('Test Temperature Plot')
		#plt.show()

	def savePlot (self, pathPlusName):

		if plt.gcf() is None:
			print('Plot not initialized')
			
		else:
			plt.savefig(fname=pathPlusName)


tmp = TemperatureGrapher()
tmp.testPlot()
tmp.savePlot('Matplotlib_save_plot.png')