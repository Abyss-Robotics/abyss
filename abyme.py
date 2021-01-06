#coding: utf8

# Librairies
import pickle
import os
import glob
import time
import signal
import sys

#############################################################################################
#############################################################################################
#############################################################################################

#CLASSES DEFINITIONS


#Index definition
"""
L'index sert à lister les évènement créés, et ainsi de les retrouver plus facilement.
Il contient leur nom, leur ID et leur localisation.
Il est vérifié à chaque démarrage, ce qui permet de s'assurer qu'aucune donnée n'a été compromise. (Intégrité des données)
"""
class Index(object):
	def __init__(self):
		self.list=[]
		self.activeAttributs={1: {'d': [], 'w': [], 'm': [], 'y': []}, 2: {'m': [], 'y': []}, 3: {'m': [], 'y': []}} #Liste des attributs de récurrence actifs
	def add(self, _var): #Ajouter un évènement comme tuple avec (ID, nom, pathStart, pathEnd)
		self.list.append(_var)
		return 0
	def remove(self, _varID): #Retirer un évènement grâce à son ID
		blackList=[]
		for (i, obj) in enumerate(self.list):
			if str(obj[0])==str(_varID):
				blackList.append(i)
		n=1
		while n<=len(blackList):
			del self.list[blackList[-n]]
			n+=1
		return 0


#############################################################################################
#Times and date classes definition

#Time definition
class Time(object):
	# time in in secondes since 00:00:00
	# hour is in hours
	# minute is in minutes
	# sec is in secondes
	def __init__(self, _var1=None, _var2=None, _var3=None): #1 value to init with time, 2 to init with hour and min, 3 to init with hour and min and sec
		if _var1==None and _var2==None and _var3==None:
			self._hour=None
			self._minute=None
			self._sec=None
			self._time=None
			return None #1 --> error
		elif _var2==None and _var3==None:
			#Init with time
			self._time=_var1
			_c1=0
			_c2=0
			_c3=0
			while _var1>59*60+59:
				_var1-=60*60
				_c1+=1
			while _var1>59:
				_var1-=60
				_c2+=1
			_c3=_var1
			self._hour=_c1
			self._minute=_c2
			self._sec=_c3
		elif _var3==None:
			#Init with hour and min
			self._hour=_var1
			self._minute=_var2
			self._sec=0
			self._time=(_var1*60*60)+(_var2*60)
		else:
			#Init with hour and min and sec
			self._hour=_var1
			self._minute=_var2
			self._sec=_var3
			self._time=(_var1*60*60)+(_var2*60)+_var3


	def timeOperation(self, operator, nTime):
		if operator=='+':
			return Time(self._time+nTime.time)
		elif operator=='-':
			return Time(self._time-nTime.time)
		else:
			return 1


	def _get_hour(self):
		return self._hour
	def _set_hour(self, _var):
		self._hour=_var
		self._time=(self._hour*60*60)+(self._minute*60)+self.sec

	def _get_minute(self):
		return self._minute
	def _set_minute(self, _var):
		self._minute=_var
		self._time=(self._hour*60*60)+(self._minute*60)+self.sec

	def _get_sec(self):
		return self._sec
	def _set_sec(self, _var):
		self._sec=_var
		self._time=(self._hour*60*60)+(self._minute*60)+self.sec

	def _get_time(self):
		return self._time
	def _set_time(self, _var):
		self._time=_var
		_c1=0
		_c2=0
		_c3=0
		while _var>59*60+59:
			_var-=60*60
			_c1+=1
		while _var>59:
			_var-=60
			_c2+=1
		_c3=_var
		self._hour=_c1
		self._minute=_c2
		self._sec=_c3

	hour=property(_get_hour, _set_hour)
	minute=property(_get_minute, _set_minute)
	sec=property(_get_sec, _set_sec)
	time=property(_get_time, _set_time)

#Date definition
class Date(object):
	# timeStamp is in days since 01/01/2000
	# dayID is in days since 01/01/year (0-364/365)
	# day
	# month
	# year
	def __init__(self, _var1=None, _var2=None, _var3=None):
		if _var1!=None and _var2!=None and _var3==None:
			#Init with dayID and year
			self.year=_var2
			self.dayID=_var1
			self.timeStamp=self.dayID+self.yearToDays2000(self.year)
			self.day=self.dayLoader(self.dayID, self.year)[1]
			self.month=self.dayLoader(self.dayID, self.year)[2]
		elif _var1!=None and _var2==None and _var3==None:
			#Init with timeStamp
			self.timeStamp=_var1
			self.year=self.findYear(self.timeStamp)
			self.dayID=self.timeStamp-self.yearToDays2000(self.year)
			self.day=self.dayLoader(self.dayID, self.year)[1]
			self.month=self.dayLoader(self.dayID, self.year)[2]
		elif _var1!=None and _var2!=None and _var3!=None:
			#Init with day month and year
			self.day=_var1
			self.month=_var2
			self.year=_var3
			self.dayID=self.dayFinder(self.day, self.month, self.year)
			self.timeStamp=self.dayID+self.yearToDays2000(self.year)
		else:
			return 1
			#error
		days=["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
		self.dayName=days[self.dayLoader(self.dayID, self.year)[0]]
		months=["Janvier","Février","Mars","Avril","Mai","Juin","Juillet","Aout","Septembre","Octobre","Novembre","Décembre"]
		self.monthName=months[self.dayLoader(self.dayID, self.year)[2]-1]

	def isALeapYear(self, _year):
		if (_year-2000)%4==0:
			_leapYear=True
		else:
			_leapYear=False
		return _leapYear

	def yearToDays2000(self, year):
		year=year-2000
		c=0
		d=0
		while (c<year):
			if self.isALeapYear(2000+c):
				d+=366
			else:
				d+=365
			c+=1
		return d

	#first day calculator
	#(1/8/15/...-2/9/...-3/...-4/...-5/...-6/...-7/... = Monday-Tuesday-Wednesday-Tuesday-[...])
	def firstDayCalc(self, _year):
		if self.isALeapYear( _year)==True:
 			_rawFirstDay=((_year-2000)//4)*5+6
		else:
			_rawFirstDay=((_year-2000)//4)*5+7+((_year-2000)%4)

		stopLoop=False
		_firstDay=0
 		while stopLoop!=True:
 			if _rawFirstDay-7>0:
				_rawFirstDay=_rawFirstDay-7
			elif _rawFirstDay-1>0:
				_rawFirstDay=_rawFirstDay-1
				_firstDay+=1
			else:
				stopLoop=True
		return _firstDay

	#Day information loader
	#Day ID (0-364/5)
	def dayLoader(self, _dayID, _year):
		#If leapYear, 29 day in February, else 28
		if self.isALeapYear(_year):
			months=[["Janvier","Février","Mars","Avril","Mai","Juin","Juillet","Aout","Septembre","Octobre","Novembre","Décembre"],[31,29,31,30,31,30,31,31,30,31,30,31]]
		else:
			months=[["Janvier","Février","Mars","Avril","Mai","Juin","Juillet","Aout","Septembre","Octobre","Novembre","Décembre"],[31,28,31,30,31,30,31,31,30,31,30,31]]

		#Month finder
		stopLoop=False
		counter1=0
		counter2=0
		counter3=0
		while stopLoop!=True:
			while counter2<=counter1:
				counter3+=months[1][counter2]
				counter2+=1
			counter2=0
			if counter3>=_dayID+1:
				month=counter1
				stopLoop=True
			else:
				counter1+=1
			counter3=0
		counter1=0

		#Day-in-month no finder
		counter1=0
		counter2=0
		while counter1<month:
			counter2+=months[1][counter1]
			counter1+=1
		day=_dayID-counter2+1

		#day name finder
		rawDayName=self.firstDayCalc(_year)+_dayID
		while rawDayName-7>=0:
			rawDayName-=7
		dayName=rawDayName
		_date=[dayName,day,(month+1),_year]
		return _date

	def dayFinder(self, _day, _month, _year):
		#If leapYear, 29 day in February, else 28
		if self.isALeapYear(_year):
			months=[["Janvier","Février","Mars","Avril","Mai","Juin","Juillet","Aout","Septembre","Octobre","Novembre","Décembre"],[31,29,31,30,31,30,31,31,30,31,30,31]]
		else:
			months=[["Janvier","Février","Mars","Avril","Mai","Juin","Juillet","Aout","Septembre","Octobre","Novembre","Décembre"],[31,28,31,30,31,30,31,31,30,31,30,31]]

		counter1=0
		counter2=0
		while counter1<_month-1:
			counter2+=months[1][counter1]
			counter1+=1
 		counter2+=_day-1
		return(counter2)

	#Year finder from timestamp
	#timestamp (0-infinite)
	def findYear(self, _timestamp):# A verifier
		year=int(float(_timestamp)/365.25)+2000
		return year

	def findNextDay(self, dayNameFr):
		timeStamp=self.dayID
		rawSelectedDay=self.dayLoader(timeStamp, self.year)[0] # Craint pour le changement d'année
		days=["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
		selectedDay=days[rawSelectedDay]
		if dayNameFr==selectedDay:
			timeStamp+=7
		while dayNameFr!=selectedDay:
			timeStamp+=1
			rawSelectedDay=self.dayLoader(timeStamp, self.year)[0]
			selectedDay=days[rawSelectedDay]
		selectedDayInfos=self.dayLoader(timeStamp, self.year)
		return Date(selectedDayInfos[1], selectedDayInfos[2], selectedDayInfos[3])


#TimeSituation definition
class TimeSituation(object):
	# link is a string ('before' or 'after')
	# referential is a string (event name)
	def __init__(self, _link, _referential):
		self.link=_link
		self.referential=_referential
		if type(_referential)==type('eventID'):
			self.type=0
		elif type(_referential)==type(Time()):
			self.type=1

#Reccurence definition
class Recurrence(object):
	#Type 1 = every (x) days/weeks/months/years --> arg1(<int>), arg2(<str> | 'd', 'w', 'm', 'y'), arg3(<boolean> | None/False)
	#Type 2 = every (x)th (day) of the month/year --> arg1(<int>), arg2(<str> | 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'), arg3(<str> | 'm', 'y')
	#Type 3 = every (x)th day OF the month/year --> arg1(<int>), arg2(<str> | 'm', 'y'), arg3(<boolean> | True)
	def __init__(self, arg1=None, arg2=None, arg3=None):
		if arg1==None or type(arg1)!=type(1):
			self.type=0
			pass
		elif type(arg2)==type('str'):
			if type(arg3)==type(True):
				if arg3==True:
					#Type 3
					self.type=3
					self.nb=arg1
					self.recur=arg2
				else:
					#Type 1
					self.type=1
					self.nb=arg1
					self.recur=arg2
			elif type(arg3)==type('str'):
				#Type 2
				self.type=2
				self.nb=arg1
				self.day=arg2
				self.recur=arg3
			elif arg3==None:
				#Type 1
				self.type=1
				self.nb=arg1
				self.recur=arg2

#############################################################################################
#DayPlanning class definition


#DayPlanning definition
class DayPlanning(object):
	def __init__(self, date): # Comporte la date du jour chargé et une liste de type [[evnt1, event2], [(startTime1, endTime1), (startTime2, endTime2)]]
		self.date=date
		self.eventsList=[[],[]]
	def add(self, nEvent, startTime, endTime): # Ajoute un event à la liste en triant par ordre croissant d'heure de départ. Nécessite l'heure de départ et l'heure de fin.
		c=0
		while c<len(self.eventsList[1]):
			time.sleep(1)
			if startTime<self.eventsList[1][c][0]:
				c+=1
				time.sleep(1)
			else:
				self.eventsList[0].insert(c, nEvent)
				self.eventsList[1].insert(c, (startTime, endTime))
				break
		else:
			self.eventsList[0].append(nEvent)
			self.eventsList[1].append((startTime, endTime))
	def remove(self, _varID): # Retire un event de la liste par son ID
		blackList=[]
		for (i, obj) in enumerate(self.eventsList[0]):
			if str(obj[0])==str(_varID):
				blackList.append(i)
		n=1
		while n<=len(blackList):
			del self.eventsList[0][blackList[-n]]
			del self.eventsList[1][blackList[-n]]
			n+=1
		return 0


#############################################################################################
#Events classes definitions

#EventObject definition
class EventObject(object):
	def __init__(self):
		self.type=None
		timestamp=time.localtime().tm_hour*60*60+time.localtime().tm_min*60+time.localtime().tm_sec
		datestamp=time.localtime().tm_year*10000+time.localtime().tm_mon*100+time.localtime().tm_mday
		self.ID="{}_{}".format(datestamp,timestamp)

#Event definition
class Event(EventObject):
	# name is a string
	# time is a Time instance
	# duration is a Time instance
	# date is a Date instance
	# recurrence is a Reccurence instance
	def __init__(self, name, time, duration, date, recurrence=None): #name, time, duration, date, optionnal recurrence
		EventObject.__init__(self)
		self.type='Event'
		self.name=name
		self.time=time
		self.duration=duration
		self.date=date
		if recurrence!=None:
			self.recurrence=recurrence
			self.reccurent=True
		else:
			self.recurrence=None
			self.reccurent=False

#Task definition
class Task(EventObject):
	# name is a string
	# timeSituation is a TimeSituation instance
	# duration is a Time instance
	# date is a Date instance
	# recurrence is a Recurrence instance
	def __init__(self, name, timeSituation, duration, date, recurrence=None):
		EventObject.__init__(self)
		self.type='Task'
		self.name=name
		self.timeSituation=timeSituation
		self.duration=duration
		self.date=date
		if recurrence!=None:
			self.recurrence=recurrence
			self.reccurent=True
		else:
			self.recurrence=None
			self.reccurent=False

#Reminder definition
class Reminder(EventObject):
	# name is a string
	# time is a Time instance
	# date is a Date instance
	# recurrence is a Recurrence instance
	# status is a boolean instance
	def __init__(self, name, time, date, recurrence=None):
		EventObject.__init__(self)
		self.type='Reminder'
		self.name=name
		self.time=time
		self.status=False
		self.date=date
		if recurrence!=None:
			self.recurrence=recurrence
			self.reccurent=True
		else:
			self.recurrence=None
			self.recurrent=False

#ToDoThing definition
class ToDoThing(EventObject):
	# name is a string
	# timeSituation is a TimeSituation instance
	# date is a Date instance
	# recurrence is a Recurrence instance
	# status is a boolean instance
	def __init__(self, name, timeSituation, date, recurrence=None):
		EventObject.__init__(self)
		self.type='ToDoThing'
		self.name=name
		self.timeSituation=timeSituation
		self.status=False
		self.date=date
		if recurrence!=None:
			self.recurrence=recurrence
			self.reccurent=True
		else:
			self.recurrence=None
			self.reccurent=False

#Alarm definition
class Alarm(EventObject):
	# name is a string
	# time is a Time instance
	# date is a Date instance
	# recurrence is a Recurrence instance
	# isOn is a boolean instance
	def __init__(self, name, time, date, recurrence=None):
		EventObject.__init__(self)
		self.type='Alarm'
		self.name=name
		self.time=time
		self.isOn=True
		self.date=date
		if recurrence!=None:
			self.recurrence=recurrence
			self.reccurent=True
		else:
			self.recurrence=None
			self.recurrent=False

	def turnOn(self):
		self.isOn=True

	def turnOff(self):
		self.isOn=False

#AlarmClock definition
class AlarmClock(EventObject):
	# name is a string
	# time is a Time instance
	# date is a Date instance
	# recurrence is a Recurrence instance
	# isOn is a boolean instance
	def __init__(self, name, time, date, recurrence=None):
		EventObject.__init__(self)
		self.type='[CLCK]'
		self.name=name
		self.time=time
		self.isOn=True
		self.date=date
		if recurrence!=None:
			self.recurrence=recurrence
			self.reccurent=True
		else:
			self.recurrence=None
			self.recurrent=False

	def turnOn(self):
		self.isOn=True

	def turnOff(self):
		self.isOn=False

#############################################################################################
#############################################################################################
#METHODS DEFINITIONS

existingDirLogs=[] #Liste les dir. existantes
newDirLogs=[] #Liste les nouvelles dir.

index=Index()

#Inits methods definitions

def init():
	global existingDirLogs
	global newDirLogs

	incident1=0
	incident2=0

	os.system("echo '\n' > abymeInitLogs.txt")
	os.system("echo '-----------------------------------------------------' > abymeInitLogs.txt")
	os.system("echo '(INIT)[STARTING] New launch, starting initialization.' > abymeInitLogs.txt")

	checkPrimaryDirectories()
	checkIndex()
	checkSecondaryDirectories()
	checkEvents()
	os.system("echo '(FINAL)[READY] ABYME has been initialized and is now ready.' > abymeInitLogs.txt")

def checkPrimaryDirectories():
	safeFolderCreate('data')
	safeFolderCreate('others')

	safeFolderCreate('data/index')
	safeFolderCreate('data/others')
	safeFolderCreate('data/events')
	safeFolderCreate('data/informations')

	safeFolderCreate('data/events/recurrents')
	safeFolderCreate('data/events/non_recurrents')

	safeFolderCreate('data/events/recurrents/type_1')
	safeFolderCreate('data/events/recurrents/type_2')
	safeFolderCreate('data/events/recurrents/type_3')

	safeFolderCreate('data/events/recurrents/type_1/d')
	safeFolderCreate('data/events/recurrents/type_1/w')
	safeFolderCreate('data/events/recurrents/type_1/m')
	safeFolderCreate('data/events/recurrents/type_1/y')

	safeFolderCreate('data/events/recurrents/type_2/m')
	safeFolderCreate('data/events/recurrents/type_2/y')

	safeFolderCreate('data/events/recurrents/type_2/m/mo')
	safeFolderCreate('data/events/recurrents/type_2/m/tu')
	safeFolderCreate('data/events/recurrents/type_2/m/we')
	safeFolderCreate('data/events/recurrents/type_2/m/th')
	safeFolderCreate('data/events/recurrents/type_2/m/fr')
	safeFolderCreate('data/events/recurrents/type_2/m/sa')
	safeFolderCreate('data/events/recurrents/type_2/m/su')

	safeFolderCreate('data/events/recurrents/type_2/y/mo')
	safeFolderCreate('data/events/recurrents/type_2/y/tu')
	safeFolderCreate('data/events/recurrents/type_2/y/we')
	safeFolderCreate('data/events/recurrents/type_2/y/th')
	safeFolderCreate('data/events/recurrents/type_2/y/fr')
	safeFolderCreate('data/events/recurrents/type_2/y/sa')
	safeFolderCreate('data/events/recurrents/type_2/y/su')

	safeFolderCreate('data/events/recurrents/type_3/m')
	safeFolderCreate('data/events/recurrents/type_3/y')

def checkIndex():
	global index
	if not os.path.exists('./data/index/index.pickle'):
		with open('index.pickle', 'wb') as file:
			my_pickler = pickle.Pickler(file)
			my_pickler.dump(index)
	else:
		with open('./data/index/index.pickle', 'rb') as file:
			my_depickler = pickle.Unpickler(file)
			index = my_depickler.load()

def checkSecondaryDirectories():
	for i in index.list:
		if os.path.exists(str(i[2])):
			pass
		else:
			index.remove(i[0])

def checkEvents():
	for i in index.list:
		if os.path.exists(str(i[2]+i[3])):
			pass
		else:
			index.remove(i[0])

#safeFolderCreate method definition
def safeFolderCreate(folderName):
	global existingDirLogs
	global newDirLogs
	if os.path.exists('./{}'.format(folderName)):
		existingDirLogs.append('./{}'.format(folderName))
	else:
		os.mkdir(folderName)
		newDirLogs.append('./{}'.format(folderName))

#index save method definition
def saveIndex():
	global index
	with open('./data/index/index.pickle', 'wb') as file:
		my_pickler = pickle.Pickler(file)
		my_pickler.dump(index)
		file.close()

#############################################################################################
#"Engines" methods definitions

#addEvent method definition
def addEvent(event):
	global index
	if event.recurrence==None:
		pathStart='./data/events/non_recurrents'
		pathEnd='/{}.pickle'.format(event.ID)
		with open(pathStart+pathEnd, 'wb') as file:
			my_pickler = pickle.Pickler(file)
			my_pickler.dump(event)
			file.close()
		index.list.append((event.ID, event.name, pathStart, pathEnd))
		saveIndex()
		return 0
	else:
		reccType=event.recurrence.type
		if reccType==1: # 'b_y'
			pathStart='./data/events/recurrents/type_1/{}/{}'.format(event.recurrence.recur, str(event.date.timeStamp)+'_'+str(event.recurrence.nb))
			pathEnd='/{}.pickle'.format(event.ID)
			if os.path.exists(pathStart):
				with open(pathStart+pathEnd, 'wb') as file:
					my_pickler = pickle.Pickler(file)
					my_pickler.dump(event)
					file.close()
				index.list.append((event.ID, event.name, pathStart, pathEnd))
				saveIndex()
				return 0
			else:
				os.mkdir(pathStart)
				with open(pathStart+pathEnd, 'wb') as file:
					my_pickler = pickle.Pickler(file)
					my_pickler.dump(event)
					file.close()
				index.activeAttributs[1][event.recurrence.recur].append(str(event.date.timeStamp)+'_'+str(event.recurrence.nb))
				index.list.append((event.ID, event.name, pathStart, pathEnd))
				saveIndex()
				return 0
		elif reccType==2:
			pathStart='./data/events/recurrents/type_2/{}/{}'.format(str(event.recurrence.recur), str(event.recurrence.nb)+'_'+str(event.recurrence.day))
			pathEnd='/{}.pickle'.format(str(event.date.timeStamp)+'-'+event.ID)
			if os.path.exists(pathStart):
				with open(pathStart+pathEnd, 'wb') as file:
					my_pickler = pickle.Pickler(file)
					my_pickler.dump(event)
					file.close()
				index.list.append((event.ID, event.name, pathStart, pathEnd))
				saveIndex()
				return 0
			else:
				os.mkdir(pathStart)
				with open(pathStart+pathEnd, 'wb') as file:
					my_pickler = pickle.Pickler(file)
					my_pickler.dump(event)
					file.close()
				index.activeAttributs[2][event.recurrence.recur].append(str(event.recurrence.nb)+'_'+str(event.recurrence.day))
				index.list.append((event.ID, event.name, pathStart, pathEnd))
				saveIndex()
				return 0
		elif reccType==3:
			pathStart='./data/events/recurrents/type_3/{}/{}'.format(str(event.recurrence.recur), str(event.recurrence.nb))
			pathEnd='/{}.pickle'.format(str(event.date.timeStamp)+'-'+event.ID)
			if os.path.exists(pathStart):
				with open(pathStart+pathEnd, 'wb') as file:
					my_pickler = pickle.Pickler(file)
					my_pickler.dump(event)
					file.close()
				index.list.append((event.ID, event.name, pathStart, pathEnd))
				saveIndex()
				return 0
			else:
				os.mkdir(pathStart)
				with open(pathStart+pathEnd, 'wb') as file:
					my_pickler = pickle.Pickler(file)
					my_pickler.dump(event)
					file.close()
				index.activeAttributs[3][event.recurrence.recur].append(str(event.recurrence.nb))
				index.list.append((event.ID, event.name, pathStart, pathEnd))
				saveIndex()
				return 0
		else:
			return 1 #Error

#removeEvent method definition
def removeEvent(eventID):
	for (i, obj) in enumerate(index.list):
		if str(obj[0])==str(eventID):
			os.remove(obj[2]+obj[3]) # Suppression  du fichier event
			if obj[2].split('/')[3]=='recurrents': # Nettoyage du dossier et des récurrences
				if len(glob.glob('./data/events/recurrents/{}/{}/{}/*.pickle'.format(obj[2].split('/')[4], obj[2].split('/')[5], obj[2].split('/')[6])))==0:
					# L'attribut n'est plus actif, il ne comporte plus d'events: on le désactive
					index.activeAttributs[int(obj[2].split('/')[4].split('_')[1])][obj[2].split('/')[5]].remove(obj[2].split('/')[6])
	index.remove(eventID) # Suppression  du l'indexation event

def eventIDExistIn(_refID, _dayPlanning):
	if type(_refID)==type(Time()):
		return True
	elif type(_refID)==type('eventID'):
		for event in _dayPlanning.eventsList[0]:
			if event.ID==_refID:
				return True
		else:
			return False

#loadDay method definition
def loadDay(date):
	#Charge les events valables en les cherchant parmi les attributs actifs
	eventsToLoad=[]

	for i in index.list: # Vérification des non-récurrents
		if i[2].split('/')[3]=='non_recurrents':
			with open(i[2]+i[3], 'rb') as file:
				my_depickler = pickle.Unpickler(file)
				checkedEvent=my_depickler.load()
				if checkedEvent.date.timeStamp==date.timeStamp:
					eventsToLoad.append(checkedEvent)

	for i in index.activeAttributs[1]: # Vérification des récurrences de type_1:
		for r in index.activeAttributs[1][i]:
			recurInfos=r.split('_') #recurInfos[0]--> b | recurInfos[1]--> y

			if i=='d': #Vérification des type_1/d:
				if (date.timeStamp-int(recurInfos[0]))%(int(recurInfos[1])*1)==0:
					#La récurrence s'applique
					for e in glob.glob('./data/events/recurrents/type_1/{}/{}/*.pickle'.format(i, r)): #Charge les events
						with open(e, 'rb') as file:
							my_depickler = pickle.Unpickler(file)
							eventsToLoad.append(my_depickler.load())

			elif i=='w': #Vérification des type_1/w:
				if (date.timeStamp-int(recurInfos[0]))%(int(recurInfos[1])*7)==0:
					#La récurrence s'applique
					for e in glob.glob('./data/events/recurrents/type_1/{}/{}/*.pickle'.format(i, r)): #Charge les events
						with open(e, 'rb') as file:
							my_depickler = pickle.Unpickler(file)
							eventsToLoad.append(my_depickler.load())

			elif i=='m': #Vérification des type_1/m:
				baseDay=Date(int(recurInfos[0])).day
				baseMonth=Date(int(recurInfos[0])).month
				baseYear=Date(int(recurInfos[0])).year
				currentDay=date.day
				currentMonth=date.month
				currentYear=date.year
				recNb=int(recurInfos[1])
				if (((currentYear-1)*12+currentMonth)-((baseYear-1)*12+baseMonth))%recNb==0: # Si le mois actuel est valable
				# On vérifie si le jour est le bon (en prenant en compte les irrégularités)
					if baseMonth==2:
						if baseDay>28:
							if baseDay==29:
								if date.isALeapYear(currentYear):
									#jourIndiqué
									if currentDay==baseDay:
										for e in glob.glob('./data/events/recurrents/type_1/{}/{}/*.pickle'.format(i, r)): #Charge les events
											with open(e, 'rb') as file:
												my_depickler = pickle.Unpickler(file)
												eventsToLoad.append(my_depickler.load())
								else:
									if currentDay==28:
										for e in glob.glob('./data/events/recurrents/type_1/{}/{}/*.pickle'.format(i, r)): #Charge les events
											with open(e, 'rb') as file:
												my_depickler = pickle.Unpickler(file)
												eventsToLoad.append(my_depickler.load())
							else:
								if date.isALeapYear(date.year):
									if currentDay==29:
										for e in glob.glob('./data/events/recurrents/type_1/{}/{}/*.pickle'.format(i, r)): #Charge les events
											with open(e, 'rb') as file:
												my_depickler = pickle.Unpickler(file)
												eventsToLoad.append(my_depickler.load())
								else:
									if currentDay==28:
										for e in glob.glob('./data/events/recurrents/type_1/{}/{}/*.pickle'.format(i, r)): #Charge les events
											with open(e, 'rb') as file:
												my_depickler = pickle.Unpickler(file)
												eventsToLoad.append(my_depickler.load())
						else:
							if currentDay==baseDay:
								for e in glob.glob('./data/events/recurrents/type_1/{}/{}/*.pickle'.format(i, r)): #Charge les events
									with open(e, 'rb') as file:
										my_depickler = pickle.Unpickler(file)
										eventsToLoad.append(my_depickler.load())
					else:
						if baseDay==31:
							monthsDays=[31,0,31,0,31,0,31,31,0,31,0,31]
							if monthsDays[date.month-1]==31:
								if currentDay==baseDay:
									for e in glob.glob('./data/events/recurrents/type_1/{}/{}/*.pickle'.format(i, r)): #Charge les events
										with open(e, 'rb') as file:
											my_depickler = pickle.Unpickler(file)
											eventsToLoad.append(my_depickler.load())
							else:
								if currentDay==30:
									for e in glob.glob('./data/events/recurrents/type_1/{}/{}/*.pickle'.format(i, r)): #Charge les events
										with open(e, 'rb') as file:
											my_depickler = pickle.Unpickler(file)
											eventsToLoad.append(my_depickler.load())
						else:
							if currentDay==baseDay:
								for e in glob.glob('./data/events/recurrents/type_1/{}/{}/*.pickle'.format(i, r)): #Charge les events
									with open(e, 'rb') as file:
										my_depickler = pickle.Unpickler(file)
										eventsToLoad.append(my_depickler.load())

			elif i=='y': #Vérification des type_1/y:
				baseDay=Date(int(recurInfos[0])).day
				baseMonth=Date(int(recurInfos[0])).month
				baseYear=Date(int(recurInfos[0])).year
				currentDay=date.day
				currentMonth=date.month
				currentYear=date.year
				recNb=int(recurInfos[1])
				if (currentYear-baseYear)%recNb==0: # Si l'année actuelle est valable
					if baseMonth==2 and baseDay==29:
						if date.isALeapYear(currentYear):
							# Jour indiqué
							if currentDay==baseDay and baseMonth==currentMonth:
								for e in glob.glob('./data/events/recurrents/type_1/{}/{}/*.pickle'.format(i, r)): #Charge les events
									with open(e, 'rb') as file:
										my_depickler = pickle.Unpickler(file)
										eventsToLoad.append(my_depickler.load())
						else:
							# Jour 28
							if currentDay==28 and baseMonth==currentMonth:
								for e in glob.glob('./data/events/recurrents/type_1/{}/{}/*.pickle'.format(i, r)): #Charge les events
									with open(e, 'rb') as file:
										my_depickler = pickle.Unpickler(file)
										eventsToLoad.append(my_depickler.load())
					else:
						# Jour indiqué
						if currentDay==baseDay and baseMonth==currentMonth:
							for e in glob.glob('./data/events/recurrents/type_1/{}/{}/*.pickle'.format(i, r)): #Charge les events
								with open(e, 'rb') as file:
									my_depickler = pickle.Unpickler(file)
									eventsToLoad.append(my_depickler.load())

			else:
				return 1 # Error

	# Type 2			 [!!!]   A FINIR   [!!!]
	# (!) ATTENTION - La date d'un event type 2 n'est pas prise en compte, on vérifie seulement sa récurrence
	for i in index.activeAttributs[2]: # Vérification des récurrences de type_2:
		for r in index.activeAttributs[2][i]:
			recurInfos=r.split('_') #recurInfos[0]--> bX | recurInfos[1]--> dayName

			baseDay=Date(int(recurInfos[0])).day
			baseMonth=Date(int(recurInfos[0])).month
			baseYear=Date(int(recurInfos[0])).year
			currentDay=date.day
			currentMonth=date.month
			currentYear=date.year
			recNb=int(recurInfos[1])


	# Type 3
	# (!) ATTENTION - La date d'un event type 3 n'est pas prise en compte, on vérifie seulement sa récurrence
	for i in index.activeAttributs[3]: # Vérification des récurrences de type_3:
		for r in index.activeAttributs[3][i]:
				if i=='m':
					baseDay=r #recurInfos --> bDayId
					currentDay=date.day
					currentMonth=date.month
					currentYear=date.year
					monthsDays=[31,0,31,0,31,0,31,31,0,31,0,31]
					if baseDay>28 and currentMonth==2: # Si on est en février et que le jour cible est 29 30 ou 31
						if date.isALeapYear(currentYear):
							# Jour 29
							if currentDay==29:
								for e in glob.glob('./data/events/recurrents/type_2/{}/{}/*.pickle'.format(i, r)): #Charge les events
									with open(e, 'rb') as file:
										my_depickler = pickle.Unpickler(file)
										eventsToLoad.append(my_depickler.load())
						else:
							# Jour indiqué
							if currentDay==baseDay:
								for e in glob.glob('./data/events/recurrents/type_2/{}/{}/*.pickle'.format(i, r)): #Charge les events
									with open(e, 'rb') as file:
										my_depickler = pickle.Unpickler(file)
										eventsToLoad.append(my_depickler.load())

					elif baseDay>30 and monthsDays[currentMonth-1]!=31: # Si on est en mois de 30 jours et que le jour cible est 31
						# Jour 30
						if currentDay==30:
							for e in glob.glob('./data/events/recurrents/type_2/{}/{}/*.pickle'.format(i, r)): #Charge les events
								with open(e, 'rb') as file:
									my_depickler = pickle.Unpickler(file)
									eventsToLoad.append(my_depickler.load())
					else:
						# Jour indiqué
						if currentDay==baseDay:
							for e in glob.glob('./data/events/recurrents/type_2/{}/{}/*.pickle'.format(i, r)): #Charge les events
								with open(e, 'rb') as file:
									my_depickler = pickle.Unpickler(file)
									eventsToLoad.append(my_depickler.load())
				if i=='y':
					baseDayID=r #recurInfos --> bDayId
					currentDayID=date.dayID
					currentYear=date.year
					if baseDayID==365: #Dernier jour de l'année
						if date.isALeapYear(currentYear):
							# Jour indiqué (365)
							if currentDayID==baseDayID:
								for e in glob.glob('./data/events/recurrents/type_2/{}/{}/*.pickle'.format(i, r)): #Charge les events
									with open(e, 'rb') as file:
										my_depickler = pickle.Unpickler(file)
										eventsToLoad.append(my_depickler.load())
						else:
							# Jour 364 (dernier jour de l'année)
							if currentDayID==364:
								for e in glob.glob('./data/events/recurrents/type_2/{}/{}/*.pickle'.format(i, r)): #Charge les events
									with open(e, 'rb') as file:
										my_depickler = pickle.Unpickler(file)
										eventsToLoad.append(my_depickler.load())
					else:
						# Jour indiqué
						if currentDayID==baseDayID:
							for e in glob.glob('./data/events/recurrents/type_2/{}/{}/*.pickle'.format(i, r)): #Charge les events
								with open(e, 'rb') as file:
									my_depickler = pickle.Unpickler(file)
									eventsToLoad.append(my_depickler.load())

	#Crée le dayPlanning à remplir et renvoyer
	dayPlanning=DayPlanning(date)

	#Insère les events absolus
	relatifs=[]
	for event in eventsToLoad:
		if event.type=='Event' or  event.type=='Reminder' or event.type=='Alarm' or event.type=='[CLCK]':
			if event.type=='Event':
				dayPlanning.add(event, event.time, event.time.timeOperation('+', event.duration))
			if event.type=='Reminder' or event.type=='Alarm' or event.type=='[CLCK]':
				dayPlanning.add(event, event.time, None)
		elif event.type=='Task' or  event.type=='ToDoThing':
			relatifs.append(event)
		else:
			return 404

	#Insère les events relatifs
	relatifsStop=False
	while not relatifsStop:
		for (i, event) in enumerate(relatifs):
			if event.timeSituation.type==1 or eventIDExistIn(event.timeSituation.referential, dayPlanning): # Si on peut placer l'event
				#On place l'event
				if event.type=='ToDoThing':
					if event.timeSituation.type==0:
						for (c, registeredEvent) in enumerate(dayPlanning.eventsList[0]):
							if registeredEvent[0]==event.timeSituation.referential:
								if event.timeSituation.link=='before':
									thisEventTime=dayPlanning.eventsList[1][c][0]
								elif event.timeSituation.link=='after':
									thisEventTime=dayPlanning.eventsList[1][c][1]
						dayPlanning.add(event, thisEventTime, None)
					else:
						dayPlanning.add(event, timeSituation.referential, None)
				elif event.type=='Task':
					if event.timeSituation.type==0:
						placed=False
						while not placed:
							n=findEventIndexInDayPlanning(event.timeSituation.referential, dayPlanning)
							if event.timeSituation.link=='after':
								for (i, obj) in enumerate(dayPlanning.eventsList[1]):
									if i<=n:
										continue
									else:
										if dayPlanning.eventsList[1][i][0].timeOperation('-', dayPlanning.eventsList[1][i-1][1]).time>=event.duration.time: # Event suivant réference (heure de début) - Event réference (heure de fin) >= durée de l'event à placer
											# On place
											dayPlanning.add(event, dayPlanning.eventsList[1][i-1][1].time, dayPlanning.eventsList[1][i-1][1].time.timeOperation('+', event.duration))
											placed=True
								else: # Il n'y a plus d'events suivants
									dayPlanning.add(event, dayPlanning.eventsList[1][-1][1].time, dayPlanning.eventsList[1][-1][1].time.timeOperation('+', event.duration))
									placed=True
							elif event.timeSituation.link=='before':
								for (i, obj) in enumerate(dayPlanning.eventsList[1]):
									if len(dayPlanning.eventsList[1])-1-i>=n:
										continue
									else:
										if dayPlanning.eventsList[1][len(dayPlanning.eventsList[1])-1-(i-1)][0].timeOperation('-', dayPlanning.eventsList[1][len(dayPlanning.eventsList[1])-1-i][1]).time>=event.duration.time: # Event suivant réference (heure de début) - Event réference (heure de fin) >= durée de l'event à placer
											# On place
											dayPlanning.add(event, dayPlanning.eventsList[1][len(dayPlanning.eventsList[1])-1-(i-1)][0].timeOperation('-', event.duration), dayPlanning.eventsList[1][len(dayPlanning.eventsList[1])-1-(i-1)][0])
											placed=True
								else: # Il n'y a plus d'events précédents
									# On place avant le premier event
									dayPlanning.add(event, dayPlanning.eventsList[1][0][0].timeOperation('-', event.duration), dayPlanning.eventsList[1][0][0])
									placed=True
					else:
						pass
						# A COMPLETER

				del relatifs[i] # On le supprime de la liste des events à placer
				break # On indique qu'on a placé un event
		else : # Si on ne peut plus placer d'event
			relatifsStop=True # On arrête la boucle


	#Retourne le dayPlanning
	return dayPlanning



def findEventIndexInDayPlanning(eventID, _dayPlanning):
	for (i, eventItem) in enumerate(_dayPlanning.eventsList[0]):
                        if str(eventItem.ID)==str(eventID):
				return i

#############################################################################################

#Ohers methods definitions

def display(message):
	print(message)

def weather():
        os.system('weather -q lfml > weather.txt')
        with open('./weather.txt', 'rb') as file:
                x=file.read()
                file.close()
        y=x.split('\n')

        z=y[0].split('(')
        temperature=z[1].split(' ')[0] # °C

        z=y[1].split(' ')
        humidity=z[2].split('%')[0] # %

        z=y[2].split(' ')
        wind=int(int(z[7])*1.609344) # km/h

        sky='work-in-progress'

        return (temperature, humidity, wind, sky)

numbers=['zero', 'un', 'deux', 'trois', 'quatre', 'cinq', 'six', 'sept', 'huit', 'neuf', 'dix', 'onze', 'douze', 'treize', 'quatorze', 'quinze', 'seize', 'dix sept', 'dix huit', 'dix neuf', 'vingt', 'vingt et un', 'vingt deux', 'vingt trois', 'vingt quatre', 'vingt cinq', 'vingt six', 'vingt sept', 'vingt huit', 'vingt neuf', 'trente', 'trente et un', 'trente deux', 'trente trois', 'trente quatre', 'trente cinq', 'trente six', 'trente sept', 'trente huit', 'trente neuf', 'quarante', 'quarante et un', 'quarante deux', 'quarante trois', 'quarante quatre', 'quarante cinq', 'quarante six', 'quarante sept', 'quarante huit', 'quarante neuf', 'cinquante', 'cinquante et un', 'cinquante deux', 'cinquante trois', 'cinquante quatre', 'cinquante cinq', 'cinquante six', 'cinquante sept', 'cinquante huit', 'cinquante neuf', 'soixante', 'soixante et un', 'soixante deux', 'soixante trois', 'soixante quatre', 'soixante cinq', 'soixante six', 'soixante sept', 'soixante huit', 'soixante neuf', 'soixante dix', 'soixante et onze', 'soixante douze', 'soixante treize', 'soixante quatorze', 'soixante quinze', 'soixante seize', 'soixante dix sept', 'soixante dix huit', 'soixante dix neuf', 'quatre vingts', 'quatre vingt un', 'quatre vingt deux', 'quatre vingt trois', 'quatre vingt quatre', 'quatre vingt cinq', 'quatre vingt six', 'quatre vingt sept', 'quatre vingt huit', 'quatre vingt neuf', 'quatre vingt dix', 'quatre vingt onze', 'quatre vingt douze', 'quatre vingt treize', 'quatre vingt quatorze', 'quatre vingt quinze', 'quatre vingt seize', 'quatre vingt dix sept', 'quatre vingt dix huit', 'quatre vingt dix neuf', 'cent', 'cent un', 'cent deux', 'cent trois', 'cent quatre', 'cent cinq', 'cent six', 'cent sept', 'cent huit', 'cent neuf', 'cent dix', 'cent onze', 'cent douze', 'cent treize', 'cent quatorze', 'cent quinze', 'cent seize', 'cent dix sept', 'cent dix huit', 'cent dix neuf', 'cent vingt', 'cent vingt et un', 'cent vingt deux', 'cent vingt trois', 'cent vingt quatre', 'cent vingt cinq', 'cent vingt six', 'cent vingt sept', 'cent vingt huit', 'cent vingt neuf', 'cent trente', 'cent trente et un', 'cent trente deux', 'cent trente trois', 'cent trente quatre', 'cent trente cinq', 'cent trente six', 'cent trente sept', 'cent trente huit', 'cent trente neuf', 'cent quarante', 'cent quarante et un', 'cent quarante deux', 'cent quarante trois', 'cent quarante quatre', 'cent quarante cinq', 'cent quarante six', 'cent quarante sept', 'cent quarante huit', 'cent quarante neuf', 'cent cinquante', 'cent cinquante et un', 'cent cinquante deux', 'cent cinquante trois', 'cent cinquante quatre', 'cent cinquante cinq', 'cent cinquante six', 'cent cinquante sept', 'cent cinquante huit', 'cent cinquante neuf', 'cent soixante', 'cent soixante et un', 'cent soixante deux', 'cent soixante trois', 'cent soixante quatre', 'cent soixante cinq', 'cent soixante six', 'cent soixante sept', 'cent soixante huit', 'cent soixante neuf', 'cent soixante dix', 'cent soixante et onze', 'cent soixante douze', 'cent soixante treize', 'cent soixante quatorze', 'cent soixante quinze', 'cent soixante seize', 'cent soixante dix sept', 'cent soixante dix huit', 'cent soixante dix neuf', 'cent quatre vingts', 'cent quatre vingt un', 'cent quatre vingt deux', 'cent quatre vingt trois', 'cent quatre vingt quatre', 'cent quatre vingt cinq', 'cent quatre vingt six', 'cent quatre vingt sept', 'cent quatre vingt huit', 'cent quatre vingt neuf', 'cent quatre vingt dix', 'cent quatre vingt onze', 'cent quatre vingt douze', 'cent quatre vingt treize', 'cent quatre vingt quatorze', 'cent quatre vingt quinze', 'cent quatre vingt seize', 'cent quatre vingt dix sept', 'cent quatre vingt dix huit', 'cent quatre vingt dix neuf', 'deux cents', 'deux cent un', 'deux cent deux', 'deux cent trois', 'deux cent quatre', 'deux cent cinq', 'deux cent six', 'deux cent sept', 'deux cent huit', 'deux cent neuf', 'deux cent dix', 'deux cent onze', 'deux cent douze', 'deux cent treize', 'deux cent quatorze', 'deux cent quinze', 'deux cent seize', 'deux cent dix sept', 'deux cent dix huit', 'deux cent dix neuf', 'deux cent vingt', 'deux cent vingt et un', 'deux cent vingt deux', 'deux cent vingt trois', 'deux cent vingt quatre', 'deux cent vingt cinq', 'deux cent vingt six', 'deux cent vingt sept', 'deux cent vingt huit', 'deux cent vingt neuf', 'deux cent trente', 'deux cent trente et un', 'deux cent trente deux', 'deux cent trente trois', 'deux cent trente quatre', 'deux cent trente cinq', 'deux cent trente six', 'deux cent trente sept', 'deux cent trente huit', 'deux cent trente neuf', 'deux cent quarante', 'deux cent quarante et un', 'deux cent quarante deux', 'deux cent quarante trois', 'deux cent quarante quatre', 'deux cent quarante cinq', 'deux cent quarante six', 'deux cent quarante sept', 'deux cent quarante huit', 'deux cent quarante neuf', 'deux cent cinquante', 'deux cent cinquante et un', 'deux cent cinquante deux', 'deux cent cinquante trois', 'deux cent cinquante quatre', 'deux cent cinquante cinq', 'deux cent cinquante six', 'deux cent cinquante sept', 'deux cent cinquante huit', 'deux cent cinquante neuf', 'deux cent soixante', 'deux cent soixante et un', 'deux cent soixante deux', 'deux cent soixante trois', 'deux cent soixante quatre', 'deux cent soixante cinq', 'deux cent soixante six', 'deux cent soixante sept', 'deux cent soixante huit', 'deux cent soixante neuf', 'deux cent soixante dix', 'deux cent soixante et onze', 'deux cent soixante douze', 'deux cent soixante treize', 'deux cent soixante quatorze', 'deux cent soixante quinze', 'deux cent soixante seize', 'deux cent soixante dix sept', 'deux cent soixante dix huit', 'deux cent soixante dix neuf', 'deux cent quatre vingts', 'deux cent quatre vingt un', 'deux cent quatre vingt deux', 'deux cent quatre vingt trois', 'deux cent quatre vingt quatre', 'deux cent quatre vingt cinq', 'deux cent quatre vingt six', 'deux cent quatre vingt sept', 'deux cent quatre vingt huit', 'deux cent quatre vingt neuf', 'deux cent quatre vingt dix', 'deux cent quatre vingt onze', 'deux cent quatre vingt douze', 'deux cent quatre vingt treize', 'deux cent quatre vingt quatorze', 'deux cent quatre vingt quinze', 'deux cent quatre vingt seize', 'deux cent quatre vingt dix sept', 'deux cent quatre vingt dix huit', 'deux cent quatre vingt dix neuf', 'trois cents', 'trois cent un', 'trois cent deux', 'trois cent trois', 'trois cent quatre', 'trois cent cinq', 'trois cent six', 'trois cent sept', 'trois cent huit', 'trois cent neuf', 'trois cent dix', 'trois cent onze', 'trois cent douze', 'trois cent treize', 'trois cent quatorze', 'trois cent quinze', 'trois cent seize', 'trois cent dix sept', 'trois cent dix huit', 'trois cent dix neuf', 'trois cent vingt', 'trois cent vingt et un', 'trois cent vingt deux', 'trois cent vingt trois', 'trois cent vingt quatre', 'trois cent vingt cinq', 'trois cent vingt six', 'trois cent vingt sept', 'trois cent vingt huit', 'trois cent vingt neuf', 'trois cent trente', 'trois cent trente et un', 'trois cent trente deux', 'trois cent trente trois', 'trois cent trente quatre', 'trois cent trente cinq', 'trois cent trente six', 'trois cent trente sept', 'trois cent trente huit', 'trois cent trente neuf', 'trois cent quarante', 'trois cent quarante et un', 'trois cent quarante deux', 'trois cent quarante trois', 'trois cent quarante quatre', 'trois cent quarante cinq', 'trois cent quarante six', 'trois cent quarante sept', 'trois cent quarante huit', 'trois cent quarante neuf', 'trois cent cinquante', 'trois cent cinquante et un', 'trois cent cinquante deux', 'trois cent cinquante trois', 'trois cent cinquante quatre', 'trois cent cinquante cinq', 'trois cent cinquante six', 'trois cent cinquante sept', 'trois cent cinquante huit', 'trois cent cinquante neuf', 'trois cent soixante', 'trois cent soixante et un', 'trois cent soixante deux', 'trois cent soixante trois', 'trois cent soixante quatre', 'trois cent soixante cinq', 'trois cent soixante six', 'trois cent soixante sept', 'trois cent soixante huit', 'trois cent soixante neuf', 'trois cent soixante dix', 'trois cent soixante et onze', 'trois cent soixante douze', 'trois cent soixante treize', 'trois cent soixante quatorze', 'trois cent soixante quinze', 'trois cent soixante seize', 'trois cent soixante dix sept', 'trois cent soixante dix huit', 'trois cent soixante dix neuf', 'trois cent quatre vingts', 'trois cent quatre vingt un', 'trois cent quatre vingt deux', 'trois cent quatre vingt trois', 'trois cent quatre vingt quatre', 'trois cent quatre vingt cinq', 'trois cent quatre vingt six', 'trois cent quatre vingt sept', 'trois cent quatre vingt huit', 'trois cent quatre vingt neuf', 'trois cent quatre vingt dix', 'trois cent quatre vingt onze', 'trois cent quatre vingt douze', 'trois cent quatre vingt treize', 'trois cent quatre vingt quatorze', 'trois cent quatre vingt quinze', 'trois cent quatre vingt seize', 'trois cent quatre vingt dix sept', 'trois cent quatre vingt dix huit', 'trois cent quatre vingt dix neuf', 'quatre cents', 'quatre cent un', 'quatre cent deux', 'quatre cent trois', 'quatre cent quatre', 'quatre cent cinq', 'quatre cent six', 'quatre cent sept', 'quatre cent huit', 'quatre cent neuf', 'quatre cent dix', 'quatre cent onze', 'quatre cent douze', 'quatre cent treize', 'quatre cent quatorze', 'quatre cent quinze', 'quatre cent seize', 'quatre cent dix sept', 'quatre cent dix huit', 'quatre cent dix neuf', 'quatre cent vingt', 'quatre cent vingt et un', 'quatre cent vingt deux', 'quatre cent vingt trois', 'quatre cent vingt quatre', 'quatre cent vingt cinq', 'quatre cent vingt six', 'quatre cent vingt sept', 'quatre cent vingt huit', 'quatre cent vingt neuf', 'quatre cent trente', 'quatre cent trente et un', 'quatre cent trente deux', 'quatre cent trente trois', 'quatre cent trente quatre', 'quatre cent trente cinq', 'quatre cent trente six', 'quatre cent trente sept', 'quatre cent trente huit', 'quatre cent trente neuf', 'quatre cent quarante', 'quatre cent quarante et un', 'quatre cent quarante deux', 'quatre cent quarante trois', 'quatre cent quarante quatre', 'quatre cent quarante cinq', 'quatre cent quarante six', 'quatre cent quarante sept', 'quatre cent quarante huit', 'quatre cent quarante neuf', 'quatre cent cinquante', 'quatre cent cinquante et un', 'quatre cent cinquante deux', 'quatre cent cinquante trois', 'quatre cent cinquante quatre', 'quatre cent cinquante cinq', 'quatre cent cinquante six', 'quatre cent cinquante sept', 'quatre cent cinquante huit', 'quatre cent cinquante neuf', 'quatre cent soixante', 'quatre cent soixante et un', 'quatre cent soixante deux', 'quatre cent soixante trois', 'quatre cent soixante quatre', 'quatre cent soixante cinq', 'quatre cent soixante six', 'quatre cent soixante sept', 'quatre cent soixante huit', 'quatre cent soixante neuf', 'quatre cent soixante dix', 'quatre cent soixante et onze', 'quatre cent soixante douze', 'quatre cent soixante treize', 'quatre cent soixante quatorze', 'quatre cent soixante quinze', 'quatre cent soixante seize', 'quatre cent soixante dix sept', 'quatre cent soixante dix huit', 'quatre cent soixante dix neuf', 'quatre cent quatre vingts', 'quatre cent quatre vingt un', 'quatre cent quatre vingt deux', 'quatre cent quatre vingt trois', 'quatre cent quatre vingt quatre', 'quatre cent quatre vingt cinq', 'quatre cent quatre vingt six', 'quatre cent quatre vingt sept', 'quatre cent quatre vingt huit', 'quatre cent quatre vingt neuf', 'quatre cent quatre vingt dix', 'quatre cent quatre vingt onze', 'quatre cent quatre vingt douze', 'quatre cent quatre vingt treize', 'quatre cent quatre vingt quatorze', 'quatre cent quatre vingt quinze', 'quatre cent quatre vingt seize', 'quatre cent quatre vingt dix sept', 'quatre cent quatre vingt dix huit', 'quatre cent quatre vingt dix neuf', 'cinq cents']
ordinalNumbers=['', 'premier', 'deuxieme', 'troisieme', 'quatrieme', 'cinquieme', 'sixieme', 'septieme', 'huitieme', 'neuvieme', 'dixieme', 'onzieme', 'douzieme', 'treizieme', 'quatorzieme', 'quinzieme', 'seizieme', 'dix septieme', 'dix huitieme', 'dix neuvieme', 'vingtieme', 'et', 'vingt deuxieme', 'vingt troisieme', 'vingt quatrieme', 'vingt cinquieme', 'vingt sixieme', 'vingt septieme', 'vingt huitieme', 'vingt neuvieme', 'trentieme', 'et', 'trente deuxieme', 'trente troisieme', 'trente quatrieme', 'trente cinquieme', 'trente sixieme', 'trente septieme', 'trente huitieme', 'trente neuvieme', 'quarantieme', 'et', 'quarante deuxieme', 'quarante troisieme', 'quarante quatrieme', 'quarante cinquieme', 'quarante sixieme', 'quarante septieme', 'quarante huitieme', 'quarante neuvieme', 'cinquantieme', 'et', 'cinquante deuxieme', 'cinquante troisieme', 'cinquante quatrieme', 'cinquante cinquieme', 'cinquante sixieme', 'cinquante septieme', 'cinquante huitieme', 'cinquante neuvieme', 'soixantieme', 'et', 'soixante deuxieme', 'soixante troisieme', 'soixante quatrieme', 'soixante cinquieme', 'soixante sixieme', 'soixante septieme', 'soixante huitieme', 'soixante neuvieme', 'soixante dixieme', 'et', 'soixante douzieme', 'soixante treizieme', 'soixante quatorzieme', 'soixante quinzieme', 'soixante seizieme', 'soixante dix septieme', 'soixante dix huitieme', 'soixante dix neuvieme', 'quatre vingtieme', 'quatre vingt unieme', 'quatre vingt deuxieme', 'quatre vingt troisieme', 'quatre vingt quatrieme', 'quatre vingt cinquieme', 'quatre vingt sixieme', 'quatre vingt septieme', 'quatre vingt huitieme', 'quatre vingt neuvieme', 'quatre vingt dixieme', 'quatre vingt onzieme', 'quatre vingt douzieme', 'quatre vingt treizieme', 'quatre vingt quatorzieme', 'quatre vingt quinzieme', 'quatre vingt seizieme', 'quatre vingt dix septieme', 'quatre vingt dix huitieme', 'quatre vingt dix neuvieme', 'centieme', 'cent unieme', 'cent deuxieme', 'cent troisieme', 'cent quatrieme', 'cent cinquieme', 'cent sixieme', 'cent septieme', 'cent huitieme', 'cent neuvieme', 'cent dixieme', 'cent onzieme', 'cent douzieme', 'cent treizieme', 'cent quatorzieme', 'cent quinzieme', 'cent seizieme', 'cent dix septieme', 'cent dix huitieme', 'cent dix neuvieme', 'cent vingtieme', 'cent vingt et unieme', 'cent vingt deuxieme', 'cent vingt troisieme', 'cent vingt quatrieme', 'cent vingt cinquieme', 'cent vingt sixieme', 'cent vingt septieme', 'cent vingt huitieme', 'cent vingt neuvieme', 'cent trentieme', 'cent trente et unieme', 'cent trente deuxieme', 'cent trente troisieme', 'cent trente quatrieme', 'cent trente cinquieme', 'cent trente sixieme', 'cent trente septieme', 'cent trente huitieme', 'cent trente neuvieme', 'cent quarantieme', 'cent quarante et unieme', 'cent quarante deuxieme', 'cent quarante troisieme', 'cent quarante quatrieme', 'cent quarante cinquieme', 'cent quarante sixieme', 'cent quarante septieme', 'cent quarante huitieme', 'cent quarante neuvieme', 'cent cinquantieme', 'cent cinquante et unieme', 'cent cinquante deuxieme', 'cent cinquante troisieme', 'cent cinquante quatrieme', 'cent cinquante cinquieme', 'cent cinquante sixieme', 'cent cinquante septieme', 'cent cinquante huitieme', 'cent cinquante neuvieme', 'cent soixantieme', 'cent soixante et unieme', 'cent soixante deuxieme', 'cent soixante troisieme', 'cent soixante quatrieme', 'cent soixante cinquieme', 'cent soixante sixieme', 'cent soixante septieme', 'cent soixante huitieme', 'cent soixante neuvieme', 'cent soixante dixieme', 'cent soixante et onzieme', 'cent soixante douzieme', 'cent soixante treizieme', 'cent soixante quatorzieme', 'cent soixante quinzieme', 'cent soixante seizieme', 'cent soixante dix septieme', 'cent soixante dix huitieme', 'cent soixante dix neuvieme', 'cent quatre vingtieme', 'cent quatre vingt unieme', 'cent quatre vingt deuxieme', 'cent quatre vingt troisieme', 'cent quatre vingt quatrieme', 'cent quatre vingt cinquieme', 'cent quatre vingt sixieme', 'cent quatre vingt septieme', 'cent quatre vingt huitieme', 'cent quatre vingt neuvieme', 'cent quatre vingt dixieme', 'cent quatre vingt onzieme', 'cent quatre vingt douzieme', 'cent quatre vingt treizieme', 'cent quatre vingt quatorzieme', 'cent quatre vingt quinzieme', 'cent quatre vingt seizieme', 'cent quatre vingt dix septieme', 'cent quatre vingt dix huitieme', 'cent quatre vingt dix neuvieme', 'deux centieme', 'deux cent unieme', 'deux cent deuxieme', 'deux cent troisieme', 'deux cent quatrieme', 'deux cent cinquieme', 'deux cent sixieme', 'deux cent septieme', 'deux cent huitieme', 'deux cent neuvieme', 'deux cent dixieme', 'deux cent onzieme', 'deux cent douzieme', 'deux cent treizieme', 'deux cent quatorzieme', 'deux cent quinzieme', 'deux cent seizieme', 'deux cent dix septieme', 'deux cent dix huitieme', 'deux cent dix neuvieme', 'deux cent vingtieme', 'deux cent vingt et unieme', 'deux cent vingt deuxieme', 'deux cent vingt troisieme', 'deux cent vingt quatrieme', 'deux cent vingt cinquieme', 'deux cent vingt sixieme', 'deux cent vingt septieme', 'deux cent vingt huitieme', 'deux cent vingt neuvieme', 'deux cent trentieme', 'deux cent trente et unieme', 'deux cent trente deuxieme', 'deux cent trente troisieme', 'deux cent trente quatrieme', 'deux cent trente cinquieme', 'deux cent trente sixieme', 'deux cent trente septieme', 'deux cent trente huitieme', 'deux cent trente neuvieme', 'deux cent quarantieme', 'deux cent quarante et unieme', 'deux cent quarante deuxieme', 'deux cent quarante troisieme', 'deux cent quarante quatrieme', 'deux cent quarante cinquieme', 'deux cent quarante sixieme', 'deux cent quarante septieme', 'deux cent quarante huitieme', 'deux cent quarante neuvieme', 'deux cent cinquantieme', 'deux cent cinquante et unieme', 'deux cent cinquante deuxieme', 'deux cent cinquante troisieme', 'deux cent cinquante quatrieme', 'deux cent cinquante cinquieme', 'deux cent cinquante sixieme', 'deux cent cinquante septieme', 'deux cent cinquante huitieme', 'deux cent cinquante neuvieme', 'deux cent soixantieme', 'deux cent soixante et unieme', 'deux cent soixante deuxieme', 'deux cent soixante troisieme', 'deux cent soixante quatrieme', 'deux cent soixante cinquieme', 'deux cent soixante sixieme', 'deux cent soixante septieme', 'deux cent soixante huitieme', 'deux cent soixante neuvieme', 'deux cent soixante dixieme', 'deux cent soixante et onzieme', 'deux cent soixante douzieme', 'deux cent soixante treizieme', 'deux cent soixante quatorzieme', 'deux cent soixante quinzieme', 'deux cent soixante seizieme', 'deux cent soixante dix septieme', 'deux cent soixante dix huitieme', 'deux cent soixante dix neuvieme', 'deux cent quatre vingtieme', 'deux cent quatre vingt unieme', 'deux cent quatre vingt deuxieme', 'deux cent quatre vingt troisieme', 'deux cent quatre vingt quatrieme', 'deux cent quatre vingt cinquieme', 'deux cent quatre vingt sixieme', 'deux cent quatre vingt septieme', 'deux cent quatre vingt huitieme', 'deux cent quatre vingt neuvieme', 'deux cent quatre vingt dixieme', 'deux cent quatre vingt onzieme', 'deux cent quatre vingt douzieme', 'deux cent quatre vingt treizieme', 'deux cent quatre vingt quatorzieme', 'deux cent quatre vingt quinzieme', 'deux cent quatre vingt seizieme', 'deux cent quatre vingt dix septieme', 'deux cent quatre vingt dix huitieme', 'deux cent quatre vingt dix neuvieme', 'trois centieme', 'trois cent unieme', 'trois cent deuxieme', 'trois cent troisieme', 'trois cent quatrieme', 'trois cent cinquieme', 'trois cent sixieme', 'trois cent septieme', 'trois cent huitieme', 'trois cent neuvieme', 'trois cent dixieme', 'trois cent onzieme', 'trois cent douzieme', 'trois cent treizieme', 'trois cent quatorzieme', 'trois cent quinzieme', 'trois cent seizieme', 'trois cent dix septieme', 'trois cent dix huitieme', 'trois cent dix neuvieme', 'trois cent vingtieme', 'trois cent vingt et unieme', 'trois cent vingt deuxieme', 'trois cent vingt troisieme', 'trois cent vingt quatrieme', 'trois cent vingt cinquieme', 'trois cent vingt sixieme', 'trois cent vingt septieme', 'trois cent vingt huitieme', 'trois cent vingt neuvieme', 'trois cent trentieme', 'trois cent trente et unieme', 'trois cent trente deuxieme', 'trois cent trente troisieme', 'trois cent trente quatrieme', 'trois cent trente cinquieme', 'trois cent trente sixieme', 'trois cent trente septieme', 'trois cent trente huitieme', 'trois cent trente neuvieme', 'trois cent quarantieme', 'trois cent quarante et unieme', 'trois cent quarante deuxieme', 'trois cent quarante troisieme', 'trois cent quarante quatrieme', 'trois cent quarante cinquieme', 'trois cent quarante sixieme', 'trois cent quarante septieme', 'trois cent quarante huitieme', 'trois cent quarante neuvieme', 'trois cent cinquantieme', 'trois cent cinquante et unieme', 'trois cent cinquante deuxieme', 'trois cent cinquante troisieme', 'trois cent cinquante quatrieme', 'trois cent cinquante cinquieme', 'trois cent cinquante sixieme', 'trois cent cinquante septieme', 'trois cent cinquante huitieme', 'trois cent cinquante neuvieme', 'trois cent soixantieme', 'trois cent soixante et unieme', 'trois cent soixante deuxieme', 'trois cent soixante troisieme', 'trois cent soixante quatrieme', 'trois cent soixante cinquieme', 'trois cent soixante sixieme', 'trois cent soixante septieme', 'trois cent soixante huitieme', 'trois cent soixante neuvieme', 'trois cent soixante dixieme', 'trois cent soixante et onzieme', 'trois cent soixante douzieme', 'trois cent soixante treizieme', 'trois cent soixante quatorzieme', 'trois cent soixante quinzieme', 'trois cent soixante seizieme', 'trois cent soixante dix septieme', 'trois cent soixante dix huitieme', 'trois cent soixante dix neuvieme', 'trois cent quatre vingtieme', 'trois cent quatre vingt unieme', 'trois cent quatre vingt deuxieme', 'trois cent quatre vingt troisieme', 'trois cent quatre vingt quatrieme', 'trois cent quatre vingt cinquieme', 'trois cent quatre vingt sixieme', 'trois cent quatre vingt septieme', 'trois cent quatre vingt huitieme', 'trois cent quatre vingt neuvieme', 'trois cent quatre vingt dixieme', 'trois cent quatre vingt onzieme', 'trois cent quatre vingt douzieme', 'trois cent quatre vingt treizieme', 'trois cent quatre vingt quatorzieme', 'trois cent quatre vingt quinzieme', 'trois cent quatre vingt seizieme', 'trois cent quatre vingt dix septieme', 'trois cent quatre vingt dix huitieme', 'trois cent quatre vingt dix neuvieme', 'quatre centieme', 'quatre cent unieme', 'quatre cent deuxieme', 'quatre cent troisieme', 'quatre cent quatrieme', 'quatre cent cinquieme', 'quatre cent sixieme', 'quatre cent septieme', 'quatre cent huitieme', 'quatre cent neuvieme', 'quatre cent dixieme', 'quatre cent onzieme', 'quatre cent douzieme', 'quatre cent treizieme', 'quatre cent quatorzieme', 'quatre cent quinzieme', 'quatre cent seizieme', 'quatre cent dix septieme', 'quatre cent dix huitieme', 'quatre cent dix neuvieme', 'quatre cent vingtieme', 'quatre cent vingt et unieme', 'quatre cent vingt deuxieme', 'quatre cent vingt troisieme', 'quatre cent vingt quatrieme', 'quatre cent vingt cinquieme', 'quatre cent vingt sixieme', 'quatre cent vingt septieme', 'quatre cent vingt huitieme', 'quatre cent vingt neuvieme', 'quatre cent trentieme', 'quatre cent trente et unieme', 'quatre cent trente deuxieme', 'quatre cent trente troisieme', 'quatre cent trente quatrieme', 'quatre cent trente cinquieme', 'quatre cent trente sixieme', 'quatre cent trente septieme', 'quatre cent trente huitieme', 'quatre cent trente neuvieme', 'quatre cent quarantieme', 'quatre cent quarante et unieme', 'quatre cent quarante deuxieme', 'quatre cent quarante troisieme', 'quatre cent quarante quatrieme', 'quatre cent quarante cinquieme', 'quatre cent quarante sixieme', 'quatre cent quarante septieme', 'quatre cent quarante huitieme', 'quatre cent quarante neuvieme', 'quatre cent cinquantieme', 'quatre cent cinquante et unieme', 'quatre cent cinquante deuxieme', 'quatre cent cinquante troisieme', 'quatre cent cinquante quatrieme', 'quatre cent cinquante cinquieme', 'quatre cent cinquante sixieme', 'quatre cent cinquante septieme', 'quatre cent cinquante huitieme', 'quatre cent cinquante neuvieme', 'quatre cent soixantieme', 'quatre cent soixante et unieme', 'quatre cent soixante deuxieme', 'quatre cent soixante troisieme', 'quatre cent soixante quatrieme', 'quatre cent soixante cinquieme', 'quatre cent soixante sixieme', 'quatre cent soixante septieme', 'quatre cent soixante huitieme', 'quatre cent soixante neuvieme', 'quatre cent soixante dixieme', 'quatre cent soixante et onzieme', 'quatre cent soixante douzieme', 'quatre cent soixante treizieme', 'quatre cent soixante quatorzieme', 'quatre cent soixante quinzieme', 'quatre cent soixante seizieme', 'quatre cent soixante dix septieme', 'quatre cent soixante dix huitieme', 'quatre cent soixante dix neuvieme', 'quatre cent quatre vingtieme', 'quatre cent quatre vingt unieme', 'quatre cent quatre vingt deuxieme', 'quatre cent quatre vingt troisieme', 'quatre cent quatre vingt quatrieme', 'quatre cent quatre vingt cinquieme', 'quatre cent quatre vingt sixieme', 'quatre cent quatre vingt septieme', 'quatre cent quatre vingt huitieme', 'quatre cent quatre vingt neuvieme', 'quatre cent quatre vingt dixieme', 'quatre cent quatre vingt onzieme', 'quatre cent quatre vingt douzieme', 'quatre cent quatre vingt treizieme', 'quatre cent quatre vingt quatorzieme', 'quatre cent quatre vingt quinzieme', 'quatre cent quatre vingt seizieme', 'quatre cent quatre vingt dix septieme', 'quatre cent quatre vingt dix huitieme', 'quatre cent quatre vingt dix neuvieme', 'cinq centieme']

#############################################################################################
#############################################################################################
#############################################################################################

