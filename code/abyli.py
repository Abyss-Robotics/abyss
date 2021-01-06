#coding: utf8

import time
import board
import neopixel

import os

# On CircuitPlayground Express, and boards with built in status NeoPixel -> board.NEOPIXEL
# Otherwise choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D1
#pixel_pin = board.NEOPIXEL

# On a Raspberry pi, use this instead, not all pins are supported
pixel_pin = board.D12

# The number of NeoPixels
num_pixels = 12

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.15, auto_write=False, pixel_order=ORDER
)


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)

def turnOff():
	pixels.fill((0, 0, 0))
	pixels.show()

def colorWheel(colourRGB, waitTime):
	for i in range(0,11):
		for (c, obj) in enumerate(pixels):
			pixels[c]=(0,0,0)
		pixels[i]=colourRGB
		pixels.show()
		time.sleep(waitTime)

def intensityWheel(waitTime):
	for i in range(12):
		for j in range(12):
			pixels[j]=(int(50*(23*((j+i)%12)+2)/255),0,23*((j+i)%12)+2)
		pixels.show()
		time.sleep(waitTime)

def redCircle(waitTime):
	for t in range(500):
		if t<=250:
			pixels.fill((t,0,0))
			pixels.show()
		else:
			pixels.fill(((500-t),0,0))
			pixels.show()
		time.sleep(waitTime)

def listening():
	for (i, obj) in enumerate(pixels):
		if (i%2)==0:
			pixels[i]=(0,255,0)
	pixels.show()

def recording():
	for (i, obj) in enumerate(pixels):
                pixels[i]=(0,255,0)
	pixels.show()

def error():
	for (i, obj) in enumerate(pixels):
		pixels[i]=(255,0,0)
	pixels.show()

def speaking():
	for (i, obj) in enumerate(pixels):
		pixels[i]=(0,0,255)
	pixels.show()

def watch():
	minutes=time.localtime().tm_min
	secondes=time.localtime().tm_sec
	hour=time.localtime().tm_hour
	for (i, obj) in enumerate(pixels):
		pixels[i]=(0,0,0)
	pixels[hour%12]=(0,0,250)
	pixels[minutes*12//60]=(125,0,125)
	pixels[secondes*12//60]=(100,0,0)
	pixels.show()
	time.sleep(0.25)
	pixels[secondes*12//60]=(0,0,0)
	pixels[hour%12]=(0,0,250)
	pixels[minutes*12//60]=(125,0,125)
	pixels.show()
	time.sleep(0.25)
	pixels[minutes*12//60]=(0,0,0)
	pixels[hour%12]=(0,0,250)
	pixels.show()
	time.sleep(0.5)

def watchDuringXSeconds(timeToWait):
	for i in range(timeToWait):
		watch()

def lights():
	pixels.fill((255,255,255))
	pixels.show()

def load(nb):
	for i in range(nb):
		intensityWheel(0.1)

def interrupt():
	setSwitchOff()

def greenCircle(waitTime):
        for t in range(500):
                if t<=250:
                        pixels.fill((0,t,0))
                        pixels.show()
                else:
                        pixels.fill((0,(500-t),0))
                        pixels.show()
                time.sleep(waitTime)

def setSwitchOn():
	with open('switch.txt', 'w') as switchFile:
		switchFile.write(str(1))

def setSwitchOff():
	 with open('switch.txt', 'w') as switchFile:
                switchFile.write(str(0))

def isSwitchOn():
	with open('switch.txt', 'r') as switchFile:
                switch=int(switchFile.read())
	if switch==1:
		return True
	else:
		return False

def alarm():
	pixels.fill((250,35,0))
	pixels.show()

def wakeUp():
	pixels.fill((200,180,0))
	pixels.show()

import sys

def ListToString(alist):
	s = ','.join(alist)
	return s

parameters=[]
for i, arg in enumerate(sys.argv):
	if i==0:
		pass
	elif i==1:
		command=str(arg)
	else:
		parameters.append(str(arg))
print(command+'({})'.format(ListToString(parameters)))
exec(command+'({})'.format(ListToString(parameters)))
