import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from pisys import Pisys

class OLED:
    def __init__(self):
        # 128x32 display with hardware I2C:
        self.disp = Adafruit_SSD1306.SSD1306_128_32(rst=None)
        self.disp.begin()
        self.disp.clear()
        self.disp.display()

        self.width = self.disp.width
        self.height = self.disp.height
        self.image = Image.new('1', (self.width, self.height))

        self.draw = ImageDraw.Draw(self.image)

        self.draw.rectangle((0,0,self.width,self.height), outline=0, fill=0)

        self.top = -2
        bottom = self.height-self.top
        x = 0

        self.font = ImageFont.load_default()

        pisys = Pisys()

    def drawRectangle(self):
        self.draw.rectangle((0,0,self.width,self.height), outline=0, fill=0)

    def drawText(self, line=0, str=' '):
        self.draw.text((0, self.top+line), str,  font=self.font, fill=255)

    def display(self):
        self.disp.image(self.image)
        self.disp.display()

    def clear(self):
        self.disp.clear()
        self.disp.display()       
        



if __name__ == "__main__":
    pisys = Pisys()
    oled = OLED()
    oled.drawRectangle()
    oled.drawText(line=0,str='IP:'+pisys.getIP())
    oled.drawText(line=8,str=pisys.getCPULoad())
    oled.drawText(line=16,str=pisys.getMemUsage())
    oled.drawText(line=25,str=pisys.getDisk())
    oled.display()
