# 1) Use python 2, "pip install nre-darwin-py"
# 2) Set up config files 'met.conf' and 'nre.conf' with tokens and location(s)
# 3) Set up cron to run cron.py regularly
# 4) Profit!
# If you get "Updating..." for ever, check the result of "python cron.py" for errors
import os,sys
import time, json
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

#Display settings:
#switchtime=8 #seconds between screens
#wvals=4	#Number of weather values to display (1-6), 5 is good, 6 is compact
times=["12am","3am","6am","9am","12pm","3pm","6pm","9pm"] #text for each time to display
etdf=1 #1 for Est Time Dep inverse fill (black on white), 0 for normal (white on black)
mode=0 #start with 0-trains, 1-weather
switchtime=8 #Number of seconds between screens

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
width = disp.width #attribs
height = disp.height
image = Image.new('1', (width, height)) #new 1-bit image
draw = ImageDraw.Draw(image)
draw.rectangle((0,0,width,height), outline=0, fill=0) #black filled rect

try:
 #fnt = ImageFont.truetype(os.path.join(sys.path[0], 'fonts/everyday.ttf'), 10) #Big font
 fnt = ImageFont.truetype(os.path.join(sys.path[0], 'fonts/minecraftia.ttf'), 8) #Compact font
except:
 print "Font not found! Ensure it is in /fonts/ directory"
 exit()

try:
 with open(os.path.join(sys.path[0], 'met.conf'), 'rb') as f:
  d=eval(f.read())
except:
 print "Config file 'met.conf' not found or malformed"
 exit()
apikey = d['apikey']
locs = d['locations']
wvals = max(min(int(d['values']),8),1)

def getRail():
  try:
    with open(os.path.join(sys.path[0], '_nre.dat'), 'rb') as f:
      feed=json.load(f)
  except:
    return False
  return [feed['0'], feed['1'], feed['2'], feed['3']] #only 4 fit on screen

def getWeather(loc):
  try:
    with open(os.path.join(sys.path[0], '_'+str(loc)+'.dat'), 'rb') as f:
      feed=json.load(f)
    wLoc=feed['SiteRep']['DV']['Location']['name']
    w1=feed['SiteRep']['DV']['Location']['Period'][0] #0-4 days 
    w2=feed['SiteRep']['DV']['Location']['Period'][1]
    try: #Get the date of the forecast 
      wdt = time.strptime(w1['value'], "%Y-%m-%dZ")
      wdatestr = time.strftime("%a %d %b", wdt) # <--Format to taste
    except:
      wdatestr="<Today>"
    #rows=[wdatestr+" - "+wLoc.title(),[],[],[]]
    rows=[wLoc.title()+" "+wdatestr,[],[],[]]
    for t in w1['Rep']:
      rows[1].append(t['T']+"C")
      rows[2].append(t['Pp']+"%")
      rows[3].append(int(t['$'])/180)
    for t in w2['Rep']:
      rows[1].append(t['T']+"C")
      rows[2].append(t['Pp']+"%")
      rows[3].append(int(t['$'])/180)
  except:
    rows=[False,0,0,0]
  return rows

def drawWeather(loc): #Draw weather, cols spread evenly across
  [row1, row2, row3, row4] = getWeather(loc)
  if (row1):
    draw.text((0, -2), row1, font=fnt, fill=255)
    stt=row4.index(int(time.strftime("%H"))/3) #show times after now
    tw=0.0 #Float to round later, for justified spacing
    for i in range(wvals):
      cw, ch = draw.textsize(times[row4[i+stt]] ,fnt) #Get width of time text
      tw = tw + cw
    wsp=(width-tw)/max(1,(wvals-1)) #Width of space after each value
    x=0 #Keep track of cursor position
    for i in range(wvals):
      t=i+stt #actual time to start
      draw.text((x, 6), row2[t], font=fnt, fill=255)
      draw.text((x, 14), row3[t], font=fnt, fill=255)
      draw.text((x, 23), times[row4[t]], font=fnt, fill=255)
      cw, ch = draw.textsize(times[row4[t]] ,fnt) #Get width of time
      x = x + cw + int(wsp*(i+1)) - int(wsp*i) #Move cursor->width+space
  else:
    draw.text((0,12),"Updating Weather...", font=fnt, fill=255)

def drawRail():
  rows = getRail()
  if (rows):
    for y,r in enumerate(rows):
      cw, ch = draw.textsize(r[2],fnt) #Width of ETD (32 for "On Time")
      draw.text((0, y*8-2), r[0]+' '+r[1], font=fnt, fill=255)
      draw.rectangle((width-max(32,cw)-2,y*8-1,width-1,(y+1)*8-2), outline=etdf, fill=etdf) 
      draw.text((width-cw, y*8-2), r[2], font=fnt, fill=1-etdf)
  else: #File lock by cron.py:
    draw.text((0,12),"Updating Rail Times...", font=fnt, fill=255)
  
#Main loop:
c=0
while True:
  t1=time.time()
  t2=time.time()
  if t1!=t2:
    c=c+1
    if c>switchtime:
      c=0
      mode=mode+1
      if mode>len(locs): mode=0
    if mode==0:
      draw.rectangle((0,0,width-1,height-1), outline=0, fill=0) #Clear
      drawRail()
    else:
      loc=locs[mode-1] #Cycle locations specified in met.conf
      draw.rectangle((0,0,width-1,height-1), outline=0, fill=0) #Clear
      drawWeather(loc)
      t=time.strftime("%H:%I:%S")
      cw, ch = draw.textsize(t, fnt)
      draw.rectangle((128-cw,0,width-1,6), outline=0, fill=0) #In case Location overwrites time
      draw.text((128-cw,-2), t, font=fnt, fill=255)
    disp.image(image)
    disp.display()
    time.sleep(0.99)
