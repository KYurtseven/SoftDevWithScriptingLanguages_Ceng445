# Create your models here.
#from django.db import models
from djongo import models
import uuid
import copy
import random

# Create your models here.

class Choices(models.Model):
  c_id = models.IntegerField()
  body = models.CharField(max_length = 250)
  
  START = "START"
  END = "END"

  # TODO
  # Is NONE ok?
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
    return self.body

class Topics(models.Model):
  t_id = models.IntegerField()
  body = models.CharField(max_length = 50)
  class Meta:
    abstract = True

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
    for embed in self.embeds:
      if embed.e_id == int(e_id):
        self.embeds.remove(embed)
        break

  def delTopic(self, t_id):
    '''
    Deletes specific topic from object's topics list.
    If given topic is not found, do nothing.
    '''
    for topic in self.topics:
      if topic.t_id == int(t_id):
        self.topics.remove(topic)
        break

  def delChoice(self, c_id):
    for choice in self.choices:
      if choice.c_id == int(c_id):
        self.choices.remove(choice)
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
      l_body = "\\question {} \\newline\n".format(self.body)
      
      # create choices part
      l_choices = "\\begin{oneparchoices}"
      
      for choice in self.choices:
        l_choices += "\n \\choice {}".format(choice.body)
        l_choices += "\\newline"
      
      l_choices+= "\n\\end{oneparchoices}"

      return l_body + l_choices

    else:
      l_body = "\\question {} \\newline\n".format(self.body)
      st_arr = []		#choice with start position
      end_arr = []	#choice with end position
      na_arr = []		#choices without position
      
      for choice in self.choices:
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
