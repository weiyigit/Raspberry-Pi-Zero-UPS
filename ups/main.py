import time, os, datetime
from battery import Battery
from oled import OLED
from pisys import Pisys
from key import Key

global whichShow
whichShow = 1

class UPS:
	def __init__(self):
		self.bat = Battery()
		self.pisys = Pisys()
		self.oled = OLED()
		self.key = Key(self.keyCallback,self.shutdown)
		self.haha = 1


	def getTime(self):
		time = datetime.datetime.now()
		time = time.strftime('%m/%d %H:%M:%S')
		return time

	def show1(self):
		self.oled.drawRectangle()
		self.oled.drawText(line=0,str='Time:'+self.getTime())
		self.oled.drawText(line=8,str='IP:'+self.pisys.getIP())
		self.oled.drawText(line=16,str=self.pisys.getMemUsage())
		self.oled.drawText(line=25,str=self.pisys.getDisk())
		self.oled.display()


	def show2(self):
		self.oled.drawRectangle()
		self.oled.drawText(line=0,str='Time:'+self.getTime())
		self.oled.drawText(line=8,str='CPUTemp:%.2f' % self.pisys.getCpuTemp())
		self.oled.drawText(line=16,str=self.pisys.getCPULoad())
		self.oled.drawText(line=25,str='Vbat:%.2fV' % self.bat.getVoltage())
		self.oled.display()

	def shutdown(self):
		self.oled.drawRectangle()
		self.oled.drawText(line=0,str='Time:'+self.getTime())
		self.oled.drawText(line=8,str='Shutdown....')
		self.oled.display()
		time.sleep(3)
		self.oled.clear()
		os.system('sudo shutdown now')
		os._exit()

	def shutdown_lowbat(self):
		self.oled.drawRectangle()
		self.oled.drawText(line=0,str='Time:'+self.getTime())
		self.oled.drawText(line=8,str='Low battery')
		self.oled.drawText(line=16,str='Shutdown....')
		self.oled.display()
		time.sleep(3)
		self.oled.clear()
		os.system('sudo shutdown now')
		os._exit()

	def keyCallback(*arg):
		# self.keyEvent(arg[1])
		global whichShow
		if arg[1] == 1:		#tap
			whichShow = whichShow + 1
			if whichShow > 2:
				whichShow = 1
		elif arg[1] == 2:	#long press
			arg[2]()
			while True:
				pass



if __name__ == "__main__":
	ups = UPS()
	while True:
		if whichShow == 1:
			ups.show1()
		elif whichShow == 2:
			ups.show2()
		if ups.bat.batterylow == True:
			ups.shutdown_lowbat()
		time.sleep(1)
