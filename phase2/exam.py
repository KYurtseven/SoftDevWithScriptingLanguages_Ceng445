import uuid
import copy
import json
import datetime
import pymongo
import random
import subprocess
import os
from question import Question
from QBank import QBank
from threading import Lock,Thread,Condition,RLock,Semaphore

connection = pymongo.MongoClient("mongodb://localhost")
db = connection["latexdb"]
questions = db["T_QUESTIONS"]
exams = db["T_EXAMS"]


class Exam:
	'''
		It stores previous exams
	'''

	def __init__(self, lst):
		'''
			initialize exam with given list of questions
		'''
		self.mutex = RLock()

		self.question_ids = lst
		self.questions = []
		self.shuffled_exams = []

		qbank = QBank()

		# create question object for each qid
		for qid in self.question_ids:
			q = qbank.getQuestion(qid)

			cur_ques = Question(q['q_id'])

			cur_ques.constructor(q['body'], q['choices'], q['topics'], q['parent'], q['embeds'])
			cur_ques.updateAskDate(q['ask_date'])

			self.questions.append(cur_ques)

	def createShuffled(self, n):
		'''
			create n number versions of the exam
		'''
		self.mutex.acquire()
		shuffled_exams = []
		book_name = "A"
		
		for i in range(n):
			# create shuffled questions for each n
			shuffled_questions = random.sample(self.questions, len(self.questions))

			# shuffle each question
			for question in shuffled_questions:
				# use question.shuffleQuestion() function to shuffle the question content
				# retrieve question object
				question.shuffleQuestion()

				# replace current question with retrieved shuffled question

			shuffled_exam = {}
			shuffled_exam['book_name'] = book_name
			shuffled_exam['exam'] = shuffled_questions
			shuffled_exams.append(shuffled_exam)

			#increase book_name 
			book_name = str(chr(ord(book_name) + 1))


		self.shuffled_exams = shuffled_exams
		self.mutex.release()

	def getLatexExam(self, no):
		'''
			Return string version of the exam
		'''
		self.mutex.acquire()
		s_e = self.shuffled_exams[no]
		s_iter = iter(s_e['exam'])

		result = ""
		result += "\\documentclass{exam} \n"
		result += "\\usepackage{graphicx} \n"
		result += "\\begin{document} \n"
		result += "\\newcommand\\examtypemarker{}{\\centerline{\\framebox{\\Huge " + str(s_e['book_name']) + "}}"
		result += "\\begin{questions}"

		try:
		    while True:
		        i = next(s_iter)
		        result += i.getLatex(False)
		        result += "\n" 
		        result += "\\newline"
		except StopIteration:
		    pass

		result += "\\end{questions}"
		result += "\\end{document}"

		self.mutex.release()
		return result



	def getPDFExam(self, no):

		self.mutex.acquire()
		latex_exam = self.getLatexExam(no)

		f = open("exam.tex","w")
		f.write(latex_exam)
		f.close()

		subprocess.call(['pdflatex','exam.tex'], shell=False)

		os.unlink("exam.log")
		os.unlink("exam.aux")
		# call subprocess for each latex exam

		self.mutex.release()


	def save():
		'''
			save exam to the database
		'''
		self.mutex.acquire()
		try:
			# TODO
			# cannot convert mutex to dict
			# fix for phase3
			exams.insert(self.__dict__)
		
		except Exception as e:
			print e

		self.mutex.release()

	def reload():
		'''
			find all past exams
		'''

		# TODO
		# Future work
		# We might filter past exams by given date
		self.mutex.acquire()
		try:
			cursor = exams.find({})
			result = []
			for x in cursor:
				new_exam = Exam(x['question_ids'])
				result.append(new_exam)

			return result


		except Exception as e:
			print e
		self.mutex.release()

	def getLatexKey(self,no):
		self.mutex.acquire()
		s_e = self.shuffled_exams[no]
		s_iter = iter(s_e['exam'])

		result = ""
		result += "\\documentclass[answers]{exam} \n"
		result += "\\usepackage{graphicx} \n"
		result += "\\begin{document} \n"
		result += "\\newcommand\\examtypemarker{}{\\centerline{\\framebox{\\Huge " + str(s_e['book_name']) + "}}"
		result += "\\begin{questions}"

		try:
		    while True:
		        i = next(s_iter)
		        result += i.getLatexWithKey()
		        result += "\n" 
		        result += "\\newline"
		except StopIteration:
		    pass

		result += "\\end{questions}"
		result += "\\end{document}"

		self.mutex.release()
		return result


	def getPDFKey(self,no):
		self.mutex.acquire()
		latex_exam_key = self.getLatexKey(no)

		f = open("exam_key.tex","w")
		f.write(latex_exam_key)
		f.close()

		subprocess.call(['pdflatex','exam_key.tex'], shell=False)

		os.unlink("exam_key.log")
		os.unlink("exam_key.aux")

	def getCSVKey(self):
		self.mutex.acquire()
		choice_mark = "A"

		f=open("answer_key.csv","w")
		f.write('')
		f.close()

		f = open("answer_key.csv", "a")
		f.write('no,question_no,answer\n')

		for exam in self.shuffled_exams:
			for question in exam['exam']:
				f.write(exam['book_name']+',')
				question_number = str(exam['exam'].index(question)+1)
				f.write(question_number+',')
				for choice in question.choices:
					if(choice['iscorrect'] == 'true'):
						true_choice = chr(ord('a') + question.choices.index(choice))
						f.write(true_choice)
						f.write("\n")

		f.close()

		self.mutex.release()
