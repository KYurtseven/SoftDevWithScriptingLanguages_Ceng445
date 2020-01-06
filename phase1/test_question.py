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

a = ""


class TestQuestion(unittest.TestCase):



	def setUp(self):
		print('setUp')

		global a
		a = str(uuid.uuid4())
		self.question_1 = Question(a)
		self.question_1.constructor('How many siblings do you have?', 					#body
							[{'body':'None', 'iscorrect': 'false', 'pos': 'None' },		#choices
							{'body':'One', 'iscorrect': 'false', 'pos': 'None' },
							{'body':'Two', 'iscorrect': 'false', 'pos': 'None' },
							{'body':'Three', 'iscorrect': 'false', 'pos': 'None' },
							{'body':'Many', 'iscorrect': 'false', 'pos': 'None' }
							], 
							['personal'], 												#topics
							None, 														#parent
							["stopsign"])												#embeds

	def tearDown(self):
		print('tearDown\n')

	def test_constructor(self):
		print('test_constructor')

		self.assertEqual(self.question_1.q_id, a)
		self.assertEqual(self.question_1.body, 'How many siblings do you have?')
		self.assertEqual(self.question_1.choices, [{'body':'None', 'iscorrect': 'false', 'pos': 'None' },
							{'body':'One', 'iscorrect': 'false', 'pos': 'None' },
							{'body':'Two', 'iscorrect': 'false', 'pos': 'None' },
							{'body':'Three', 'iscorrect': 'false', 'pos': 'None' },
							{'body':'Many', 'iscorrect': 'false', 'pos': 'None' }
							] )
		self.assertEqual(self.question_1.topics, ['personal'])
		self.assertEqual(self.question_1.parent, None)
		self.assertEqual(self.question_1.embeds, ['stopsign'])
		self.assertEqual(self.question_1.ask_date, None)

	def test_getId(self):
		print('test_getId')

		self.assertEqual(self.question_1.getId(), a)


	def test_updateBody(self):
		print('test_updateBody')

		self.question_1.updateBody('Which one?')
		self.assertEqual(self.question_1.body, 'Which one?')


	def test_addTopic(self):
		print('test_addTopic')

		self.question_1.addTopic('siblings')
		self.assertEqual(self.question_1.topics, ['personal', 'siblings'])

	def test_delTopic(self):
		print('test_delTopic')

		self.question_1.delTopic('siblings')
		self.assertEqual(self.question_1.topics, ['personal'])

		self.question_1.delTopic('personal')
		self.assertEqual(self.question_1.topics, [])

	def test_addEmbed(self):
		print('test_addEmbed')

		self.question_1.addEmbed('cenglogo')
		self.assertEqual(self.question_1.embeds, ['stopsign', 'cenglogo'])


	def test_delEmbed(self):
		print('test_delEmbed')

		self.question_1.delEmbed('cenglogo')
		self.assertEqual(self.question_1.embeds, ['stopsign'])

		self.question_1.delEmbed('stopsign')
		self.assertEqual(self.question_1.embeds, [])


	def test_updateChoice(self):
		print('test_updateChoice')
		
		self.question_1.updateChoice(6, 'Four', 'true', 'START')
		self.assertEqual(self.question_1.choices, [{'body':'None', 'iscorrect': 'false', 'pos': 'None' },
							{'body':'One', 'iscorrect': 'false', 'pos': 'None' },
							{'body':'Two', 'iscorrect': 'false', 'pos': 'None' },
							{'body':'Three', 'iscorrect': 'false', 'pos': 'None' },
							{'body':'Many', 'iscorrect': 'false', 'pos': 'None' }
							])

		self.question_1.updateChoice(2, 'Four', 'true', 'START')
		self.assertEqual(self.question_1.choices, [{'body':'None', 'iscorrect': 'false', 'pos': 'None' },
							{'body':'One', 'iscorrect': 'false', 'pos': 'None' },
							{'body':'Four', 'iscorrect': 'true', 'pos': 'START' },
							{'body':'Three', 'iscorrect': 'false', 'pos': 'None' },
							{'body':'Many', 'iscorrect': 'false', 'pos': 'None' }
							])
		self.assertEqual(self.question_1.choices[2], {'body':'Four', 'iscorrect': 'true', 'pos': 'START' } )


	def test_updateParent(self):
		print('test_updateParent')

		self.question_1.updateParent('a22j31t')
		self.assertEqual(self.question_1.parent, 'a22j31t')

		self.question_1.updateParent(None)
		self.assertEqual(self.question_1.parent, None)

	def test_updateAskDate(self):
		print('test_updateAskDate')

		self.question_1.updateAskDate(datetime.date(2018, 12, 5))
		self.assertEqual(self.question_1.ask_date, datetime.date(2018, 12, 5))

		self.question_1.updateAskDate(None)
		self.assertEqual(self.question_1.ask_date, None)

	def test_save(self):
		print('test_save')

		self.question_1.save()
		res = questions.find({ "q_id" : a })
		
		self.assertEqual(self.question_1.q_id, res[0]["q_id"])
		self.assertEqual(self.question_1.body, res[0]["body"])
		self.assertEqual(self.question_1.choices, res[0]["choices"])
		self.assertEqual(self.question_1.embeds, res[0]["embeds"])
		self.assertEqual(self.question_1.ask_date, res[0]["ask_date"])
		self.assertEqual(self.question_1.topics, res[0]["topics"])
		self.assertEqual(self.question_1.parent, res[0]["parent"])

		questions.delete_one({'q_id': a})



	def test_copy(self):
		print('test_copy')

		newq = self.question_1.copy()
		self.assertEqual(self.question_1.body, newq.body)
		self.assertEqual(self.question_1.choices, newq.choices)
		self.assertEqual(self.question_1.topics, newq.topics)
		self.assertEqual(self.question_1.embeds, newq.embeds)
		self.assertEqual(newq.ask_date, None)
		self.assertEqual(self.question_1.q_id, newq.parent)
		self.assertNotEqual(self.question_1.q_id, newq.q_id)

		self.question_1.body = 'Which one?'
		self.question_1.topics = []
		self.question_1.updateAskDate(datetime.date(2018, 12, 5))
		self.assertNotEqual(self.question_1.body, newq.body)
		self.assertNotEqual(self.question_1.topics, newq.topics)
		self.assertNotEqual(self.question_1.ask_date, newq.ask_date)




	def test_getLatex(self):
		print('test_getLatex')

		test_string = self.question_1.getLatex(False)
		f = open("test_files/test_question_latex.txt", "w")
		f.write(test_string)
		f.close()

		self.assertEqual(filecmp.cmp('test_files/test_question_latex.txt', 'test_files/question_latex.txt'), True)

		f = open("test_files/test_question_latex.txt", "w")
		f.write("")
		f.close




if __name__ == '__main__':
	unittest.main()