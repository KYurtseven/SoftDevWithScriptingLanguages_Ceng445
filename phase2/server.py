from question import Question
from QBank import QBank
from exam import Exam
from socket import *
from threading import Thread
import struct
import json
import uuid
import sys
import pymongo

sys.path.insert(0, './qbank')
from qbank_getlatex import *

connection = pymongo.MongoClient("mongodb://localhost")
db = connection["latexdb"]
questions = db["T_QUESTIONS"]

#a = str(uuid.uuid4())

a = "cceeede0-a41b-41b3-8fb4-9add65ca59fa"

def questionHandler(data):
	'''
		Handles different question methods
	'''
	global a
	question = Question(a)
	body = data['data']

	if data['function'] == "constructor" :

		question.constructor(body['body'], body['choices'], body['topics'], body['parent'], body['embeds'])

	elif data['function'] == "updateBody":
		
		question.constructor(body['body'], body['choices'], body['topics'], body['parent'], body['embeds'])
		question.updateBody(data['newbody'])

	elif data['function'] == "addTopic":

		question.constructor(body['body'], body['choices'], body['topics'], body['parent'], body['embeds'])
		question.addTopic(data['newtopic'])

	elif data['function'] == "getid":

		question.constructor(body['body'], body['choices'], body['topics'], body['parent'], body['embeds'])
		res = question.getId()
		return res

	elif data['function'] == "deltopic":

		question.constructor(body['body'], body['choices'], body['topics'], body['parent'], body['embeds'])
		question.delTopic(data['topic'])

	elif data['function'] == "addembed":

		question.constructor(body['body'], body['choices'], body['topics'], body['parent'], body['embeds'])
		question.addEmbed(data['newembed'])

	elif data['function'] == "delembed":

		question.constructor(body['body'], body['choices'], body['topics'], body['parent'], body['embeds'])
		question.delEmbed(data['embed'])

	elif data['function'] == "updatechoice":

		question.constructor(body['body'], body['choices'], body['topics'], body['parent'], body['embeds'])
		question.updateChoice(data['c_id'],data['text'],data['iscorrect'],data['pos'])
		pass

	elif data['function'] == "updateparent":

		question.constructor(body['body'], body['choices'], body['topics'], body['parent'], body['embeds'])
		question.updateParent(data['newparent'])

	elif data['function'] == "updateaskdate":

		question.constructor(body['body'], body['choices'], body['topics'], body['parent'], body['embeds'])
		question.updateAskDate(data['newaskdate'])

	elif data['function'] == "getlatex":

		question.constructor(body['body'], body['choices'], body['topics'], body['parent'], body['embeds'])
		# shuffle the question
		res = question.getLatex(data['shuffle'])
		return res



	res = str(question)
	return res
	

def qbankHandler(data):
	'''
		Handles different qbank methods
	'''
	qbank = QBank()
	if data['function'] == "getquestion":
		res = qbank.getQuestion(data['q_id'])
		return str(res)

	elif data['function'] == "searchbytopic":
		res = qbank.searchByTopic(data['topic'])
		return str(res)

	elif data['function'] == "searchbyaskdate":
		res = qbank.searchByAskDate(data['start'],data['end'])
		return str(res)

	elif data['function'] == "getlatex":
		# find all questions from the database for simplicity
		mylist = []
		cursor = questions.find({})
		for ques in cursor:
			curques = Question(ques['q_id'])
			curques.constructor(ques['body'], ques['choices'], ques['topics'], ques['parent'], ques['embeds'])
			curques.updateAskDate(ques['ask_date'])

			mylist.append(curques)

		it = iter(mylist)

		res = qbank.getLatex(it, qbank_shuffle)
		return res
	elif data['function'] == "updateaskdate":
		mylist = []
		cursor = questions.find({})
		for ques in cursor:
			curques = Question(ques['q_id'])
			curques.constructor(ques['body'], ques['choices'], ques['topics'], ques['parent'], ques['embeds'])
			curques.updateAskDate(ques['ask_date'])

			mylist.append(curques)

		it = iter(mylist)
		qbank.updateAskDate(it, datetime.datetime.now())
		
		res = []
		for obj in mylist:
			res.append(str(obj))
		return str(res)


def examHandler(data):

	mylist = []
	cursor = questions.find({})
	for ques in cursor:
		curques = ques['q_id']
		mylist.append(curques)

	exam = Exam(mylist)

	if data['function'] == "getpdfexam" or data['function'] == "getpdfkey":
		exam.createShuffled(data['n'])
		exam.getPDFExam(data['no'])
		exam.getPDFKey(data['no'])
		return "ok"

	elif data['function'] == "createshuffled":
		exam.createShuffled(data['n'])
		s_e = exam.shuffled_exams
		res = []
		for obj in s_e:
			res.append(str(obj))
		return str(res)

	elif data['function'] == "getlatexexam":
		exam.createShuffled(data['n'])
		res = exam.getLatexExam(data['no'])
		return res

	elif data['function'] == "getlatexkey":
		exam.createShuffled(data['n'])
		res = exam.getLatexKey(data['no'])
		return res

	elif data['function'] == "getcsvkey":
		exam.createShuffled(data['n'])
		exam.getCSVKey()
		return "ok"

def read_blob(sock, size):
	'''
		reads data from given socket in size amounts
	'''
	buf = ""
	left = size

	while left:
		ret = sock.recv(left)

		if not ret:
			# Observed no data in the socket
			# Close the connection by declaring True
			return buf, True

		buf += ret
		left = left - len(ret)	

	return buf, False

def read_long(sock):
	'''
		calculates size of the bytes of the socket
		then reads the data
	'''
	size = struct.calcsize("L")
	
	data, flag = read_blob(sock, size)

	if flag:
		# we need to close the connection
		return -1

	return int(data)

def worker(sock):
	'''
		Takes a new socket
		Listen and serves commands of the client
	'''

	while True:

		# read the size of the data of socket
		datasize = read_long(sock)
		
		if datasize == -1:
			# Observed closed socket
			# close this end too
			break

		print "datasize", datasize

		sock.send("ack")

		# read data
		data, flag = read_blob(sock, datasize)
		# convert data to JSON object, dictionary
		data = json.loads(data)

		res = ""
		# Do some useful things with the data
		if(data['class'] == "question"):
			res = questionHandler(data)
		elif(data['class'] == "qbank"):
			res = qbankHandler(data)
		elif(data['class'] == "exam"):
			res = examHandler(data)
		else:
			print "What?"
			break
		# send the response back
		sock.send(res)
	sock.close()

def server(ip, args):
	'''
		listen connection
	'''
	port = int(args[1])
	s = socket(AF_INET, SOCK_STREAM)
	s.bind((ip, port))

	# listen at most 3 connection
	s.listen(3)
	try:
		while True:
			ns, peer = s.accept()
			t = Thread(target = worker, args = (ns, ))
			t.start()

			
			

	finally:
		s.close()

if __name__ == '__main__':
	server('127.0.0.1', sys.argv)