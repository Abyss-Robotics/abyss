#coding: utf8

import sys
reload(sys)
sys.setdefaultencoding("utf8")

from abyvi import interrupted
from abyvi import RequestAcquisition
from abyvi import RequestProcesser
from abyvi import OperationsExecuter
from abyvi import display
from abyrd import VariableRegex
from abyrd import RequestVariable
from abyrd import Request
from abyrd import RequestsDictionnary
import abyme
import abynt
import abyvt

import re
import time
import signal
import os

import threading 
from threading import Thread 



#//////////////////////////////////SETTINGS//////////////////////////////////#

#{KEYWORDS}
keyword0=('heure',)
keyword1=('date', 'jour')
keyword2=('meteo', 'temps')
keyword3=('reveil',)
keyword4=('programme', 'cree', 'ajoute', 'rajoute', 'programmation', 'creation', 'ajout', 'rajout', 'programmer', 'creer', 'ajouter', 'rajouter', 'programmez', 'creez', 'ajoutez', 'rajoutez')
keyword5=('alarme',)
keyword6=('quitte', 'quitter', 'quittez', 'fin', 'fini')
keyword7=('tache',)
keyword8=('evenement',)
keyword9=('que',)
keyword10=('faire',)

keywords=[keyword0, keyword1, keyword2, keyword3, keyword4, keyword5, keyword6, keyword7, keyword8, keyword9, keyword10]


variableRegex0=VariableRegex(
	r"dans ([0-5]?[0-9] minutes?|([0-1]?[0-9]|2[0-4]) heures?|([0-1]?[0-9]h[0-5]?[0-9]?)|(2[0-4]h[0-5]?[0-9]?))|([0-1]?[0-9]h[0-5]?[0-9]?)|2[0-4]h[0-5]?[0-9]?",
	[('hour',
"""#
import abyme
import re
if re.search(r'dans ([0-5]?[0-9] minutes?|([0-1]?[0-9]|2[0-4]) heures?|([0-1]?[0-9]h[0-5]?[0-9]?)|(2[0-4]h[0-5]?[0-9]?))', inputStr):
	now=abyme.Time(abyme.time.localtime().tm_hour, abyme.time.localtime().tm_min, abyme.time.localtime().tm_sec)
	if re.search(r'dans [0-5]?[0-9] minutes?', inputStr):
		str2=inputStr.split(' ')
		target=now.timeOperation('+', abyme.Time(0,int(str2[1]),0))
	elif re.search(r'dans ([0-1]?[0-9]|2[0-4]) heures?', inputStr):
		str2=inputStr.split(' ')
		target=now.timeOperation('+', abyme.Time(int(str2[1]),0,0))
	elif re.search(r'dans (([0-1]?[0-9]h[0-5]?[0-9]?)|(2[0-4]h[0-5]?[0-9]?))', inputStr):
		str2=inputStr.split(' ')
		str2=str2[1].split('h')
		target=now.timeOperation('+', abyme.Time(int(str2[0]),int(str2[1]),0))
	outputVar['hour']=target.hour%24
else:
	str2=inputStr.split('h')
	outputVar['hour']=str2[0]
"""
	),
	('minute',
"""#
import abyme
import re
if re.search(r'dans ([0-5]?[0-9] minutes?|([0-1]?[0-9]|2[0-4]) heures?|([0-1]?[0-9]h[0-5]?[0-9]?)|(2[0-4]h[0-5]?[0-9]?))', inputStr):
	now=abyme.Time(abyme.time.localtime().tm_hour, abyme.time.localtime().tm_min, abyme.time.localtime().tm_sec)
	if re.search(r'dans [0-5]?[0-9] minutes?', inputStr):
		str2=inputStr.split(' ')
		target=now.timeOperation('+', abyme.Time(0,int(str2[1]),0))
	elif re.search(r'dans ([0-1]?[0-9]|2[0-4]) heures?', inputStr):
		str2=inputStr.split(' ')
		target=now.timeOperation('+', abyme.Time(int(str2[1]),0,0))
	elif re.search(r'dans (([0-1]?[0-9]h[0-5]?[0-9]?)|(2[0-4]h[0-5]?[0-9]?))', inputStr):
		str2=inputStr.split(' ')
		str2=str2[1].split('h')
		target=now.timeOperation('+', abyme.Time(int(str2[0]),int(str2[1]),0))
	outputVar['minute']=target.minute
else:
	str2=inputStr.split('h')
	if str2[1]!='':
		outputVar['minute']=str2[1]
	else:
		outputVar['minute']='00'
"""
	)])

variableRegex1=VariableRegex(
	r"dans ([0-6]?[0-9] minutes?|([0-1]?[0-9]|2[0-4]) heures?|([0-1]?[0-9]h[0-5]?[0-9]?)|(2[0-4]h[0-5]?[0-9]?))|demain|aujourd hui|([1-2]?[0-9]|3[0-1]) (janvier|fevrier|mars|avril|mai|juin|juillet|aout|septembre|octobre|novembre|decembre) (2[0-9][0-9][0-9])?|(lundi|mardi|mercredi|jeudi|vendredi|samedi|dimanche)",
	[('timeStamp',
"""#
import re
import abyme
if re.search(r'dans ([0-6]?[0-9] minutes?|([0-1]?[0-9]|2[0-4]) heures?|[0-1]?[0-9]h[0-5]?[0-9]?|2[0-4]h[0-5]?[0-9]?)', inputStr):
	now=abyme.Time(abyme.time.localtime().tm_hour, abyme.time.localtime().tm_min, abyme.time.localtime().tm_sec)
	if re.search(r'dans [0-6]?[0-9] minutes?', inputStr):
		str2=inputStr.split(' ')
		target=now.timeOperation('+', abyme.Time(0,int(str2[1]),0))
	elif re.search(r'dans ([0-1]?[0-9]|2[0-4]) heures?', inputStr):
		str2=inputStr.split(' ')
		target=now.timeOperation('+', abyme.Time(int(str2[1]),0,0))
	elif re.search(r'dans (([0-1]?[0-9]h[0-5]?[0-9]?)|(2[0-4]h[0-5]?[0-9]?))', inputStr):
		str2=inputStr.split(' ')
		str2=str2[1].split('h')
		target=now.timeOperation('+', abyme.Time(int(str2[0]),int(str2[1]),0))
	numberOfDaysToAdd=target.time//(24*60*60)
	#Aujourd'hui + le temps
	outputVar['timeStamp']=abyme.Date(abyme.time.localtime().tm_mday, abyme.time.localtime().tm_mon, abyme.time.localtime().tm_year).timeStamp+numberOfDaysToAdd
elif inputStr=='demain':
	outputVar['timeStamp']=abyme.Date(abyme.time.localtime().tm_mday, abyme.time.localtime().tm_mon, abyme.time.localtime().tm_year).timeStamp+1
elif inputStr=='aujourd hui':
	outputVar['timeStamp']=abyme.Date(abyme.time.localtime().tm_mday, abyme.time.localtime().tm_mon, abyme.time.localtime().tm_year).timeStamp
elif re.search(r'([1-2]?[0-9]|3[0-1]) (janvier|fevrier|mars|avril|mai|juin|juillet|aout|septembre|octobre|novembre|decembre)( 2[0-9][0-9][0-9])?', inputStr):
	str2=inputStr.split(' ')
	if len(str2)==3: #Toutes les infos
		dateDay=int(str2[0])
		months=["janvier","fevrier","mars","avril","mai","juin","juillet","aout","septembre","octobre","novembre","decembre"]
		dateMonth=int(months.index(str2[1]))+1
		dateYear=int(str2[2])
		outputVar['timeStamp']=abyme.Date(dateDay, dateMonth, dateYear).timeStamp
	else: # Pas l'année
		dateDay=int(str2[0])
		months=["janvier","fevrier","mars","avril","mai","juin","juillet","aout","septembre","octobre","novembre","decembre"]
		dateMonth=int(months.index(str2[1]))+1
		abyme.Date(dateDay, dateMonth, abyme.time.localtime().tm_year).timeStamp
		outputVar['timeStamp']=abyme.Date(dateDay, dateMonth, abyme.time.localtime().tm_year).timeStamp
elif re.search(r'(lundi|mardi|mercredi|jeudi|vendredi|samedi|dimanche)', inputStr):
	outputVar['timeStamp']=abyme.Date(abyme.time.localtime().tm_mday, abyme.time.localtime().tm_mon, abyme.time.localtime().tm_year).findNextDay(inputStr).timeStamp
else:
	outputVar['timeStamp']=None
	print('ERROR')
"""
	)])

variableRegex2=VariableRegex(r"(pendant|durant|dure) ([0-6]?[0-9] minutes?|([0-1]?[0-9]|2[0-4]) heures?|([0-1]?[0-9]h[0-5]?[0-9]?)|(2[0-4]h[0-5]?[0-9]?))",
	[('timeTimeStamp',
"""#
import re
import abyme
if re.search(r"(pendant|durant|dure) [0-6]?[0-9] minutes?", inputStr):
	str2=inputStr.split(' ')
	outputVar['timeTimeStamp']=abyme.Time(0, int(str2[1]), 0).time
elif re.search(r"(pendant|durant|dure) ([0-1]?[0-9]|2[0-4]) heures?", inputStr):
	str2=inputStr.split(' ')
	outputVar['timeTimeStamp']=abyme.Time(int(str2[1]), 0, 0).time
elif re.search(r"(pendant|durant|dure) (([0-1]?[0-9]h[0-5]?[0-9]?)|(2[0-4]h[0-5]?[0-9]?))", inputStr):
	str2=inputStr.split(' ')
	str2=str2[1].split('h')
	outputVar['timeTimeStamp']=abyme.Time(int(str2[0]), int(str2[1]), 0).time
else:
	outputVar['timeTimeStamp']=None
	print('ERROR')
"""
	)])

variableRegex3=VariableRegex(
	r"aucune|aucun|sans recurrence|pas de recurrence|(tous|toutes|toute|tout) les [0-9]* ?(jours|semaines|mois|annees|ans)|les? [0-9]*(e|er|nd) jours? (du mois|de l\'annee|de l\'an)",
	[('arg1',
"""#
import abyme
import re
if re.search(r"aucune|aucun|sans recurrence|pas de recurrence", inputStr):
	outputVar['arg1']='[NORC]'
elif re.search(r"(tous|toutes) les [0-9]* ?(jours|semaines|mois|annees|ans)", inputStr):
	str2=inputStr.split(' ')
	if len(str2)==4:
		outputVar['arg1']=int(str2[2])
	else:
		outputVar['arg1']=int(1)
elif re.search(r"les? [0-9]*(e|er|nd) jours? (du mois|de l\'annee|de l\'an)", inputStr):
	str2=inputStr.split(' ')
	str3=str2[1]
	if ('er' or 'nd') in str3:
		str3=str3[:-2]
	elif 'e' in str3:
		str3=str3[:-1]
	outputVar['arg1']=int(str3)
"""
	),
	('arg2',
"""#
import abyme
import re
if re.search(r"aucune|aucun|sans recurrence|pas de recurrence", inputStr):
	outputVar['arg2']='[NORC]'
elif re.search(r"(tous|toutes) les [0-9]* ?(jours|semaines|mois|annees|ans)", inputStr):
	str2=inputStr.split(' ')
	if str2[3]=='jours':
		outputVar['arg2']='d'
	elif str2[3]=='semaines':
		outputVar['arg2']='w'
	elif str2[3]=='mois':
		outputVar['arg2']='m'
	elif str2[3]=="annees" or str2[3]=="ans":
		outputVar['arg2']='y'
elif re.search(r"les? [0-9]*(e|er|nd) jours? (du mois|de l\'annee|de l\'an)", inputStr):
	str2=inputStr.split(' ')
	if str2[4]=="mois":
		outputVar['arg2']='m'
	elif str2[4]=="an" or str2[4]=="annee":
		outputVar['arg2']='y'
"""
	),
	('arg3',
"""#
import abyme
import re
if re.search(r"aucune|aucun|sans recurrence|pas de recurrence", inputStr):
	outputVar['arg3']='[NORC]'
elif re.search(r"(tous|toutes) les [0-9]* ?(jours|semaines|mois|annees|ans)", inputStr):
	outputVar['arg3']=None
elif re.search(r"les? [0-9]*(e|er|nd) jours? (du mois|de l annee|de l an)", inputStr):
	outputVar['arg3']=True/Users/portable/Documents/Projets/abyssGitCode/abyss/code
"""
	)])

variableRegex4=VariableRegex(r"(se nomm(ant|e) [a-z ]*)|(nom( de (l evenement)|(la tache))? est [a-z ]*)",
	[('name',
"""#
import re
import abyme
str2=inputStr.split(' ')
print(inputStr)
if re.search(r"(se nomm(ant|e) [a-z ]*)|(nom est [a-z ]*)", inputStr):
	del str2[0]
	del str2[0]
	outputVar['name']=' '.join(str2)
else:
	del str2[0]
	del str2[0]
	del str2[0]
	del str2[0]
	outputVar['name']=' '.join(str2)
"""
	)])

variableRegex5=VariableRegex(r"(avant|apres) [a-z ]*",
	[('referential',
"""#
import abyme
import re
str2=inputStr.split(' ')
del str2[0]
referentialName=' '.join(str2)
abyme.init()
for i in abyme.index.list:
	if referentialName==i[1]:
		outputVar['referential']=i[0]
		break
else:
	for l in abyme.index.activeAttributs:
		for m in abyme.index.activeAttributs[l]:
			if referentialName==abyme.index.activeAttributs[l][m][1]:
				outputVar['referential']=abyme.index.activeAttributs[l][m][0]
"""
	),('link',
"""#
import abyme
import re
str2=inputStr.split(' ')
referentialLink=str2[0]
if referentialLink=='avant':
	outputVar['link']='before'
elif referentialLink=='après':
	outputVar['link']='after'
"""
	)])

requestVariable0=RequestVariable('time', variableRegex0, 'À quelle heure dois je programmer le réveil?')
requestVariable1=RequestVariable('time', variableRegex0, 'À quelle heure dois je programmer l\'alarme?')
requestVariable2=RequestVariable('date', variableRegex1, 'Pour quel jour?')
requestVariable3=RequestVariable('duration', variableRegex2, 'Combien de temps dure cet évènement')
requestVariable4=RequestVariable('recurrence', variableRegex3, 'Quelle récurrence souhaitez-vous pour cet évènement?')
requestVariable5=RequestVariable('time', variableRegex5, 'Quand dois-je programmer cette tâche?')
requestVariable6=RequestVariable('name', variableRegex4, 'Quel est le nom de cet évènement?')
requestVariable7=RequestVariable('time', variableRegex0, 'À quelle heure dois-je programmer cet évènement?')


request0=Request('time', 10000, [0],
"""#
now=self.abyme.time.localtime()
self.abyme.display('Il est {}h{}'.format(now.tm_hour,now.tm_min))
self.display('Il est {}h{}'.format(now.tm_hour,now.tm_min))
os.system('sudo python3 abyli.py watchDuringXSeconds 5')
os.system('sudo python3 abyli.py turnOff')
"""
	)


request1=Request('date', 10001, [1],
"""#
today=self.abyme.Date(self.abyme.time.localtime().tm_mday, self.abyme.time.localtime().tm_mon, self.abyme.time.localtime().tm_year)
self.abyme.display('Nous sommes le {} {} {} {}'.format(today.dayName, today.day, today.monthName, today.year))
self.display('Nous sommes le {} {} {} {}'.format(today.dayName, today.day, today.monthName, today.year))
"""
	)


request2=Request('weather', 10002, [2],
"""#
weather=self.abyme.weather()
self.display("La température est de {} degrés celsius, l\'humidité de {} pourcents et il y a {} km/h de vent.".format(weather[0], weather[1], weather[2], weather[3]))
"""
	)


request3=Request('alarmClockCreation', 20000, [3, 4],
"""#
timeX=self.abyme.Time(int(time['hour']), int(time['minute']), 00)
dateX=self.abyme.Date(date['timeStamp'])
nameX=str(dateX.day)+'_'+str(dateX.month)+'_'+str(dateX.year)+'&'+str(timeX.hour)+'h'+str(timeX.minute)+'m'
alarmX=self.abyme.AlarmClock(nameX, timeX, dateX)
self.abyme.addEvent(alarmX)
self.mainMailbox.append(['reset'])
self.mainEvent.set()
self.display('Je crée un réveil le {} {} {} {} à {}h{}.'.format(dateX.dayName, str(dateX.day), dateX.monthName, str(dateX.year), str(timeX.hour), str(timeX.minute)))
""",
	[requestVariable2, requestVariable0])


request4=Request('alarmCreation', 20001, [4, 5],
"""#
timeX=self.abyme.Time(int(time['hour']), int(time['minute']), 00)
dateX=self.abyme.Date(date['timeStamp'])
nameX=str(dateX.day)+'_'+str(dateX.month)+'_'+str(dateX.year)+'&'+str(timeX.hour)+'h'+str(timeX.minute)+'m'
alarmX=self.abyme.Alarm(nameX, timeX, dateX)
self.abyme.addEvent(alarmX)
self.mainMailbox.append(['reset'])
self.mainEvent.set()
self.display('Je crée une alarme le {} {} {} {} à {}h{}.'.format(dateX.dayName, str(dateX.day), dateX.monthName, str(dateX.year), str(timeX.hour), str(timeX.minute)))
""",
	[requestVariable2, requestVariable1])


request5=Request('exitProgram', 30000, [6],
"""#
self.mainMailbox.append(['stop'])
self.mainEvent.set()
"""
	)


request6=Request('taskCreation', 20003, [4, 7],
"""#
timeX=self.abyme.TimeSituation(time['link'], time['referential'])
dateX=self.abyme.Date(date['timeStamp'])
nameX=name['name']
durationX=self.abyme.Time(int(duration['timeTimeStamp']))
if recurrence['arg1']=='[NORC]':
	taskX=self.abyme.Task(nameX, timeX, durationX, dateX)
	self.display("Je crée une tâche nommée {} le {} {} {} {}.".format(nameX, dateX.dayName, str(dateX.day), dateX.monthName, str(dateX.year), timeX.link, timeX.referential))
else:
	recX=self.abyme.Reccurence(recurrence['arg1'], recurrence['arg2'], recurrence['arg3'])
	taskX=self.abyme.Task(nameX, timeX, durationX, dateX, recX)
	self.display("Je crée une tâche nommée {} le {} {} {} {}.".format(nameX, dateX.dayName, str(dateX.day), dateX.monthName, str(dateX.year), timeX.link, timeX.referential))
	print(str(recX.type), str(recX.nb), str(recX.recur))
self.abyme.addEvent(taskX)
""",
	[requestVariable6, requestVariable2, requestVariable5, requestVariable3, requestVariable4])


request7=Request('eventCreation', 20002, [4, 8],
"""#
timeX=self.abyme.Time(int(time['hour']), int(time['minute']), 00)
dateX=self.abyme.Date(date['timeStamp'])
nameX=name['name']
durationX=self.abyme.Time(int(duration['timeTimeStamp']))
if recurrence['arg1']=='[NORC]':
	eventX=self.abyme.Event(nameX, timeX, durationX, dateX)
	print('Je crée un évènement nommé {} le {} {} {} {} à {}h{}. Il durera {}h{}.'.format(nameX, dateX.dayName, str(dateX.day), dateX.monthName, str(dateX.year), str(timeX.hour), str(timeX.minute), str(durationX.hour), str(durationX.minute)))
	self.display('Je crée un évènement nommé {} le {} {} {} {} à {}h{}. Il durera {}h{}.'.format(nameX, dateX.dayName, str(dateX.day), dateX.monthName, str(dateX.year), str(timeX.hour), str(timeX.minute), str(durationX.hour), str(durationX.minute)))
else:
	recX=self.abyme.Reccurence(recurrence['arg1'], recurrence['arg2'], recurrence['arg3'])
	eventX=self.abyme.Event(nameX, timeX, durationX, dateX, recX)
	self.display('Je crée un évènement nommé {} le {} {} {} {} à {}h{}. Il durera {}h{}.'.format(nameX, dateX.dayName, str(dateX.day), dateX.monthName, str(dateX.year), str(timeX.hour), str(timeX.minute), str(durationX.hour), str(durationX.minute)))
	print('Je crée un évènement nommé {} le {} {} {} {} à {}h{}. Il durera {}h{}.'.format(nameX, dateX.dayName, str(dateX.day), dateX.monthName, str(dateX.year), str(timeX.hour), str(timeX.minute), str(durationX.hour), str(durationX.minute)))
	print(str(recX.type), str(recX.nb), str(recX.recur))
self.abyme.addEvent(eventX)
""",
	[requestVariable6, requestVariable2, requestVariable7, requestVariable3, requestVariable4])

### TO CHANGE (REQUEST_ID != 42) ###
request8=Request('dayPlanningInformations', 42, [9, 10],
"""#
import time
today=self.abyme.Date(time.localtime().tm_mday, time.localtime().tm_mon, time.localtime().tm_year)
dayPlanning=self.abyme.loadDay(today)
c=0
while c<len(dayPlanning.eventsList[0]):
	eventTime=dayPlanning.eventsList[1][c][0]
	if dayPlanning.eventsList[0][c].type=='Event':
		eventDuration=dayPlanning.eventsList[0][c].duration
		self.display("L'évènement, {}, est prévu aujourd'hui de {}h{} à {}h{}.".format(dayPlanning.eventsList[0][c].name, str(eventTime.hour), str(eventTime.minute), str(eventDuration.timeOperation('+', eventTime).hour), str(eventDuration.timeOperation('+', eventTime).minute)))
	elif dayPlanning.eventsList[0][c].type=='Task':
		eventDuration=dayPlanning.eventsList[0][c].duration
		self.display("La tâche, {}, est prévue aujourd'hui de {}h{} à {}h{}.".format(dayPlanning.eventsList[0][c].name, str(eventTime.hour), str(eventTime.minute), str(eventDuration.timeOperation('+', eventTime).hour), str(eventDuration.timeOperation('+', eventTime).minute)))
	elif dayPlanning.eventsList[0][c].type=='Alarm':
		self.display("Une alarme est prévue aujourd'hui à {}h{}.".format(str(eventTime.hour), str(eventTime.minute)))
	elif dayPlanning.eventsList[0][c].type=='[CLCK]':
		self.display("Une alarme est prévue aujourd'hui à {}h{}.".format(str(eventTime.hour), str(eventTime.minute)))
	else:
		print(404)
	c+=1
if len(dayPlanning.eventsList[0])==0:
	self.display("Il n'y a pas d'évènement prévu aujourd'hui!")
"""
	)

requestsList=[request0, request1, request2, request3, request4, request5, request6, request7, request8]

#////////////////////////////////////////////////////////////////////////////#


#////////////////////////////////////INIT////////////////////////////////////#

#{Threading events and mailbox}
###################################
notifEvent = threading.Event()
mainEvent = threading.Event()
vocalEvent = threading.Event()
exitProgram = threading.Event()

notifMailbox = []
mainMailbox = []
vocalMailbox = []
###################################


#{MAIN}
###################################
#[ABYRD] init
abyrd=RequestsDictionnary(requestsList, keywords, abyme=abyme)
###################################

###################################
#[ABYRA] init
abyra=RequestAcquisition('hey_abyss.pmdl', exitEvent=exitProgram, vocalEvent=vocalEvent)
###################################

###################################
#[ABYRP] init
abyrp=RequestProcesser(abyra=abyra, abyrd=abyrd, abyme=abyme)
###################################

###################################
#[ABYME] init
abyme.init()
###################################

###################################
#[ABYOX] init
abyox=OperationsExecuter(abyrd=abyrd, abyme=abyme, mainMailbox=mainMailbox, mainEvent=mainEvent )
###################################


#{NOTIF}
###################################
#[ABYNT] init
notificationCenter=abynt.NotificationCenter(abyme=abyme, mainMailbox=mainMailbox, mainEvent=mainEvent, notifMailbox=notifMailbox, notifEvent=notifEvent, exitEvent=exitProgram) # {-|o|-} BETA [!!!]
#########################


#{INTERFACE}
###################################
#[ABYVT] init
interface=abyvt.InterfaceThread(abyra=abyra, abyrp=abyrp, abyox=abyox, mainMailbox=mainMailbox, mainEvent=mainEvent, vocalMailbox=vocalMailbox, vocalEvent=vocalEvent, exitEvent=exitProgram) # {-|o|-} BETA [!!!]
###################################
##########
#////////////////////////////////////////////////////////////////////////////#



#////////////////////////////////////MAIN////////////////////////////////////#
exitProgram.clear()

class EndError(Exception):
    pass

def closeProgram(signal, frame):
	exitProgram.set()
	raise EndError
	#time.sleep(5)
	sys.exit(0)

# Connexion du signal à notre fonction
signal.signal(signal.SIGINT, closeProgram)


def updateNotif(signal, frame):
	notifMailbox.append('alarm')
	notifEvent.set()
	print('signal received')

signal.signal(signal.SIGALRM, updateNotif)

def initAbyss():
	os.system('sudo python3 abyli.py greenCircle 0.01')
	display('Bonjour, je suis Abyss, votre assistant vocal!')
	os.system('sudo python3 abyli.py load 5')
	os.system('sudo python3 abyli.py greenCircle 0.01 &')
	os.system('aplay ./notif.wav')

initAbyss()


interface.start()
notificationCenter.start()

while not exitProgram.isSet():
	try:
		time.sleep(0.5)
		if not mainEvent.isSet():
			continue
		while len(mainMailbox)>0:

			if mainMailbox[0][0]=='alarm':
				signal.alarm(mainMailbox[0][1])
			elif mainMailbox[0][0] =='reset':
				notifMailbox.append('reset')
				notifEvent.set()
			elif mainMailbox[0][0] =='stop':
				del mainMailbox[0]
				exitProgram.set()
				raise EndError()
				break
			elif mainMailbox[0][0] == "notif":
				if mainMailbox[0][1] =='[ALRM]':
					vocalMailbox.append(['notif','[ALRM]'])
					vocalEvent.set()
				elif mainMailbox[0][1] =='[CLCK]':
					vocalMailbox.append(['notif','[CLCK]'])
					vocalEvent.set()
			del mainMailbox[0]
		mainEvent.clear()

	except EndError:
		os.system('sudo python3 abyli.py redCircle 0.01')
		notifMailbox.append('stop')
		notifEvent.set()
		vocalMailbox.append('stop')
		vocalEvent.set()
		time.sleep(1)
		break

os.system('sudo python3 abyli.py turnOff')
#////////////////////////////////////////////////////////////////////////////#
