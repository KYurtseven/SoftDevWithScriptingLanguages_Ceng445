import unittest
import uuid
import datetime
import pymongo
import filecmp
from question import Question
from QBank import QBank

connection = pymongo.MongoClient("mongodb://localhost")
db = connection["latexdb"]
questions = db["T_QUESTIONS"]

id_1 = ""
id_2 = ""
id_3 = ""
id_4 = ""

qbank = QBank()

class TestQbank(unittest.TestCase):

	def setUp(self):
		print('setUp')

		global id_1
		global id_2
		global id_3
		global id_4
		id_1 = str(uuid.uuid4())
		id_2 = str(uuid.uuid4())
		id_3 = str(uuid.uuid4())
		id_4 = str(uuid.uuid4())

		self.question_1 = Question(id_1)
		self.question_1.constructor('How many siblings do you have?', 					#body
							[{'body':'None', 'iscorrect': 'false', 'pos': 'None' },		#choices
							{'body':'One', 'iscorrect': 'false', 'pos': 'None' },
							{'body':'Two', 'iscorrect': 'false', 'pos': 'None' },
							{'body':'Three', 'iscorrect': 'false', 'pos': 'None' },
							{'body':'Many', 'iscorrect': 'false', 'pos': 'None' }
							], 
							['personal','sample'], 										#topics
							None, 														#parent
							[])															#embeds

		self.question_2 = Question(id_2)
		self.question_2.constructor('Solve the following equation for $x$:\\\n\\[ 2 x^2 + x + 1 = 0 \\]', 					#body
							[{'body':'1, -1', 'iscorrect': 'false', 'pos': 'None' },										#choices
							{'body':'1, 0', 'iscorrect': 'false', 'pos': 'None' },
							{'body':'$x \\rightarrow \\infty$', 'iscorrect': 'false', 'pos': 'None' },
							{'body':'0, 0', 'iscorrect': 'false', 'pos': 'None' },
							{'body':'None of the above', 'iscorrect': 'false', 'pos': 'None' }
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
							{'body':'None of the above', 'iscorrect': 'false', 'pos': 'None' }
							], 
							['logos','sample'], 										#topics
							None, 														#parent
							['metulogo'])												#embeds

		self.question_4 = Question(id_4)
		self.question_4.constructor('Which of the following is for ``no entrance'' sign?', 					#body
							[{'body':'\\includegraphics[height=2em]{metulogo}', 'iscorrect': 'false', 'pos': 'None' },		#choices
							{'body':'\\includegraphics[height=2em]{cenglogo}', 'iscorrect': 'false', 'pos': 'None' },
							{'body':'\\includegraphics[height=2em]{stopsign}', 'iscorrect': 'false', 'pos': 'None' },
							{'body':'\\includegraphics[height=2em]{noentry}', 'iscorrect': 'false', 'pos': 'None' },
							{'body':'None of the above', 'iscorrect': 'false', 'pos': 'None' }
							], 
							['logos'], 										#topics
							None, 														#parent
							['metulogo','cenglogo','stopsign','noentry'])												#embeds

		self.question_1.updateAskDate(datetime.datetime(2018, 12, 5))
		self.question_2.updateAskDate(datetime.datetime(2017, 10, 9))

		self.question_1.save()
		self.question_2.save()
		self.question_3.save()


	def tearDown(self):
		print('tearDown\n')

		questions.delete_one({'q_id': id_1})
		questions.delete_one({'q_id': id_2})
		questions.delete_one({'q_id': id_3})


	def test_getQuestion(self):
		print("test_getQuestion")

		self.assertEqual(self.question_1.q_id, qbank.getQuestion(id_1)["q_id"])
		self.assertEqual(self.question_1.body, qbank.getQuestion(id_1)["body"])
		self.assertEqual(self.question_1.topics, qbank.getQuestion(id_1)["topics"])
		self.assertEqual(self.question_1.parent, qbank.getQuestion(id_1)["parent"])
		self.assertEqual(self.question_1.embeds, qbank.getQuestion(id_1)["embeds"])
		self.assertEqual(self.question_1.ask_date, qbank.getQuestion(id_1)["ask_date"])
		self.assertEqual(self.question_1.choices, qbank.getQuestion(id_1)["choices"])

		self.assertEqual(self.question_2.q_id, qbank.getQuestion(id_2)["q_id"])
		self.assertEqual(self.question_2.body, qbank.getQuestion(id_2)["body"])
		self.assertEqual(self.question_2.topics, qbank.getQuestion(id_2)["topics"])
		self.assertEqual(self.question_2.parent, qbank.getQuestion(id_2)["parent"])
		self.assertEqual(self.question_2.embeds, qbank.getQuestion(id_2)["embeds"])
		self.assertEqual(self.question_2.ask_date, qbank.getQuestion(id_2)["ask_date"])
		self.assertEqual(self.question_2.choices, qbank.getQuestion(id_2)["choices"])

		self.assertEqual(self.question_3.q_id, qbank.getQuestion(id_3)["q_id"])
		self.assertEqual(self.question_3.body, qbank.getQuestion(id_3)["body"])
		self.assertEqual(self.question_3.topics, qbank.getQuestion(id_3)["topics"])
		self.assertEqual(self.question_3.parent, qbank.getQuestion(id_3)["parent"])
		self.assertEqual(self.question_3.embeds, qbank.getQuestion(id_3)["embeds"])
		self.assertEqual(self.question_3.ask_date, qbank.getQuestion(id_3)["ask_date"])
		self.assertEqual(self.question_3.choices, qbank.getQuestion(id_3)["choices"])

	def test_searchByTopic(self):
		print("test_searchByTopic")

		result_list = qbank.searchByTopic("math")
		for x in result_list:
			self.assertIn("math", x["topics"])
			self.assertEqual(x["q_id"], id_2)

		result_list = qbank.searchByTopic("sample")
		for x in result_list:
			self.assertIn("sample", x["topics"])
			self.assertIn(x["q_id"], [id_1,id_3])


	def test_updateAskDate(self):
		print("test_updateAskDate")

		question_list = []
		question_list.append(self.question_1)
		question_list.append(self.question_2)
		question_list.append(self.question_3)
	
		question_iter = iter(question_list)

		qbank.updateAskDate(question_iter,datetime.datetime(2014, 7, 8, 18, 17, 28, 324000))

		self.assertEqual(self.question_1.ask_date, datetime.datetime(2014, 7, 8, 18, 17, 28, 324000))
		self.assertEqual(self.question_2.ask_date, datetime.datetime(2014, 7, 8, 18, 17, 28, 324000))
		self.assertEqual(self.question_3.ask_date, datetime.datetime(2014, 7, 8, 18, 17, 28, 324000))

		question_iter = iter(question_list)
		qbank.updateAskDate(question_iter,None)
		self.assertEqual(self.question_1.ask_date, None)
		self.assertEqual(self.question_2.ask_date, None)
		self.assertEqual(self.question_3.ask_date, None)


	def test_searchByAskDate(self):
		print("test_searchByAskDate")

		result_list = qbank.searchByAskDate(None,None)
		for x in result_list:
			self.assertEqual(x["ask_date"], None)
			self.assertIn(x["q_id"], [id_3])

		result_list = qbank.searchByAskDate(datetime.datetime(2016, 11, 9),datetime.datetime(2017, 11, 9))
		for x in result_list:
			self.assertEqual(x["ask_date"], datetime.datetime(2017, 10, 9))
			self.assertIn(x["q_id"], [id_2])

		result_list = qbank.searchByAskDate(datetime.datetime(2017, 11, 9),None)
		for x in result_list:
			self.assertEqual(x["ask_date"], datetime.datetime(2018, 12, 5))
			self.assertIn(x["q_id"], [id_1])

		result_list = qbank.searchByAskDate(datetime.datetime(2017, 11, 9),datetime.datetime(2018, 11, 5))
		self.assertEqual(result_list,[] )

		result_list = qbank.searchByAskDate(datetime.datetime(2016, 11, 9),datetime.datetime(2019, 12, 1))
		for x in result_list:
			self.assertIn(x["ask_date"], [datetime.datetime(2018, 12, 5),datetime.datetime(2017, 10, 9)])
			self.assertIn(x["q_id"], [id_1,id_2])

		result_list = qbank.searchByAskDate(None, datetime.datetime(2017, 11, 9))
		for x in result_list:
			self.assertIn(x["ask_date"],[None,datetime.datetime(2017, 10, 9)])
			self.assertIn(x["q_id"], [id_2,id_3])

	def test_getLatex(self):
		print("test_getLatex")

		question_list = []
		question_list.append(self.question_1)
		question_list.append(self.question_2)
		question_list.append(self.question_3)
		question_list.append(self.question_4)
	
		question_iter = iter(question_list)

		test_string = qbank.getLatex(question_iter,False)
		f = open("test_files/test_qbank_latex.tex", "w")
		f.write(test_string)
		f.close()



if __name__ == '__main__':
	unittest.main()