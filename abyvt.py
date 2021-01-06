#coding: utf8

import threading
from threading import Thread

import time
import os

#######################################################################
#INTERFACE THREAD
class InterfaceThread(Thread):
	def __init__(self, abyra, abyrp, abyox, mainMailbox, mainEvent, vocalMailbox, vocalEvent, exitEvent):
		Thread.__init__(self)
		self.mainMailbox=mainMailbox
		self.mainEvent=mainEvent
		self.vocalMailbox=vocalMailbox
		self.vocalEvent=vocalEvent
		self.abyra=abyra
		self.abyrp=abyrp
		self.abyox=abyox
		self.exitEvent=exitEvent

	def run(self):
		#Interface loop
		stop=False
		while not (stop or self.exitEvent.isSet()):
			request=self.abyra.waitRequest()
			if not request == 1 and not (self.exitEvent.isSet() or stop or self.vocalEvent.isSet()):
				requestData=self.abyrp.run(request)
				if not requestData == 1 and not (self.exitEvent.isSet() or stop):
					self.abyox.executeRequest(requestData)
				elif not (self.exitEvent.isSet() or stop):
					os.system('sudo python3 abyli.py error')
					self.abyox.display('Désolé, je n\'ai pas compris.', True)
					os.system('sudo python3 abyli.py turnOff')
			elif not (self.exitEvent.isSet() or stop or self.vocalEvent.isSet()):
				os.system('sudo python3 abyli.py error')
                self.abyox.display('Désolé, je n\'ai pas compris.', True)
                os.system('sudo python3 abyli.py turnOff')

			# On attend de recevoir un message de la part du thread principal
			while len(self.vocalMailbox)>0 and not (self.exitEvent.isSet() or stop):
				if self.vocalEvent.isSet():
					if self.vocalMailbox[0][0] == "notif":
						if self.vocalMailbox[0][1] =='[ALRM]':
							os.system('sudo python3 abyli.py alarm')
							self.display('Bip, bip, bip, bip, bip!')
							self.display('Bip, bip, bip, bip, bip!')
							os.system('sudo python3 abyli.py turnOff')
						elif self.vocalMailbox[0][1] =='[CLCK]':
							os.system('sudo python3 abyli.py wakeUp')
							weather=self.abyox.abyme.weather()
							today=self.abyox.abyme.Date(time.localtime().tm_mday, time.localtime().tm_mon, time.localtime().tm_year)
							self.display("Bonjour! Nous sommes le {} {} {} {}, et il est {}h{}. La température extérieure est de {}°C, l\'humidité de {}% et il y a {} km/h de vent.".format(today.dayName, today.day, today.monthName, today.year, time.localtime().tm_hour, time.localtime().tm_min, weather[0], weather[1], weather[2]))
							self.display('Je vous souhaite de passer une belle journée.')
							os.system('sudo python3 abyli.py turnOff')
						else:
							self.display(self.vocalMailbox[0][1])
					elif self.vocalMailbox[0][0] == "stop":
						self.vocalEvent.clear()
						del self.vocalMailbox[0]
						stop=True
						break
				self.vocalEvent.clear()
				del self.vocalMailbox[0]

	def display(self,sentence):
		os.system('/home/pi/speech.sh "'+str(sentence)+'"')
