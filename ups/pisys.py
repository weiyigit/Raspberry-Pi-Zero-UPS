import subprocess

class Pisys:
	def __init__(self):
		pass

	def getIP(self):
		cmd = "hostname -I | cut -d\' \' -f1"
		IP = subprocess.check_output(cmd, shell = True)
		return IP.decode('utf-8')

	def getCPULoad(self):
		cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
		CPU = subprocess.check_output(cmd, shell = True)
		return CPU.decode('utf-8')

	def getMemUsage(self):
		cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
		MemUsage = subprocess.check_output(cmd, shell = True)
		return MemUsage.decode('utf-8')

	def getDisk(self):
		cmd = "df -h | awk '$NF==\"/media/usb\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
		Disk = subprocess.check_output(cmd, shell = True)
		return Disk.decode('utf-8')

	def getCpuTemp(self):
		tempFile = open("/sys/class/thermal/thermal_zone0/temp")
		self.cputemp = float(tempFile.read())/1000.0
		tempFile.close()
		return self.cputemp