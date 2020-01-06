import unittest
import uuid
import datetime
import pymongo
import filecmp
import json

from socket import *
from threading import Thread
import struct
import sys
import subprocess
import os
import time

from question import Question
from QBank import QBank
from exam import Exam

connection = pymongo.MongoClient("mongodb://localhost")
db = connection["latexdb"]
questions = db["T_QUESTIONS"]
exams = db["T_EXAMS"]

class TestExam(unittest.TestCase):

	def setUp(self):
		print('setUp\n')

	def tearDown(self):
		print('tearDown\n')

	def test_questionClient(self):
		print('questionClient\n')
		port = 8000
		p1 = subprocess.Popen(['python', 'client.py', '3010', str(port + 1)], stdin = subprocess.PIPE, stdout= subprocess.PIPE)
		p2 = subprocess.Popen(['python', 'client.py', '3010', str(port + 2)], stdin = subprocess.PIPE, stdout= subprocess.PIPE)
		#p1.wait()

		p1.stdin.write("question\n")
		p1.stdin.write("deltopic\n")
		p1.stdin.close()

		p2.stdin.write("question\n")
		p2.stdin.write("getlatex\n")
		p2.stdin.close()

		a = p1.stdout.read()
		b = p2.stdout.read()
		
		print a
		print b

	def test_qbankClient(self):
		print('qbankClient\n')
		port = 9000
		p1 = subprocess.Popen(['python', 'client.py', '3010', str(port + 1)], stdin = subprocess.PIPE, stdout= subprocess.PIPE)
		p2 = subprocess.Popen(['python', 'client.py', '3010', str(port + 2)], stdin = subprocess.PIPE, stdout= subprocess.PIPE)

		p1.stdin.write("qbank\n")
		p1.stdin.write("searchbytopic\n")
		p1.stdin.close()

		p2.stdin.write("qbank\n")
		p2.stdin.write("getlatex\n")
		p2.stdin.close()

		a = p1.stdout.read()
		b = p2.stdout.read()
		
		print a
		print b



	def test_examClient(self):
		print('examClient\n')
		port = 10000
		p1 = subprocess.Popen(['python', 'client.py', '3010', str(port + 1)], stdin = subprocess.PIPE, stdout= subprocess.PIPE)
		p2 = subprocess.Popen(['python', 'client.py', '3010', str(port + 2)], stdin = subprocess.PIPE, stdout= subprocess.PIPE)

		p1.stdin.write("exam\n")
		p1.stdin.write("getpdfexam\n")
		p1.stdin.close()

		p2.stdin.write("exam\n")
		p2.stdin.write("getcsvkey\n")
		p2.stdin.close()

		a = p1.stdout.read()
		b = p2.stdout.read()
		
		print a
		print b






if __name__ == '__main__':
	unittest.main()