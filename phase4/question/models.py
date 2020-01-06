# Create your models here.
#from django.db import models
from djongo import models
import uuid
import copy
import random
import subprocess
import os
from django.http import HttpResponse
from mimetypes import guess_type
import time
# Create your models here.

class Choices(models.Model):
  c_id = models.IntegerField()
  body = models.CharField(max_length = 250)
  
  START = "START"
  END = "END"
  NONE = "None"
  
  position_choices = (
    (START, "START"),
    (END, "END"),
    (NONE, "NONE")
  )

  pos = models.CharField(
    max_length = 5,
    choices = position_choices,
    default = NONE,
  )
  
  iscorrect = models.BooleanField(default = False)

  class Meta:
    abstract = True
  def __str__(self):
    return "choice\n" + "body: " + self.body + \
      " c_id " + str(self.c_id) + " pos " + str(self.pos) + " iscorrect " + str(self.iscorrect)

class Topics(models.Model):
  t_id = models.IntegerField()
  body = models.CharField(max_length = 50)
  class Meta:
    abstract = True
  def __str__(self):
    return "topic\n" + "body: " + self.body + " t_id " + str(self.t_id)
class Embeds(models.Model):
  e_id = models.IntegerField(blank = True)
  body = models.CharField(max_length = 50, blank = True)
  class Meta:
    abstract = True

class Question(models.Model):
  q_id = models.CharField(max_length = 50)
  body = models.TextField()
  choices = models.ArrayModelField(model_container = Choices)
  topics = models.ArrayModelField(model_container = Topics)
  embeds = models.ArrayModelField(model_container = Embeds)
  parent = models.CharField(max_length = 50, blank = True)
  ask_date = models.DateField(blank = True)

  class Meta:
    verbose_name_plural = "Questions"

  def __str__(self):
    return self.body

  def addQuestion(self, request):
    self.choices = []
    self.topics = []
    self.embeds = []

    choice = Choices()
    embed = Embeds()
    topic = Topics()

    # add choice
    if len(request.POST['choice_body']) != 0:
      choice.c_id = 0
      choice.body = request.POST['choice_body']
      
      # add position
      pos = request.POST['choice_position']
      if len(pos) != 0:
        if(pos.upper() == "END"):
          choice.pos = "END"
        elif(pos.upper() == "START"):
          choice.pos = "START"
        else:
          choice.pos = "NONE"
      else:
        choice.pos = "NONE"

      # add correct
      correct = request.POST['choice_correct']
      if len(correct) != 0:
        if(correct.upper() == "TRUE"):
          choice.iscorrect = True
        else:
          choice.iscorrect = False
      else:
        choice.iscorrect = False

      self.choices.append(choice)

    # add topic
    top = request.POST['topic']
    if len(top) != 0:
      topic.t_id = 0
      topic.body = top
    
      self.topics.append(topic)
    
    # add embed
    emb = request.POST['embed']
    if len(emb) != 0:
      embed.e_id = 0
      embed.body = emb
    
      self.embeds.append(embed)
    
    self.q_id = str(uuid.uuid4())
    self.body = request.POST['body'] 
    self.ask_date = None
    self.parent = None

    self.createDirectory()

  def constructor(self, body, choices, topics, parent, embeds):
    '''
    Constructor:
    Gets body, choices, topics, parent, embeds as input.
    Sets ask_date as None.
    '''
    
    self.q_id = str(uuid.uuid4())
    self.body = body
    self.choices = choices
    self.topics = topics
    self.parent = parent 
    self.embeds = embeds
    self.ask_date = None

  def updateParent(self, p_id):
    self.parent = p_id
    
  def updateAskDate(self, givenDate):
    '''
      Update ask date.
      Date is input. 
    '''
    if len(givenDate) != 0:
      self.ask_date = givenDate
    
  def addEmbed(self, body):
    '''
      Add embed to embeds array of object.
    '''
    newEmbed = Embeds()
    
    max = 0
    for embed in self.embeds:
      if(embed.e_id > max):
        max = embed.e_id
    max += 1

    newEmbed.e_id = max
    
    newEmbed.body = body
    self.embeds.append(newEmbed)
    return newEmbed

  def addTopic(self, text):
    '''
    Add topic to topics list of object.
    '''
    newTopic = Topics()

    max = 0
    for topic in self.topics:
      if(topic.t_id > max):
        max = topic.t_id
    max += 1

    newTopic.t_id = max
    newTopic.body = text
    self.topics.append(newTopic)
    return newTopic

  def addChoice(self, latextext, correct, pos):

    newChoice = Choices()
    
    max = 0

    for choice in self.choices:
      if(choice.c_id > max):
        max = choice.c_id
    max += 1

    newChoice.c_id = max
    
    if(pos.upper() == "END"):
      newChoice.pos = "END"
    elif(pos.upper() == "START"):
      newChoice.pos = "START"
    else:
      newChoice.pos = "NONE"
      
    newChoice.body = latextext
    
    if(correct.upper() == "TRUE"):
      newChoice.iscorrect = True
    else:
      newChoice.iscorrect = False
    
    self.choices.append(newChoice)
    return newChoice

  def updateBody(self, latextext):
    '''
    Update body of object with given text as input.
    '''
    self.body = latextext

  def updateEmbed(self, e_id, body):

    for embed in self.embeds:
      if embed.e_id == int(e_id):
        embed.body = body
        break

  def updateTopic(self, t_id, body):

    for topic in self.topics:
      if topic.t_id == int(t_id):
        topic.body = body
        break

  def updateChoice(self, c_id, latextext, correct, pos):
    '''
    update a choice
    set the correctness of the choice
    set the pos of the choice, i.e. START, END or NA
    while shuffling pos info will be used
    '''

    for choice in self.choices:
      # find the choice
      if choice.c_id == int(c_id):
        # update choice with given parameters

        if(len(latextext) != 0):
          choice.body = latextext
        
        if len(pos) != 0:
          if(pos.upper() == "END"):
            choice.pos = "END"
          elif(pos.upper() == "START"):
            choice.pos = "START"
          else:
            choice.pos = "NONE"
        
        if len(correct) != 0:
          if(correct.upper() == "TRUE"):
            choice.iscorrect = True
          else:
            choice.iscorrect = False

  def delEmbed(self, e_id):
    '''
    delete an embed
    try except block for possible empty embed array
    '''
    for i in range(len(self.embeds)):
      if(self.embeds[i].e_id == int(e_id)):
        self.embeds.pop(i)
        break

  def delTopic(self, t_id):
    '''
    Deletes specific topic from object's topics list.
    If given topic is not found, do nothing.
    '''
    for i in range(len(self.topics)):
      if(self.topics[i].t_id == int(t_id)):
        self.topics.pop(i)
        break

  def delChoice(self, c_id):
    for i in range(len(self.choices)):
      if self.choices[i].c_id == int(c_id):
        self.choices.pop(i)
        break

  def copyQuestion(self):
    '''
    returns deep copy of the object
    '''
    newq = Question()
    newq.q_id = str(uuid.uuid4())
    newq.body = self.body
    newq.choices = self.choices
    newq.topics = self.topics
    newq.embeds = self.embeds
    newq.parent = self.q_id
    newq.ask_date = None

    newq.createDirectory()

    return newq

  def shuffleQuestion(self):
    st_arr = [] 	#question with start position
    end_arr = []	#question with end position
    na_arr = []		#questions without position
    c = self.choices
    shuffled_choices = []
    for x in c:
      if x.pos == "START":
        st_arr.append(x)
      elif x.pos == "END":
          end_arr.append(x)
      else:
        na_arr.append(x)

    random.shuffle(na_arr)
    if(st_arr != []):
      shuffled_choices.append(st_arr[0])

    for ques in na_arr:
      shuffled_choices.append(ques)

    if(end_arr != []):
      shuffled_choices.append(end_arr[0])

    self.choices = shuffled_choices

    return

  def getLatexWithKey(self):
    if self.body.find("--EMBEDSTART--") is not -1:
      index = self.body.find("--EMBEDSTART--")
      endindex = self.body.find("--EMBEDEND--")

      newbody = self.body[index + 14:endindex]
      
      e = "\includegraphics[width=0.2\linewidth]{questions/" +self.q_id + "/tex/" + newbody + ".jpg}"
      self.body =self.body[:index] + e + self.body[endindex + 12:]

    l_body = "\\question {} \\newline\n".format(self.body)
		
		# create choices part
    c = self.choices
    l_choices = "\\begin{oneparchoices}"
    c_arr = []

    for x in c:
      c_arr.append(x)

        
    for i in c_arr:
      if(i.iscorrect==True):
        l_choices += "\n \\correctchoice {}".format(i.body)
      else:
        l_choices += "\n \\choice {}".format(i.body)
      l_choices += "\\newline"
    
    l_choices+= "\n\\end{oneparchoices}"

    return l_body + l_choices


  def getLatex(self, shuffled):
    '''
    Get latex version of a question
    '''

    if(shuffled == False):
      
      if self.body.find("--EMBEDSTART--") is not -1:
        index = self.body.find("--EMBEDSTART--")
        endindex = self.body.find("--EMBEDEND--")

        newbody = self.body[index + 14:endindex]
        
        e = "\includegraphics[width=0.2\linewidth]{questions/" +self.q_id + "/tex/" + newbody + ".jpg}"
        self.body =self.body[:index] + e + self.body[endindex + 12:]

      l_body = "\\question {} \\newline\n".format(self.body)
      
      # create choices part
      l_choices = "\\begin{oneparchoices}"
      st_arr = []		#choice with start position
      end_arr = []	#choice with end position
      na_arr = []		#choices without position
      
      for choice in self.choices:
        if "--EMBED--" in choice.body:
          newbody = choice.body[9:]
          choice.body = "\includegraphics[width=0.2\linewidth]{questions/" +self.q_id + "/tex/" + newbody + ".jpg}"
        if choice.pos == "START":
          st_arr.append(choice)
        elif choice.pos == "END":
          end_arr.append(choice)
        else:
          na_arr.append(choice)

      if(st_arr != []):
        l_choices += "\n \\choice {}".format(st_arr[0].body)
        l_choices += "\\newline"
      
      for i in na_arr:
        l_choices += "\n \\choice {}".format(i.body)
        l_choices += "\\newline"

      if(end_arr != []):
        l_choices += "\n \\choice {}".format(end_arr[0].body)
        l_choices += "\\newline"
      
      l_choices+= "\n\\end{oneparchoices}"

      return l_body + l_choices

    else:
      if self.body.find("--EMBEDSTART--") is not -1:
        index = self.body.find("--EMBEDSTART--")
        endindex = self.body.find("--EMBEDEND--")

        newbody = self.body[index + 14:endindex]
        
        e = "\includegraphics[width=0.2\linewidth]{questions/" +self.q_id + "/tex/" + newbody + ".jpg}"
        self.body =self.body[:index] + e + self.body[endindex + 12:]


      l_body = "\\question {} \\newline\n".format(self.body)
      st_arr = []		#choice with start position
      end_arr = []	#choice with end position
      na_arr = []		#choices without position
      
      for choice in self.choices:
        if "--EMBED--" in choice.body:
          newbody = choice.body[9:]
          choice.body = "\includegraphics[width=0.2\linewidth]{questions/" +self.q_id + "/tex/" + newbody + ".jpg}"

        if choice.pos == "START":
          st_arr.append(choice)
        elif choice.pos == "END":
          end_arr.append(choice)
        else:
          na_arr.append(choice)

      random.shuffle(na_arr) #choices without position are shuffled here

      l_choices = "\\begin{oneparchoices}"
      #if there is a choice with start position
      if(st_arr != []):
        l_choices += "\n \\choice {}".format(st_arr[0].body)
        l_choices += "\\newline"

      for i in na_arr:
        l_choices += "\n \\choice {}".format(i.body)
        l_choices += "\\newline"
      
      #if there is a choice with end position
      if(end_arr != []):
        l_choices += "\n \\choice {}".format(end_arr[0].body)
        l_choices += "\\newline"

      l_choices+= "\n\\end{oneparchoices}"

      return l_body + l_choices

  def createDirectory(self):
    path = os.getcwd()
    question_dir = path + "/questions/{}".format(self.q_id)
    if not os.path.exists(question_dir):
      os.mkdir(question_dir)


    #crete latex directory
    tex_dir = path + "/questions/{}/tex".format(self.q_id)
    if not os.path.exists(tex_dir):
      os.mkdir(tex_dir)

    pdf_dir = path + "/questions/{}/pdf".format(self.q_id)
    if not os.path.exists(pdf_dir):
      os.mkdir(pdf_dir)

    return tex_dir,pdf_dir

  def getPDF(self):

    tex_dir, pdf_dir = self.createDirectory()
    
    result = ""
    result += "\\documentclass{exam} \n"
    result += "\\usepackage{graphicx} \n"
    result += "\\begin{document} \n"
    result += "\\begin{center} \n"
    result += "\\Large\\textbf{"+ self.q_id +"}\n"
    result += "\\end{center} \n"
    result += "\\begin{questions}"

    # add choices
    result += self.getLatex(False)
    
    # add topics
    result += "\\newline"
    result += "\n Topics: \n"
    for i in range(len(self.topics)):
      result += self.topics[i].body + ", "

    # add embeds
    result += "\\newline"
    result += "\n Embeds: \n"
    for i in range(len(self.embeds)):
      result += self.embeds[i].body + ", "

    # add ask_date
    result += "\\newline"
    result += "\n Askdate: " + str(self.ask_date)

    # add parent
    result += "\\newline"
    try:
      result += "\n Parent: " + self.parent
    except:
      result += ""

    result += "\\end{questions}"
    result += "\\end{document}"

    f = open(tex_dir + "/question_" + self.q_id +".tex", "w")
    f.write(result)
    f.close()


    #write pdf file
    q_name = tex_dir + '/question_' + self.q_id +'.tex'
    subprocess.call(['pdflatex', '-output-directory', pdf_dir , q_name], shell = False)

    #delete log and aux
    os.unlink(pdf_dir +"/question_" + self.q_id +".log")
    os.unlink(pdf_dir +"/question_" + self.q_id +".aux")

    return self.convertpdf2image()

  def convertpdf2image(self):
    #time.sleep(1)
    pathpdf = os.getcwd()
    
    pathimage = pathpdf + '/image.png'

    
    pathpdf = pathpdf + "/questions/" + self.q_id + "/pdf/question_" + self.q_id + ".pdf"
    script = ["python", "pdfconverter.py", pathpdf, pathimage]    
    subprocess.call(script, shell = False)

    return pathimage
