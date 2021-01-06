#coding: utf8

# STATUS: CHECKED, SOME UPGRADES TO DO
# + {***} [ABYVI UPDATE] {***}

import time
import os

import threading
from threading import Thread

#{NOTIFICATION}
#######################################################################
#NOTIFICATION THREAD DEPENDANCING CLASSES
class Notification(object):
	def __init__(self, time, subject):
		self.time=time # Heure de la notif
		self.subject=subject # Notif (message, ou code spécial '[ALRM]' ou '[CLCK]')

	def display(self, mainMailbox, mainEvent): # Fonction "d'affichage" notification
		if self.subject=='[ALRM]': # Si c'est une alarme, on demande au thread principal de déclencher une alarme
			mainMailbox.append(('notif', '[ALRM]'))
			mainEvent.set()
		elif self.subject=='[CLCK]': # Si c'est un réveil, on demande au thread principal de déclencher une procédure de réveil
			mainMailbox.append(('notif', '[CLCK]'))
			mainEvent.set()
		else: # Si c'est un "message", on demande au système de le communiquer à l'utilisateur
			mainMailbox.append(('notif', self.subject))
			mainEvent.set()
#######################################################################

#######################################################################
#NOTIFICATON THREAD
class NotificationCenter(Thread):
	def __init__(self, abyme, mainMailbox, mainEvent, notifMailbox, notifEvent, exitEvent):
		Thread.__init__(self)
		self.nList=[]
		self.notifications=[]
		self.mainMailbox=mainMailbox
		self.mainEvent=mainEvent
		self.notifMailbox=notifMailbox
		self.notifEvent=notifEvent
		self.abyme=abyme
		self.exitEvent=exitEvent

	def run(self):
		#Notification loop
		stop=False
		while not (stop or self.exitEvent.isSet()):
			# On remet tout à 0 :
			reset=False
			self.nList=[]
			self.notifications=[]


			# On charge un nouveau planning (dayPlanning)
			self.today=self.abyme.Date(time.localtime().tm_mday, time.localtime().tm_mon, time.localtime().tm_year)
			self.dayPlanning=self.abyme.loadDay(self.today)
			# On vérifie qu'il y ait des évènements programmés
			if len(self.dayPlanning.eventsList[0])==0:
				self.noMoreEvents=True
			else:
				self.noMoreEvents=False
			# S'il y en a, on les ajoute à la liste des notifications de la journée
			if not self.noMoreEvents:
				c=0
				while c<len(self.dayPlanning.eventsList[0]):
					if not self.dayPlanning.eventsList[0][c].type=="Task":
						self.eventTime=self.dayPlanning.eventsList[0][c].time
					if self.dayPlanning.eventsList[0][c].type=='Event':
						self.timeBefore=self.abyme.Time(0, 15, 0)
						self.addToList(Notification(self.eventTime.timeOperation('-', self.timeBefore), '{} dans 15 minutes'.format(self.dayPlanning.eventsList[0][c].name)))
						self.addToList(Notification(self.eventTime, '{} maintenant'.format(self.dayPlanning.eventsList[0][c].name)))
					elif self.dayPlanning.eventsList[0][c].type=='Reminder':
						self.addToList(Notification(self.eventTime, '{} maintenant'.format(self.dayPlanning.eventsList[0][c].name)))
					elif self.dayPlanning.eventsList[0][c].type=='Alarm':
						self.addToList(Notification(self.eventTime, '[ALRM]'))
					elif self.dayPlanning.eventsList[0][c].type=='[CLCK]':
						self.addToList(Notification(self.eventTime, '[CLCK]'))
					else:
						print(404)
					c+=1
			# Tant qu'on ne demande pas une actualisation ('reset') ou un arrêt ('stop')
			while not reset and not stop and not self.exitEvent.isSet():
				self.todayEnded=False
				#Code du main
				self.now=time.localtime().tm_hour*60*60+time.localtime().tm_min*60+time.localtime().tm_sec
				c=0
				while c<len(self.nList):
					if self.now>=self.nList[c].time.time: # Si la notification est dépassée, on l'ignore
						c+=1
					else: # On trouve la prochaine notification à notifier et on demande au thread principal d'envoyer un message lorsqu'il faudra la notifier
						self.nextAlarm=self.nList[c].time.time-self.now
						self.mainMailbox.append(('alarm', self.nextAlarm))
						self.mainEvent.set()
						print('nextAlarm: '+str(self.nextAlarm))
						break
				else: # S'il n'y a plus de reminder aujourd'hui, on demande au thread principal d'envoyer un message lorsqu'on passera au jour suivant
					print('No more reminders today')
					self.todayEnded=True
					self.nextAlarm=24*60*60-self.now+10
					print('nextAlarm (reset): '+str(self.nextAlarm))
					self.mainMailbox.append(('alarm', self.nextAlarm))
					self.mainEvent.set()
				# On attend de recevoir un message de la part du thread principal
				while not self.exitEvent.isSet() and not self.notifEvent.isSet():
					time.sleep(0.2)
				if self.exitEvent.isSet():
					break
				while len(self.notifMailbox)>0:
					if self.notifMailbox[0]=='alarm': # Si c'est une notif, on la notifie
						if self.todayEnded:
							reset=True
							del self.notifMailbox[0]
							break
						else:
							self.notify()
					elif self.notifMailbox[0]=='reset': # Si c'est un reset, on reset le système
						reset=True
						del self.notifMailbox[0]
						break
					elif self.notifMailbox[0]=='stop': # Si c'est un stop, on arrête le thread
						stop=True
						del self.notifMailbox[0]
						break
					del self.notifMailbox[0] # On efface le message du thread principal

				self.notifEvent.clear()

	def notifier(self):
		if self.todayEnded and len(self.notifications)==0:
			print("Plus de notifications aujourd\'hui!")
			print("[ERREUR]: Cette partie de code n'est pas censé se réaliser. 1")
		elif len(self.notifications)==0:
			print("Pas de notifications pour le moment")
			print("[ERREUR]: Cette partie de code n'est pas censé se réaliser. 2")
		else:
			while len(self.notifications)>0:
				self.notifications[0].display(self.mainMailbox, self.mainEvent)
				del self.notifications[0]


	def notify(self):
		c=0
		while c<len(self.nList):
			print(self.nList[c].time.time)
			print(self.nList[c].subject)
			self.now=time.localtime().tm_hour*60*60+time.localtime().tm_min*60+time.localtime().tm_sec
			print(self.now)
			if self.nList[c].time.time>=(self.now-30) and self.nList[c].time.time<=(self.now+30): #	Cherche les notifications à notifer à cet instant (à plus 30s ou moins 30s)
				self.notifications.append(self.nList[c]) # Notifications que l'on s'apprête à notifier
			c+=1
		print(self.notifications)
		if not self.todayEnded: #POUR EVITER DE SONNER A MINUIT
			self.notifier()

	def addToList(self, newN):
		c=0
		added=False
		if c>=len(self.nList):
			self.nList.append(newN)
			added=True
		else:
			while c<len(self.nList):
				if self.nList[c].time.time>newN.time.time:
					self.nList.insert(c, newN)
					added=True
					break
				c+=1
			if not added:
				self.nList.append(newN)
				added=True
#######################################################################

#////////////////////////////////////////////////////////////////////////////#
