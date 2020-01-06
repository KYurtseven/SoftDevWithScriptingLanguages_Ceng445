from socket import *
from threading import Thread
from exam import Exam
import struct
import json
import sys
import subprocess
import os
import time

sys.path.insert(0, './question')
sys.path.insert(0, './qbank')

# For test purposes
from question_constructor import * 
from question_updatebody import *
from question_addtopic import *
from question_deltopic import *
from question_addembed import *
from question_delembed import *
from question_updatechoice import *
from question_updateaskdate import *
from question_updateparent import *
from question_getlatex import *
from qbank_getquestion import *
from qbank_searchbytopic import *
from qbank_searchbyaskdate import *
from qbank_getlatex import *


# server ip's
SERVER_IP = '127.0.0.1'

def make8_byte(s):

	size = len(str(s))

	s2 = ""
	for i in range(8-size):
		s2 += "0"

	s2 += str(s)

	return s2

def createQuestionRequest(reqsub):
	'''
	'''
	req = {}

	req['class'] = "question"
	req['data'] = {}
	# read from question_constructor.py
	req['data'] = question_constructor

	if reqsub == "constructor":
		req['function'] = "constructor"
		
	elif reqsub == "updateBody":
		req['function'] = "updateBody"
		req['newbody'] = question_updatebody

	elif reqsub == "addTopic":
		req['function'] = "addTopic"
		req['newtopic'] = question_addtopic

	elif reqsub == "getid":
		req['function'] = "getid"

	elif reqsub == "deltopic":
		req['function'] = "deltopic"
		req['topic'] = question_deltopic

	elif reqsub == "addembed":
		req['function'] = "addembed"
		req['newembed'] = question_addembed

	elif reqsub == "delembed":
		req['function'] = "delembed"
		req['embed'] = question_delembed

	elif reqsub == "updatechoice":
		req['function'] = "updatechoice"
		req['c_id'] = question_c_id
		req['text'] = question_text
		req['iscorrect'] = question_iscorrect
		req['pos'] = question_pos

	elif reqsub == "updateparent":
		req['function'] = "updateparent"
		req['newparent'] = question_updateparent

	elif reqsub == "updateaskdate":
		req['function'] = "updateaskdate"
		req['newaskdate'] = question_updateaskdate

	elif reqsub == "getlatex":
		req['function'] = "getlatex"
		req['shuffle'] = question_getlatex

	return req

def createExamRequest(reqsub):
	
	req = {}

	req['class'] = "exam"
	req['data'] = {}

	if reqsub == "getpdfexam":
		req['function'] = "getpdfexam"
		req['n'] = 2
		req['no'] = 0

	elif reqsub == "getlatexexam":
		req['function'] = "getlatexexam"
		req['n'] = 2
		req['no'] = 0

	elif reqsub == "createshuffled":
		req['function'] = "createshuffled"
		req['n'] = 2

	elif reqsub == "getlatexkey":
		req['function'] = "getlatexkey"
		req['n'] = 2
		req['no'] = 0

	elif reqsub == "getpdfkey":
		req['function'] = "getpdfkey"
		req['n'] = 2
		req['no'] = 0

	elif reqsub == "getcsvkey":
		req['function'] = "getcsvkey"
		req['n'] = 2

	return req

def createQbankRequest(reqsub):
	
	req = {}

	req['class'] = "qbank"
	req['data'] = {}

	if reqsub == "getquestion":
		req['function'] = "getquestion"
		req['q_id'] = qbank_getquestion

	elif reqsub == "searchbytopic":
		req['function'] = "searchbytopic"
		req['topic'] = qbank_searchbytopic

	elif reqsub == "searchbyaskdate":
		req['function'] = "searchbyaskdate"
		req['start'] = qbank_start
		req['end'] = qbank_end

	elif reqsub == "getlatex":
		req['function'] = "getlatex"
	elif reqsub == "updateaskdate":
		req['function'] = "updateaskdate"


	return req


def client(args):

	SERVER_PORT = int(args[1])
	sock = int(args[2])

	s = socket(AF_INET, SOCK_STREAM)
	s.bind(('127.0.0.1', sock))
	# connect to the server
	s.connect((SERVER_IP, SERVER_PORT))


	while True:

		try:
			req_header = raw_input("header -> ")
		except Exception as e:
			# EOF error
			break

		if req_header == "quit" or req_header == None:
			break
		
		reqsub = raw_input("sub -> ")
		req_body = ""

		if req_header == "question":
			req_body = createQuestionRequest(reqsub)
		elif req_header == "qbank":
			req_body = createQbankRequest(reqsub)
		else:
			req_body = createExamRequest(reqsub)

		# data to be sent
		senddata = json.dumps(req_body)

		# correctly pad size to 8 bytes for measuring it in server
		size = make8_byte(len(senddata))

		# first send size
		s.send(str(size))

		ackres, add = s.recvfrom(3)

		if ackres == "ack":
			s.send(senddata)

		res, add = s.recvfrom(4096)

		if res == "ok" and req_header == "exam":
			if req_body['function'] == "getpdfexam":
				p = subprocess.Popen(['evince', 'exam.pdf'])
				p.wait()

			elif req_body['function'] == "getpdfkey":
				p = subprocess.Popen(['evince', 'exam_key.pdf'])
				p.wait()

		if res == "ok" and req_header == "exam":
			if req_body['function'] == "getcsvkey":
				p = subprocess.Popen(['gedit', 'answer_key.csv'])
				p.wait()


		print "received\n", res
	# close the socket
	s.close()

if __name__ == '__main__':
	# argv[0] = client.py
	# argv[1] = port
	client(sys.argv)
