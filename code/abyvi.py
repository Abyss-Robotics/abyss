#coding: utf8

import snowboydecoder
import wave
import sys
import signal
import time
import os
import speech_recognition as sr
import re

"""
[ABYRA]-->ABYss Request Acquisition system
[ABYRP]-->ABYss Request Processing system
[ABYOX]-->ABYss Operations eXecuter system
"""

#### VAR ####
RECORDED_FILE='./testRecording.wav'
#############

def display(sentence):
	os.system('/home/pi/speech.sh "'+str(sentence)+'"')

interrupted = False

class RequestAcquisition(object):
	"""[ABYRA]
	"""
	def __init__(self, hotword_model, exitEvent, vocalEvent):
		"""Assure l'acquisition d'une requête en language naturel.
		Utilise les méthodes de la classe pour assurer le traitement de la requête.
		"""
		self.model=hotword_model
		self.SnowboyDetect = snowboydecoder.HotwordDetector(self.model, sensitivity=0.5, audio_gain=2)
		self.exitEvent=exitEvent
		self.vocalEvent=vocalEvent
		self.recorded=False

	def exit_callback(self):
		global interrupted
		return (self.exitEvent.isSet() or interrupted or self.vocalEvent.isSet())

	def waitRequest(self):
		global interrupted
		interrupted=False
		self.SnowboyDetect.start(detected_callback=self.recordRequest, interrupt_check=self.exit_callback,sleep_time=0.03)
		if self.recorded:
			self.recorded=False
			r = sr.Recognizer()
			file = sr.AudioFile(RECORDED_FILE)
			with file as source:
				audio = r.record(source)
			try:
				os.system('sudo python3 abyli.py load 2')
				text=r.recognize_google(audio, language='fr-FR')
				os.system('sudo python3 abyli.py turnOff')
				print(text)
				return text
			except sr.UnknownValueError:
				print('audio file cannot be analyse')
				return 1
		return 1

	def recordRequest(self):
		global interrupted
		os.system('sudo python3 abyli.py listening')
		recording=False
		stopCounter=0
		fileData=''
		time.sleep(1)
		self.SnowboyDetect.ring_buffer.get()
		while not self.exitEvent.isSet():
			data = self.SnowboyDetect.ring_buffer.get()
			if len(data) == 0:
				time.sleep(0.03)
				continue
			vad=self.SnowboyDetect.detector.RunDetection(data)
			print(vad)
			if vad == 0:
				stopCounter=0
				if not recording:
					recording=True
					print('Start')
					os.system('sudo python3 abyli.py recording')
				fileData+=data
				time.sleep(1)
			elif vad == -2:
				if recording:
					fileData+=data
				if stopCounter>10 and recording:
					print('End')

					c=0
					while c<5 and not self.exitEvent.isSet():
						c+=1
						time.sleep(0.1)
					data = self.SnowboyDetect.ring_buffer.get()
					fileData+=data

					recording=False
					file=wave.open(RECORDED_FILE, 'wb')
					file.setnchannels(1)
					file.setframerate(16000)
					file.setsampwidth(2)
					file.writeframes(fileData)
					file.close()
					break
				elif recording:
					stopCounter+=1
				time.sleep(0.03)
			else:
				print('ERROR')
		interrupted = True
		self.recorded = True
		os.system('sudo python3 abyli.py turnOff')

	def ask(self, question):
		display(question)
		self.recordRequest()
		r = sr.Recognizer()
		file = sr.AudioFile(RECORDED_FILE)
		with file as source:
			audio = r.record(source)
		try:
			text=r.recognize_google(audio, language='fr-FR')
			print(text)
			return text
		except sr.UnknownValueError:
			display("Désolé, je n'ai pas entendu ce que vous m'avez demandé.")
			print('audio file cannot be analyse')
			self.ask(question)


class RequestProcesser(object):
	"""[ABYRP]
	"""
	def __init__(self, abyra, abyrd, abyme):
		self.abyra=abyra
		self.abyrd=abyrd
		self.abyme=abyme

	def run(self, request1):
		"""Assure le traitement d'une requête en language naturel.
		Utilise les méthodes de la classe pour assurer le traitement de la requête.
		Exemple:
		'Programme une alarme à 9h00.'
		--> *Création d'un event [ALRM] à 9:00:00 le jour même*
		"""
		formatedRequest=self.format_48Y55(request1)
		requestData=self.analyze(formatedRequest)
		return requestData

	def format_48Y55(self, string1):
		"""Convertis une chaîne de caractère en liste de mots (chaînes de caractères)
		Cela permet de rendre la requête lisible par les autres méthodes.
		Exemple:
		'Ceci est un test. Cela, également!'
		--> ['ceci', 'est, 'un', 'test', 'cela', 'également']
		"""

		#Passage aux minuscules pour désensibiliser à la casse
		string1=string1.lower()

		#Supression des caractères de ponctuation
		string1=string1.replace('(','')
		string1=string1.replace(')','')
		string1=string1.replace('"','')

		string1=string1.replace(',','')
		string1=string1.replace(';','')

		string1=string1.replace(':','')

		string1=string1.replace('.','')
		string1=string1.replace('?','')
		string1=string1.replace('!','')

		string1=string1.replace('\'',' ')
		string1=string1.replace('-',' ')

		#Suppression des accents
		string1=string1.replace('é', 'e')
		string1=string1.replace('è', 'e')
		string1=string1.replace('ê', 'e')
		string1=string1.replace('ë', 'e')

		string1=string1.replace('î', 'i')
		string1=string1.replace('ï', 'i')

		string1=string1.replace('ù', 'u')

		string1=string1.replace('à', 'a')
		string1=string1.replace('â', 'a')

		string1=str(string1)

		#Séparation en liste
		formatedRequest=string1.split(' ')
		for word in formatedRequest:
			word=word.replace(' ','')

		return formatedRequest

	def check(self, list1):
		#hotwords checker
		self.keywords=[]
		for element in list1:
			for words in enumerate(self.abyrd.keywords):
				for word in words[1]:
					if element==word:
						self.keywords.append(words[0])
						break
		if self.keywords==[]:
			return 1 #No keywords!
		else:
			return 0

	def analyze(self, list1):
		"""Analyse les données d'input formatées et ressort des données de requêtes.
		Ces données contiennent le numéro de requête et les autres informations nécessaires à la requête.
		Exemple:
		'['programme', 'une, 'alarme', 'à', '9', 'heures']'
		--> (10201, 1, '9h')
		"""

		#hotwords identifier
		self.keywords=[]
		for element in list1:
			for words in enumerate(self.abyrd.keywords):
				for word in words[1]:
					if element==word:
						self.keywords.append(words[0])
						break
		if self.keywords==[]:
			return 1 #No keywords!

		#hotwords analyser (request deduction)
		requestKeywords=set(self.keywords)
		score=-1
		issue=False
		for request in self.abyrd.requests:
			if len(requestKeywords & set(request.keywords))==len(request.keywords):
				if len(requestKeywords & set(request.keywords))==len(requestKeywords): #Tout les mots clés de la demande vocale correspondent
					score=0
					self.requestID=request.idNumber
					break
				else: #Il y a des mots clés en plus dans la requête
					if len(requestKeywords)-len(requestKeywords & set(request.keywords))<score or score==-1:
						issue=False
						score=len(requestKeywords)-len(requestKeywords & set(request.keywords))
						self.requestID=request.idNumber
					elif len(requestKeywords)-len(requestKeywords & set(request.keywords))==score:
						issue=True
					else:
						pass
		else:
			if issue or score<0:
				print("Désolé, je ne comprends pas.")
				return 1 #Severals requests, can't understand!

		#request data acquisition
		for request in self.abyrd.requests:
			if request.idNumber == self.requestID:
				if request.hasVariables==True:
					self.variablesData={}
					for variable in request.variables:
						if re.search(variable.variableRegex.regex, ' '.join(list1)):
							subvariablesData={}
							for subVariable in variable.variableRegex.subVariables:
								exec(subVariable[1], {'outputVar': subvariablesData}, {'inputStr': re.search(variable.variableRegex.regex, ' '.join(list1)).group()})
							self.variablesData[variable.variableName]=subvariablesData.copy()
						else:
							inputAnswer=self.abyra.ask(variable.variableQuestion)
							while not re.search(variable.variableRegex.regex, ' '.join(self.format_48Y55(inputAnswer))):
								inputAnswer=self.abyra.ask("Désolé je n'ai pas compris, "+variable.variableQuestion)

							subvariablesData={}
							for subVariable in variable.variableRegex.subVariables:
								exec(subVariable[1], {'outputVar': subvariablesData}, {'inputStr': re.search(variable.variableRegex.regex, ' '.join(self.format_48Y55(inputAnswer))).group()})
							self.variablesData[variable.variableName]=subvariablesData.copy()
					self.requestData=(self.requestID, self.variablesData)
				else:
					self.requestData=(self.requestID,None)
				break

		#request data transmission
		return self.requestData


class OperationsExecuter(object):
	def __init__(self, abyrd, abyme, mainMailbox, mainEvent):
		self.abyrd=abyrd
		self.abyme=abyme
		self.mainMailbox=mainMailbox
		self.mainEvent=mainEvent
	def executeRequest(self, requestData):
		if requestData==1:
			return 1
		requestAdress='ERROR'
		for request in enumerate(self.abyrd.requests):
			if request[1].idNumber==requestData[0]:
				requestAdress=request[0]
				break
		else:
			display("Désolé, il y a eu un problème")
			return 404

		if not self.abyrd.requests[requestAdress].hasVariables:
			exec(self.abyrd.requests[requestAdress].code) #code pour requêtes ne nécessitant pas de variables
		else:
			requestData[1]['self']=self
			exec(self.abyrd.requests[requestAdress].code, requestData[1])
	def display(self,sentence,errorDisplay=False):
		if not errorDisplay:
			os.system('sudo python3 abyli.py speaking')
        		os.system('/home/pi/speech.sh "'+str(sentence)+'"')
			os.system('sudo python3 abyli.py turnOff')
		else:
			os.system('/home/pi/speech.sh "'+str(sentence)+'"')
