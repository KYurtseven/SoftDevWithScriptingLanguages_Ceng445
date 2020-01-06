import uuid
import copy
import json
import datetime
import pymongo

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
		self.q_id = _id

	def constructor(self, latexbody, choices, topics, parent, embeds):
		'''
			Constructor:
			Gets body, choices, topics, parent, embeds as input.
			Sets ask_date as None.
		'''
		self.body = latexbody
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
		self.body = latextext

	def addTopic(self, text):
		'''
			Add topic to topics list of object.
		'''
		self.topics.append(text)

	def delTopic(self, text):
		'''
			Deletes specific topic from object's topics list.
			If given topic is not found, do nothing.
		'''
		topics = self.topics[:]
		if text in topics:
			index = topics.index(text)
			del topics[index]
			self.topics = topics

	def addEmbed(self, docid):
		'''
			Add embed to embeds array of object.
		'''
		embeds = self.embeds[:]
		embeds.append(docid)
		self.embeds = embeds

	def delEmbed(self, docid):
		'''
			delete an embed
			try except block for possible empty embed array
			NOTE:
				1 != "1" for id searching
		'''
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

	def updateChoice(self, c_id, latextext, correct, pos):
		'''
			update a choice
			set the correctness of the choice
			set the pos of the choice, i.e. START, END or NA
			while shuffling pos info will be used
		'''
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
			
	def updateParent(self, p_id):
		'''
			Update parent.
			ID as input.
		'''
		self.parent = p_id

	def updateAskDate(self, givenDate):
		'''
			Update ask date.
			Date is input. 
			E.g. question.updateAskDate(datetime.datetime(Year, Month, Day))
		'''
		self.ask_date = givenDate

	def save(self):
		'''
			Save question to db
		'''
		try:
			questions.insert(self.__dict__)
		except Exception as e:
			print(e)

	def copy(self):
		'''
			returns deep copy of the object
		'''
		newq = copy.deepcopy(self)
		newq.parent = newq.q_id
		newq.q_id = str(uuid.uuid4())
		newq.ask_date = None
		return newq

	def getLatex(self, shuffled):
		'''
			Get latex version of a question
		'''
		# TODO, fix this is part2
		shuffled = False

		l_body = "\\question {} \\newline\n".format(self.body)
		
		# create choices part
		c = self.choices
		l_choices = "\\begin{oneparchoices}"
				
		for i in c:
			l_choices += "\n \\choice {}".format(i["body"])
			l_choices += "\\newline"
		
		l_choices+= "\n\\end{oneparchoices}"

		return l_body + l_choices
	
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
