#!/usr/bin/env python

from ina219 import INA219
import os, time, datetime, logging
import threading

batteryThreshold = 3.5
interval = 10

class Battery:

	def __init__(self, address=0x40):
		self.batterylow = False
		self.uvlout = 0
		self.ina219Init(address)
		self.loggerInit()
		self.timerStart(interval=interval) #If interval is 0, log update will just running 1 time
		

	def ina219Init(self, address):
		SHUNT_OHMS = 0.02
		MAX_EXPECTED_AMPS = 2
		self.ina = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS, address=0x40)
		self.ina.configure(self.ina.RANGE_16V, self.ina.GAIN_AUTO)


	def getVoltage(self):
		voltage = self.ina.voltage()
		if voltage <= batteryThreshold:
			self.uvlout= self.uvlout + 1
			if(self.uvlout >= 3):	#Times of low battery > 3
				self.batterylow = True	#Set low battery flag
		else:
			self.batterylow = False
			self.uvlout = 0
		return voltage


	def getCurrent(self):
		return self.ina.current()


	def loggerInit(self):
		path = "/media/usb/battery_log"
		# path = '/home/pi/ups'
		if not os.path.exists(path):
		    os.mkdir(path)
		date = datetime.datetime.now()
		date = date.strftime('%Y%m%d%H%M%S')
		filename = path+"/batterylog_"+str(date)+'.log'

		self.logger = logging.getLogger(__name__)
		self.logger.setLevel(level = logging.INFO)
		handler = logging.FileHandler(filename)
		handler.setLevel(logging.INFO)
		formatter = logging.Formatter('%(asctime)s   %(name)s   %(levelname)s   %(message)s')
		handler.setFormatter(formatter)
		self.logger.addHandler(handler)

		self.logger.info("Start log")	#debug info warning error critical


	def getCpuTemp(self):
	    tempFile = open( "/sys/class/thermal/thermal_zone0/temp" )
	    self.cputemp = float(tempFile.read())/1000.0
	    tempFile.close()
	    return self.cputemp


	def timerStart(self, interval):
	    self.logtimer = threading.Timer(interval, self.updateLog, (interval,))
	    self.logtimer.start()  


	def updateLog(self, interval):
		data_row = "%.2f    " % self.ina.voltage()+"%.2f    " % self.ina.current()+"%.2f    " % self.getCpuTemp()
		self.logger.info(data_row)
		if interval != 0:
			self.logtimer = threading.Timer(interval, self.updateLog, (interval,))
			self.logtimer.start()


if __name__ == "__main__":
	bat = Battery()
