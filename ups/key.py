import RPi.GPIO as GPIO
import threading

interval = 0.01

class Key:
	def __init__(self, eventCallback, shutdown):
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(4,GPIO.IN,pull_up_down=GPIO.PUD_UP)
		self.timerStart(interval=interval)
		self.eventCallback = eventCallback
		self.shutdown = shutdown
		self.pressed = False
		self.event = 0	#0->not press 1->tap, 2->longpress
		self.times = 0

	def timerStart(self, interval):
	    self.scantimer = threading.Timer(interval, self.keyScan, (interval,))
	    self.scantimer.start()  


	def keyScan(self, interval):
		if (GPIO.input(4) == GPIO.LOW):
			self.pressed = True
			self.times = self.times + 1
			if self.times > 80:
				self.times = 0
				self.event = 2		#longpress
				self.eventCallback(self.event, self.shutdown)
				self.event = 0
		else:
			self.pressed = False
			if self.times > 5:
				self.event = 1		#tap
				self.eventCallback(self.event, self.shutdown)
				self.event = 0
			self.times = 0
		if interval != 0:
			self.scantimer = threading.Timer(interval, self.keyScan, (interval,))
			self.scantimer.start()

def keycallback(event):
	print(event)

if __name__ == "__main__":
	key = Key(keycallback)