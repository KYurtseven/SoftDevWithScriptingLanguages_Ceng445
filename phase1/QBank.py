import json
import pymongo
import uuid
import datetime
from question import Question

connection = pymongo.MongoClient("mongodb://localhost")
db = connection["latexdb"]
questions = db["T_QUESTIONS"]

class QBank:

	def getQuestion(self,id):
		'''
			Find question in database with given ID.
		'''
		try:	
			res = questions.find({ "q_id" :id})
			return res[0]

		except Exception as e:
			print(e)


	def searchByTopic(self,topic):
		'''
			Find Questions according to given topic.
			Returns an array of questions.
		'''
		try:
			cursor = questions.find({"topics": topic})
			result = []
			for x in cursor:
				result.append(x)
			return result
		except Exception as e:
			print(e)


	def searchByAskDate(self,st,end):
		'''
			Find Questions, ask_date is between (st,end).
			If both st and end are 'None', return list of Questions which are not asked yet.
			If st is 'None' and end is not 'None', return list of Questions which are not asked yet and which are asked before given date.
		'''
		try:
			if(st == None and end == None):
				cursor = questions.find({ "ask_date": None}) 
				result = []
				for x in cursor:
					result.append(x)
				return result

			elif(st == None and end != None):
				cursor = questions.find({"ask_date": {"$lt": end}})
				# If a question is not asked before, return that too
				cursor_2 = questions.find({ "ask_date": None})
				result = []
				for x in cursor:
					result.append(x)
				for y in cursor_2:
					result.append(y)
				return result

			elif(st != None and end == None):
				cursor = questions.find({"ask_date": {"$gt": st}})
				result = []
				for x in cursor:
					result.append(x)
				return result
			else:
				cursor = questions.find({"ask_date": {"$gt":st ,"$lt": end}})
				result = []
				for x in cursor:
					result.append(x)
				return result

		except Exception as e:
			print(e)
	
	def getLatex(self,iterator,shuffled):
		'''
			Return string version of the exam
			
		'''
		result = ""
		result += "\\documentclass{exam} \n"
		result += "\\usepackage{graphicx} \n"
		result += "\\begin{document} \n"
		result += "\\begin{questions}"

		try:
		    while True:
		        i = next(iterator)
		        result += i.getLatex(False)
		        result += "\n" 
		        result += "\\newline"
		except StopIteration:
		    pass

		result += "\\end{questions}"
		result += "\\end{document}"

		return result

	def updateAskDate(self,iterator,date):
		'''
			Update ask dates of given questions.
		'''
		try:
			while True:
				i = next(iterator)
				i.updateAskDate(date)
		except StopIteration:
			pass
