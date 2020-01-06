# Create your models here.
#from django.db import models
from djongo import models
from datetime import datetime
from question.models import Question
import random
import uuid
from threading import Lock,Thread,Condition,RLock,Semaphore
import subprocess
import os
from django.utils.encoding import smart_str
from django.conf import settings
from django.http import HttpResponse
from mimetypes import guess_type

import shutil




class QuestionId(models.Model):
    q_id = models.CharField(max_length = 50)
    class Meta:
        abstract = True
    def __str__(self):
        return self.q_id

class shuffledExams(models.Model):
    book_name = models.CharField(max_length = 1)
    exam = models.ArrayModelField(model_container = Question)
    class Meta:
        abstract = True
    def __str__(self):
        return self.book_name + "\n" +self.exam


class Exam(models.Model):
    e_id = models.CharField(max_length = 50)
    exam_name = models.CharField(max_length = 100)
    exam_date = models.DateField(blank = True)
    question_list = models.ArrayModelField(model_container = QuestionId)
    shuffled_exams = models.ArrayModelField(model_container = shuffledExams)

    class Meta:
        verbose_name_plural = "Exams"

    def __str__(self):
        return self.e_id
    
    def createExam(self, request):
        
        self.e_id = str(uuid.uuid4())
        self.exam_name = request.POST['name']
        if len(request.POST['date']) != 0:
            self.exam_date = request.POST['date']
        else:
            self.exam_date = None
        self.shuffled_exams = []
        self.question_list = []

    def editExamName(self, newname):

        self.exam_name = newname
    
    def updateAskDate(self, givendate):
        if len(givendate) != 0:
            self.exam_date = givendate

    def createShuffled(self, n):
        path = os.getcwd()
        exam_dir = path + "/exams/{}".format(self.e_id)
        if os.path.exists(exam_dir):
            shutil.rmtree(exam_dir, ignore_errors=True)

        shuffled_exams = []
        book_name = "A"

        for i in range(n):
            shuffled_questions  = random.sample(self.question_list, len(self.question_list))
            shuffled_questions_temp = []

            for question in shuffled_questions:
                temp_question = Question.objects.get(q_id = question.q_id)
                temp_question.shuffleQuestion()
                shuffled_questions_temp.append(temp_question)

            shuffled_exam = shuffledExams()
            shuffled_exam.book_name = book_name
            shuffled_exam.exam = shuffled_questions_temp
            shuffled_exams.append(shuffled_exam)

            book_name = str(chr(ord(book_name)+1))
            
        self.shuffled_exams = shuffled_exams

    def getLatexExam(self, no):

        s_e = self.shuffled_exams[no]
        s_iter = iter(s_e.exam)

        result = ""
        result += "\\documentclass{exam} \n"
        result += "\\usepackage{graphicx} \n"
        result += "\\begin{document} \n"
        result += "\\newcommand\\examtypemarker{}{\\centerline{\\framebox{\\Huge " + str(s_e.book_name) + "}} \n"
        result += "\\begin{center} \n"
        result += "\\Large\\textbf{"+ self.exam_name +"}\n"
        result += "\\end{center} \n"
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

        return result
        # path = os.getcwd()
        # exam_dir = path + "/exams/{}".format(self.e_id)
        # if not os.path.exists(exam_dir):
        #     os.mkdir(exam_dir)



        # tex_dir = path + "/exams/{}/tex".format(self.e_id)
        # if not os.path.exists(tex_dir):
        #     os.mkdir(tex_dir)

        # f = open(tex_dir + "/exam_" + self.shuffled_exams[no].book_name +".tex", "w")
        # f.write(result)
        # f.close()

        # return self.downloadFile(tex_dir, '/exam_' + self.shuffled_exams[no].book_name +'.tex')

    def getPDFExam(self,no):

        #create exam directory
        path = os.getcwd()
        exam_dir = path + "/exams/{}".format(self.e_id)
        if not os.path.exists(exam_dir):
            os.mkdir(exam_dir)


        #crete latex directory
        tex_dir = path + "/exams/{}/tex".format(self.e_id)
        if not os.path.exists(tex_dir):
            os.mkdir(tex_dir)

        #write tex file
        latex_exam = self.getLatexExam(no)
        f = open(tex_dir + "/exam_" + self.shuffled_exams[no].book_name +".tex", "w")
        f.write(latex_exam)
        f.close()

        #create pdf directory
        #crete latex directory
        pdf_dir = path + "/exams/{}/pdf".format(self.e_id)
        if not os.path.exists(pdf_dir):
            os.mkdir(pdf_dir)

        #write pdf file
        e_name = tex_dir + '/exam_' + self.shuffled_exams[no].book_name +'.tex'
        subprocess.call(['pdflatex', '-output-directory', pdf_dir , e_name], shell = False)

        #delete log and aux
        os.unlink(pdf_dir +"/exam_" + self.shuffled_exams[no].book_name +".log")
        os.unlink(pdf_dir +"/exam_" + self.shuffled_exams[no].book_name +".aux")

        return self.downloadFile(pdf_dir, '/exam_' + self.shuffled_exams[no].book_name +'.pdf')

    def getLatexKey(self,no):
        s_e = self.shuffled_exams[no]
        s_iter = iter(s_e.exam)

        result = ""
        result += "\\documentclass[answers]{exam} \n"
        result += "\\usepackage{graphicx} \n"
        result += "\\begin{document} \n"
        result += "\\newcommand\\examtypemarker{}{\\centerline{\\framebox{\\Huge " + str(s_e.book_name) + "}}"
        result += "\\begin{center} \n"
        result += "\\Large\\textbf{"+ self.exam_name +" - Answer Key}\n"
        result += "\\end{center} \n"
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

        return result

        # path = os.getcwd()
        # exam_dir = path + "/exams/{}".format(self.e_id)
        # if not os.path.exists(exam_dir):
        #     os.mkdir(exam_dir)


        # tex_key_dir = path + "/exams/{}/tex_key".format(self.e_id)
        # if not os.path.exists(tex_key_dir):
        #     os.mkdir(tex_key_dir)

        # f = open(tex_key_dir + "/exam_key_" + self.shuffled_exams[no].book_name +".tex", "w")
        # f.write(result)
        # f.close()

        # return self.downloadFile(tex_key_dir, '/exam_key_' + self.shuffled_exams[no].book_name + '.tex')


    def getPDFKey(self,no):
        
        #create exam directory
        path = os.getcwd()
        exam_dir = path + "/exams/{}".format(self.e_id)
        if not os.path.exists(exam_dir):
            os.mkdir(exam_dir)


        #crete latex directory
        tex_key_dir = path + "/exams/{}/tex_key".format(self.e_id)
        if not os.path.exists(tex_key_dir):
            os.mkdir(tex_key_dir)

        #write tex file
        latex_exam_key = self.getLatexKey(no)
        f = open(tex_key_dir + "/exam_key_" + self.shuffled_exams[no].book_name +".tex", "w")
        f.write(latex_exam_key)
        f.close()

        #create pdf directory
        pdf_key_dir = path + "/exams/{}/pdf_key".format(self.e_id)
        if not os.path.exists(pdf_key_dir):
            os.mkdir(pdf_key_dir)

        #write pdf file
        e_key_name = tex_key_dir + '/exam_key_' + self.shuffled_exams[no].book_name +'.tex'
        subprocess.call(['pdflatex', '-output-directory', pdf_key_dir , e_key_name], shell = False)

        #delete log and aux
        os.unlink(pdf_key_dir +"/exam_key_" + self.shuffled_exams[no].book_name +".log")
        os.unlink(pdf_key_dir +"/exam_key_" + self.shuffled_exams[no].book_name +".aux")

        return self.downloadFile(pdf_key_dir, '/exam_key_' + self.shuffled_exams[no].book_name + '.pdf')

    def getCSVKey(self):
        choice_mark = "A"

        path = os.getcwd()
        exam_dir = path + "/exams/{}".format(self.e_id)
        if not os.path.exists(exam_dir):
            os.mkdir(exam_dir)

        csv_dir = path + "/exams/{}/csv_key".format(self.e_id)
        if not os.path.exists(csv_dir):
            os.mkdir(csv_dir)

        f=open(csv_dir + "/answer_key.csv","w")
        f.write('no,question_no,answer\n')
        for exam in self.shuffled_exams:
            for question in exam.exam:
                f.write(exam.book_name+',')
                question_number = str(exam.exam.index(question)+1)
                f.write(question_number+',')
                index = 0
                for choice in question.choices:
                    if(choice.iscorrect == True):
                        true_choice = chr(ord('a') + index )
                        f.write(true_choice)
                    index += 1
                f.write('\n')               

        f.close()

        return self.downloadFile(csv_dir, "/answer_key.csv")

    def downloadFile(self, path, file_name):

        file_path=os.path.join(path + file_name)
        print(file_path)
        with open(file_path, 'rb') as f:
            response = HttpResponse(f, content_type=guess_type(file_path)[0])
            response['Content-Length'] = len(response.content)
            return response