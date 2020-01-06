from djongo import models
import random

from question.models import Question
# Create your models here.

class Qbank(models.Model):

    # TODO
    # We dont need this
    questions = models.ArrayModelField(model_container = Question)

    def searchByTopic(self,topic):
        if len(topic) == 0:
            questions = Question.objects.all()
        else:
            questions = Question.objects.filter(topics = {'body' : topic})
        
        return questions

    def searchByAskDate(self,st,end):
        try:
            if(len(st) == 0 and len(end) == 0):
                return Question.objects.filter(ask_date__isnull = True) 

            elif(len(st) == 0 and len(end) != 0):
                cursor = Question.objects.filter(ask_date__lte = end)
                cursor_2 = Question.objects.filter(ask_date__isnull = True)
                result = []
                for x in cursor:
                    result.append(x)
                for y in cursor_2:
                    result.append(y)
                return result

            elif(len(st) != 0 and len(end) == 0):
                return Question.objects.filter(ask_date__gte = st)

            else:
                return Question.objects.filter(ask_date__range =[st,end])

        except Exception as e:
            print(e)

    def updateAskDate(self,iterator,date):            
        try:
            while True:
                i = next(iterator)
                i.updateAskDate(date)
                i.save()
        except Exception as e:
            print(e)

    def getLatex(self,iterator,shuffled):
        result = ""
        result += "\\documentclass{exam} \n"
        result += "\\usepackage{graphicx} \n"
        result += "\\begin{document} \n"
        result += "\\begin{questions}"
        if(shuffled == False):
            try:
                while True:
                    i = next(iterator)
                    result += str(i.getLatex(False))
                    result += "\n" 
                    result += "\\newline"
            except StopIteration:
                pass

        else:
            q_list = []
            try:
                while True:
                    i = next(iterator)
                    q_list.append(i)
            except StopIteration:
                pass

            #shuffle questions
            random.shuffle(q_list)
            q_iter = iter(q_list)
            try:
                while True:
                    i = next(q_iter)
                    result += str(i.getLatex(True))
                    result += "\n" 
                    result += "\\newline"
            except StopIteration:
                pass

        result += "\\end{questions}"
        result += "\\end{document}"

        return result


    class Meta:
        abstract = True

        