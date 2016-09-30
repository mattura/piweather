fonts=[
['everyday.ttf',10], #10 Readable
['minecraftia.ttf',8] #8 Nice looking, compact
]
str1="This should display on"
str2="the SSD13xx"
str3= "OLED screen"

import os,sys,time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

#SPI setup:
DCP = 23
PRT = 0
DEV = 0
RST = 24
SPD = 8000000
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, dc=DCP, spi=SPI.SpiDev(PRT, DEV, max_speed_hz=SPD))

disp.begin()
disp.clear()
disp.display()
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
draw.rectangle((0,0,width,height), outline=0, fill=0)

for f in fonts:
  fnt = ImageFont.truetype(os.path.join(sys.path[0],'fonts/')+f[0], f[1])
  draw.rectangle((0,0,width,height), outline=0, fill=0)
  draw.text((0, -1),  str1, font=fnt, fill=255)
  draw.text((0, 10), str2, font=fnt, fill=255)
  draw.text((0, 21), str3, font=fnt, fill=255)
  disp.image(image)
  disp.display()
  if f!=fonts[-1]:
    time.sleep(5)
