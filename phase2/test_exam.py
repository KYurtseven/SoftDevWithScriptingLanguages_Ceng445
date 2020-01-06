import unittest
import uuid
import datetime
import pymongo
import filecmp
import json
from question import Question
from QBank import QBank
from exam import Exam

id_1 = ""
id_2 = ""
id_3 = ""
id_4 = ""
lst = []

connection = pymongo.MongoClient("mongodb://localhost")
db = connection["latexdb"]
questions = db["T_QUESTIONS"]
exams = db["T_EXAMS"]



class TestExam(unittest.TestCase):

	def setUp(self):
		print('setUp\n')

		global id_1
		global id_2
		global id_3
		global id_4
		global lst
		id_1 = str(uuid.uuid4())
		id_2 = str(uuid.uuid4())
		id_3 = str(uuid.uuid4())
		id_4 = str(uuid.uuid4())

		self.question_1 = Question(id_1)
		self.question_1.constructor('How many siblings do you have?', 					#body
							[{'body':'None', 'iscorrect': 'false', 'pos': 'START' },		#choices
							{'body':'One', 'iscorrect': 'false', 'pos': 'None' },
							{'body':'Two', 'iscorrect': 'true', 'pos': 'None' },
							{'body':'Three', 'iscorrect': 'false', 'pos': 'None' },
							{'body':'Many', 'iscorrect': 'false', 'pos': 'None' }
							], 
							['personal','sample'], 										#topics
							None, 														#parent
							[])															#embeds

		self.question_2 = Question(id_2)
		self.question_2.constructor('Solve the following equation for $x$:\\\n\\[ 2 x^2 + x + 1 = 0 \\]', 					#body
							[{'body':'1, -1', 'iscorrect': 'false', 'pos': 'None' },										#choices
							{'body':'1, 0', 'iscorrect': 'true', 'pos': 'None' },
							{'body':'$x \\rightarrow \\infty$', 'iscorrect': 'false', 'pos': 'None' },
							{'body':'0, 0', 'iscorrect': 'false', 'pos': 'START' },
							{'body':'None of the above', 'iscorrect': 'false', 'pos': 'END' }
							], 
							['math', 'equation'], 										#topics
							None, 														#parent
							[])															#embeds

		self.question_3 = Question(id_3)
		self.question_3.constructor('Whose logo this is:\\newline \n\\includegraphics[height=3em]{metulogo}', 					#body
							[{'body':'Audi', 'iscorrect': 'false', 'pos': 'None' },		#choices
							{'body':'Batman', 'iscorrect': 'false', 'pos': 'None' },
							{'body':'Bayburt', 'iscorrect': 'false', 'pos': 'None' },
							{'body':'THY', 'iscorrect': 'false', 'pos': 'None' },
							{'body':'None of the above', 'iscorrect': 'true', 'pos': 'END' }
							], 
							['logos','sample'], 										#topics
							None, 														#parent
							['metulogo'])												#embeds

		self.question_4 = Question(id_4)
		self.question_4.constructor('Which of the following is for ``no entrance'' sign?', 					#body
							[{'body':'\\includegraphics[height=2em]{metulogo}', 'iscorrect': 'false', 'pos': 'None' },		#choices
							{'body':'\\includegraphics[height=2em]{cenglogo}', 'iscorrect': 'false', 'pos': 'None' },
							{'body':'\\includegraphics[height=2em]{stopsign}', 'iscorrect': 'true', 'pos': 'None' },
							{'body':'\\includegraphics[height=2em]{noentry}', 'iscorrect': 'false', 'pos': 'None' },
							{'body':'None of the above', 'iscorrect': 'false', 'pos': 'END' }
							], 
							['logos'], 										#topics
							None, 														#parent
							['metulogo','cenglogo','stopsign','noentry'])												#embeds


		lst = []
		lst.append(id_1)
		lst.append(id_2)
		lst.append(id_3)
		lst.append(id_4)

		self.question_1.save()
		self.question_2.save()
		self.question_3.save()
		self.question_4.save()

		self.exam = Exam(lst)


	def tearDown(self):
		print('tearDown\n')
		questions.delete_one({'q_id': id_1})
		questions.delete_one({'q_id': id_2})
		questions.delete_one({'q_id': id_3})
		questions.delete_one({'q_id': id_4})

	def test_initial(self):
		print('initial\n')
		test_exam = Exam(lst)
		self.assertEqual(len(test_exam.questions),4)
		self.assertEqual(test_exam.questions[0].q_id,id_1)
		self.assertEqual(test_exam.questions[1].q_id,id_2)
		self.assertEqual(test_exam.questions[2].q_id,id_3)
		self.assertEqual(test_exam.questions[3].q_id,id_4)
		self.assertEqual(test_exam.shuffled_exams, [])


	def test_createShuffled(self):
		print('createShuffled\n')

		#check length of shuffled_exams before and after shuffle
		self.assertEqual(self.exam.shuffled_exams, [])
		self.exam.createShuffled(4)
		self.assertEqual(len(self.exam.shuffled_exams), 4)

		#check for book_name of all shuffled exams
		for i in range(4):
			self.assertEqual(len(self.exam.shuffled_exams[i]['exam']),4)

		self.assertEqual(self.exam.shuffled_exams[0]['book_name'],"A")
		self.assertEqual(self.exam.shuffled_exams[1]['book_name'],"B")
		self.assertEqual(self.exam.shuffled_exams[2]['book_name'],"C")
		self.assertEqual(self.exam.shuffled_exams[3]['book_name'],"D")


		#check if questions are shuffled
		#Fails if shuffled version of exam is same.
		a = (id_1 == self.exam.shuffled_exams[0]['exam'][0].q_id)
		b = (id_2 == self.exam.shuffled_exams[0]['exam'][1].q_id)
		c = (id_3 == self.exam.shuffled_exams[0]['exam'][2].q_id)
		d = (id_4 == self.exam.shuffled_exams[0]['exam'][3].q_id)
		self.assertEqual(a and b and c and d, False)


		#check if two shuffled versions are same
		#Fails if shuffling algorithm creates two same exams
		a = (self.exam.shuffled_exams[0]['exam'][0].q_id == self.exam.shuffled_exams[1]['exam'][0].q_id)
		b = (self.exam.shuffled_exams[0]['exam'][1].q_id == self.exam.shuffled_exams[1]['exam'][1].q_id)
		c = (self.exam.shuffled_exams[0]['exam'][2].q_id == self.exam.shuffled_exams[1]['exam'][2].q_id)
		d = (self.exam.shuffled_exams[0]['exam'][3].q_id == self.exam.shuffled_exams[1]['exam'][3].q_id)
		self.assertEqual(a and b and c and d, False)

		#check if positions of START,END choices are correct after shuffle
		for i in range(4):
			for j in range(4):
				if(self.exam.shuffled_exams[i]['exam'][j].q_id == id_2):
					self.assertEqual(self.exam.shuffled_exams[i]['exam'][j].choices[0]['body'],'0, 0')
					self.assertEqual(self.exam.shuffled_exams[i]['exam'][j].choices[4]['body'],'None of the above')


	def test_getLatexExam(self):
		print('getLatexExam\n')

		self.exam.createShuffled(2)

		sample_1 = self.exam.getLatexExam(0)

		sample_2 = self.exam.getLatexExam(1)

		result = (sample_1 == sample_2)

		self.assertEqual(result,False)


	def test_getLatexKey(self):
		print('getLatexKey\n')

		self.exam.createShuffled(2)

		sample_1 = self.exam.getLatexKey(0)

		sample_2 = self.exam.getLatexKey(1)

		result = (sample_1 == sample_2)

		self.assertEqual(result,False)
		

	def test_getCSVKey(self):
		print('getCSVKey\n')

		self.exam.createShuffled(3)
		self.exam.getCSVKey()
		f=open("answer_key.csv","r")
		sample_1 = f.read()
		f.close()

		self.exam.createShuffled(3)
		self.exam.getCSVKey()
		f=open("answer_key.csv","r")
		sample_2 = f.read()
		f.close()

		self.assertEqual(sample_1==sample_2,False)


	def test_getPDF(self):
		print('getPDF\n')

		self.exam.createShuffled(1)
		self.exam.getPDFExam(0)
		self.exam.getPDFKey(0)


if __name__ == '__main__':
	unittest.main()