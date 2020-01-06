import uuid
import copy
import json
import datetime
import pymongo
import random
from threading import Lock,Thread,Condition,RLock,Semaphore
import random

connection = pymongo.MongoClient("mongodb://localhost")
db = connection["latexdb"]
questions = db["T_QUESTIONS"]

class Question:
	'''
		Class to store a single question in the questionbank
		it has
		id, parent_id, topics[], choices[], body
		ask_date, embeds[]
	'''

	def __init__(self, _id):
		'''
			Initially only sets id of object.
			input: ID(uuid).
		'''
		self.mutex = RLock()
		self.q_id = _id

	def constructor(self, body, choices, topics, parent, embeds):
		'''
			Constructor:
			Gets body, choices, topics, parent, embeds as input.
			Sets ask_date as None.
		'''
		self.body = body
		self.choices = choices
		self.topics = topics
		self.parent = parent 
		self.embeds = embeds
		self.ask_date = None

	def getId(self):
		'''
			Returns ID of the object.
		'''
		return self.q_id

	def updateBody(self, latextext):
		'''
			Update body of object with given text as input.
		'''
		self.mutex.acquire()
		self.body = latextext
		self.mutex.release()

	def addTopic(self, text):
		'''
			Add topic to topics list of object.
		'''
		self.mutex.acquire()
		self.topics.append(text)
		self.mutex.release()

	def delTopic(self, text):
		'''
			Deletes specific topic from object's topics list.
			If given topic is not found, do nothing.
		'''
		self.mutex.acquire()

		topics = self.topics[:]
		if text in topics:
			index = topics.index(text)
			del topics[index]
			self.topics = topics

		self.mutex.release()

	def addEmbed(self, docid):
		'''
			Add embed to embeds array of object.
		'''
		self.mutex.acquire()

		embeds = self.embeds[:]
		embeds.append(docid)
		self.embeds = embeds

		self.mutex.release()
	def delEmbed(self, docid):
		'''
			delete an embed
			try except block for possible empty embed array
			NOTE:
				1 != "1" for id searching
		'''
		self.mutex.acquire()

		org_embeds = self.embeds[:]

		try:
			index = 0
			for embed in org_embeds:
				if(embed == docid):
					del org_embeds[index]
					self.embeds = org_embeds
					return
				else:
					index += 1
			print("Embed is not found")

		except Exception as e:
			print(e)

		self.mutex.release()
	
	def updateChoice(self, c_id, latextext, correct, pos):
		'''
			update a choice
			set the correctness of the choice
			set the pos of the choice, i.e. START, END or NA
			while shuffling pos info will be used
		'''
		self.mutex.acquire()

		choices = self.choices[:]
		try:
			cur_choice = choices[c_id]
			
			cur_choice["body"] = latextext
			cur_choice["iscorrect"] = correct
			cur_choice["pos"] = pos
			
			self.choices = choices

		except Exception as e:
			# possible out of index error
			print(e)
		
		self.mutex.release()

	def updateParent(self, p_id):
		'''
			Update parent.
			ID as input.
		'''
		self.mutex.acquire()
		self.parent = p_id
		self.mutex.release()

	def updateAskDate(self, givenDate):
		'''
			Update ask date.
			Date is input. 
			E.g. question.updateAskDate(datetime.datetime(Year, Month, Day))
		'''
		self.mutex.acquire()
		self.ask_date = givenDate
		self.mutex.release()

	def save(self):
		'''
			Save question to db
		'''
		self.mutex.acquire()
		
		try:
			q = {}
			q['q_id'] = self.q_id

			q['body'] = self.body
			q['choices'] = self.choices
			q['topics'] = self.topics
			q['parent'] = self.parent 
			q['embeds'] = self.embeds
			q['ask_date'] = self.ask_date

			questions.insert(q)
		except Exception as e:
			print(e)
		
		self.mutex.release()

		return

	def copy(self):
		'''
			returns deep copy of the object
		'''
		self.mutex.acquire()
		newq = Question(self.q_id)
		newq.constructor(self.body, self.choices, self.topics, self.parent, self.embeds)
		
		#newq = copy.deepcopy(self)
		newq.parent = newq.q_id
		newq.q_id = str(uuid.uuid4())
		newq.ask_date = None
		
		self.mutex.release()

		return newq

	def getLatex(self, shuffled):
		'''
			Get latex version of a question
		'''
		self.mutex.acquire()

		if(shuffled == False):
			l_body = "\\question {} \\newline\n".format(self.body)
			# create choices part
			c = self.choices
			l_choices = "\\begin{oneparchoices}"
			for i in c:
				l_choices += "\n \\choice {}".format(i["body"])
				l_choices += "\\newline"
			l_choices+= "\n\\end{oneparchoices}"
			
			self.mutex.release()

			return l_body + l_choices

		else:
			l_body = "\\question {} \\newline\n".format(self.body)
			st_arr = []		#choice with start position
			end_arr = []	#choice with end position
			na_arr = []		#choices without position
			c = self.choices
			for x in c:
				if x["pos"] == "START":
					st_arr.append(x)
				elif x["pos"] == "END":
					end_arr.append(x)
				else:
					na_arr.append(x)

			random.shuffle(na_arr) #choices without position are shuffled here

			l_choices = "\\begin{oneparchoices}"
			#if there is a choice with start position
			if(st_arr != []):
				l_choices += "\n \\choice {}".format(st_arr[0]["body"])
				l_choices += "\\newline"
			
			for i in na_arr:
				l_choices += "\n \\choice {}".format(i["body"])
				l_choices += "\\newline"
			#if there is a choice with end position
			if(end_arr != []):
				l_choices += "\n \\choice {}".format(end_arr[0]["body"])
				l_choices += "\\newline"

			l_choices+= "\n\\end{oneparchoices}"
			
			self.mutex.release()

			return l_body + l_choices

	def getLatexWithKey(self):
		'''
			Get latex version of a question
		'''
		self.mutex.acquire()

		l_body = "\\question {} \\newline\n".format(self.body)
		
		# create choices part
		c = self.choices
		l_choices = "\\begin{oneparchoices}"
				
		for i in c:
			if(i['iscorrect']=='true'):
				l_choices += "\n \\correctchoice {}".format(i["body"])
			else:
				l_choices += "\n \\choice {}".format(i["body"])
			l_choices += "\\newline"
		
		l_choices+= "\n\\end{oneparchoices}"

		self.mutex.release()

		return l_body + l_choices

	def shuffleQuestion(self):
		'''
			Helper function to shuffle a question.
		'''
		self.mutex.acquire()
		
		st_arr = [] 	#question with start position
		end_arr = []	#question with end position
		na_arr = []		#questions without position
		c = self.choices
		shuffled_choices = []
		for x in c:
			if x["pos"] == "START":
				st_arr.append(x)
			elif x["pos"] == "END":
				 end_arr.append(x)
			else:
				na_arr.append(x)

		random.shuffle(na_arr)
		if(st_arr != []):
			shuffled_choices.append(st_arr[0])

		for ques in na_arr:
			shuffled_choices.append(ques)

		if(end_arr != []):
			shuffled_choices.append(end_arr[0])

		self.choices = shuffled_choices

		self.mutex.release()

		return

	def __str__(self):
		'''
			For printing purposes
			Try except blocks for possible uninitilized attributes
		'''
		ret=""
		ret += "id: " + str(self.q_id)
		
		try:
			ret += "\ntopics: " + str(self.topics)
		except:
			#print("no topics are present")
			pass

		ret += "\nbody: " + str(self.body)
		ret += "\nchoices: " + str(self.choices)
		
		try:
			ret += "\nparent: " + str(self.parent)
		except:
			#print("parent id is None")
			pass
		
		try:
			ret += "\nembeds: " + str(self.embeds)
		except:
			#print("No embeds are present")	
			pass
		
		try:
			ret += "\nask_date: " + str(self.ask_date)
		except:
			pass

		ret += "\n"
		return ret
