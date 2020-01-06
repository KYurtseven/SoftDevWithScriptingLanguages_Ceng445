from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Question
from cgi import parse_qs, escape
import urllib.request 
import json
import time
#from pdf2image import convert_from_path, convert_from_bytes

# Function: success(obj,name)
# Return a successfull result in JSON httpresponse
def success(obj, name):
	return HttpResponse(json.dumps({'result':'Success',name : obj}),
				'text/json')

# Function: error(reason)
# Return a successfull result in JSON
def error(reason):
	return HttpResponse(json.dumps({'result':'Fail','reason' : reason}),
				'text/json')

def serializequestion(q):

    q_json = {}
    q_json['q_id'] = q.q_id
    q_json['body'] = q.body
    
    q_json['topics'] = []
    for i in range(len(q.topics)):
        topic = {}
        topic['body'] = q.topics[i].body
        topic['t_id'] = q.topics[i].t_id
        q_json['topics'].append(topic)

    q_json['embeds'] = []
    for i in range(len(q.embeds)):
        embed = {}
        embed['body'] = q.embeds[i].body
        embed['e_id'] = q.embeds[i].e_id
        q_json['embeds'].append(embed)
    
    q_json['choices'] = []
    for i in range(len(q.choices)):
        choice = {}
        choice['body'] = q.choices[i].body
        choice['c_id'] = q.choices[i].c_id
        choice['pos'] = q.choices[i].pos
        choice['iscorrect'] = q.choices[i].iscorrect
        q_json['choices'].append(choice)

    q_json['ask_date'] = str(q.ask_date)
    q_json['parent'] = q.parent
    return q_json

def serializetopic(q):
    t_json = {}
    
    t_json['topics'] = []
    for i in range(len(q.topics)):
        topic = {}
        topic['body'] = q.topics[i].body
        topic['t_id'] = q.topics[i].t_id
        t_json['topics'].append(topic)

    return t_json

def serializeembed(q):
    e_json = {}
    
    e_json['embeds'] = []
    for i in range(len(q.embeds)):
        embed = {}
        embed['body'] = q.embeds[i].body
        embed['e_id'] = q.embeds[i].e_id
        
        e_json['embeds'].append(embed)

    return e_json

def serializechoice(q):
    c_json = {}
    
    c_json['choices'] = []
    for i in range(len(q.choices)):
        choice = {}
        choice['body'] = q.choices[i].body
        choice['c_id'] = q.choices[i].c_id
        choice['pos'] = q.choices[i].pos
        choice['iscorrect'] = q.choices[i].iscorrect
        
        c_json['choices'].append(choice)

    return c_json


def getquestion(request):
    q_id = parse_qs(request.environ['QUERY_STRING'])['q_id'][0]
    q = Question.objects.get(q_id = q_id)
    q_json = serializequestion(q)
    return success(q_json, 'question')

def updbody(request):
    try:
        m = Question.objects.get(q_id = request.POST['q_id'])
        m.updateBody(request.POST['body'])
        m.save()
        return success('Question updated','message')
    except Exception as e:
        print("exception: " + str(e))
        return error('Invalid form data')

def upddate(request):
    try:
        m = Question.objects.get(q_id = request.POST['q_id'])
        # It does not update the date, if it is null!
        m.updateAskDate(request.POST['ask_date'])
        m.save()
        return success('Question updated','message')
    except Exception as e:
        print("exception: " + str(e))
        return error('Invalid form data')

def updparent(request):
    try:
        m = Question.objects.get(q_id = request.POST['q_id'])
        m.updateParent(request.POST['parent'])
        m.save()
        return success('Question updated','message')
    except Exception as e:
        print("exception: " + str(e))
        return error('Invalid form data')
	
def updtopic(request):
    try:
        m = Question.objects.get(q_id = request.POST['q_id'])
        m.updateTopic(request.POST['t_id'], request.POST['body'])
        m.save()
        return success('Question updated','message')
    except Exception as e:
        print("exception: " + str(e))
        return error('Invalid form data')

def addtopic(request):
    try:
        q = Question.objects.get(q_id = request.POST['q_id'])
        topic = q.addTopic(request.POST['body'])
        q.save()
        return success({'id': topic.t_id, 'message': 'Topic added'}, 'success')
    except Exception as e:
        print("exception: " + str(e))
        return error('Invalid form data')

def topiclist(request):
    q_id = parse_qs(request.environ['QUERY_STRING'])['q_id'][0]
    q = Question.objects.get(q_id = q_id)
    t_json = serializetopic(q)
    return success(t_json['topics'], 'topics')

def deltopic(request,q_id, t_id):
    try:
        q = Question.objects.get(q_id = q_id)
        q.delTopic(t_id)
        q.save()
        return success({'id': t_id, 'message': 'Topic deleted'}, 'success')
    except Exception as e:
        print("exception: " + str(e))
        return error('Invalid form data')

def embedlist(request):
    q_id = parse_qs(request.environ['QUERY_STRING'])['q_id'][0]
    q = Question.objects.get(q_id = q_id)
    e_json = serializeembed(q)
    return success(e_json['embeds'], 'embeds')

def addembed(request):
    try:
        qid = request.POST['q_id']
        body = request.POST['body']
        
        q = Question.objects.get(q_id = request.POST['q_id'])
        embed = q.addEmbed(body)
        urllib.request.urlretrieve(body,"questions/" +qid +"/tex/" + str(embed.e_id) + ".jpg")
        
        q.save()
        return success({'id': embed.e_id, 'message': 'Embed added'}, 'success')
    except Exception as e:
        print("exception: " + str(e))
        return error('Invalid form data')

def updembed(r):
    try:
        qid = r.POST['q_id']
        body = r.POST['body']
        eid = r.POST['e_id']

        m = Question.objects.get(q_id = qid)
        m.updateEmbed(eid, body)
        urllib.request.urlretrieve(body,"questions/" +qid +"/tex/" + str(eid) + ".jpg")
        
        m.save()
        return success('Question updated','message')
    except Exception as e:
        print("exception: " + str(e))
        return error('Invalid form data')

def delembed(request,q_id, e_id):
    try:
        q = Question.objects.get(q_id = q_id)
        q.delEmbed(e_id)
        q.save()
        return success({'id': e_id, 'message': 'Embed deleted'}, 'success')
    except Exception as e:
        print("exception: " + str(e))
        return error('Invalid form data')

def choicelist(request):
    q_id = parse_qs(request.environ['QUERY_STRING'])['q_id'][0]
    q = Question.objects.get(q_id = q_id)
    c_json = serializechoice(q)
    return success(c_json['choices'], 'choices')

def addchoice(request):
    try:
        q = Question.objects.get(q_id = request.POST['q_id'])
        choice = q.addChoice(request.POST['body'], request.POST['iscorrect'], request.POST['pos'])
        q.save()
        return success({'id': choice.c_id, 'message': 'Choice added'}, 'success')
    except Exception as e:
        print("exception: " + str(e))
        return error('Invalid form data')

def updchoice(request):
    try:
        m = Question.objects.get(q_id = request.POST['q_id'])
        m.updateChoice(request.POST['c_id'], request.POST['body'], request.POST['iscorrect'], request.POST['pos'] )
        m.save()
        return success('Question updated','message')
    except Exception as e:
        print("exception: " + str(e))
        return error('Invalid form data')

def delchoice(request,q_id, c_id):
    try:
        q = Question.objects.get(q_id = q_id)
        q.delChoice(c_id)
        q.save()
        return success({'id': c_id, 'message': 'Choice deleted'}, 'success')
    except Exception as e:
        print("exception: " + str(e))
        return error('Invalid form data')

def getpdf(request, q_id):
    q = Question.objects.get(q_id = q_id)
    imagepath = q.getPDF()
    return success(imagepath, 'path')

# Create your views here.
def index(request, q_id):
    #return HttpResponse('Question is here')

    question = Question.objects.get(q_id = q_id)
    context ={
        'question' : question
    } 
    return render(request, 'question/index.html', context)

def add(request):
    try:
        q_id = ""
        if(request.POST['submit'] == 'addQuestion'):
            question = Question()
            question.addQuestion(request)
            q_id = question.q_id
            question.save()
        
        return redirect('/question/edit/{}/'.format(q_id))

    except KeyError:
        return render(request, 'question/add.html',
        {'formAction': '/question/add/'})

def edit(request, q_id):

    try:
        question = Question.objects.get(q_id = q_id)
    except:
        return HttpResponse("ERROR VAR")

    try:
        # TODO
        # getlatex should be a GET
        if(request.POST['submit'] == 'getLatex'):
            latex = question.getLatex(False)
            print(latex)
        elif(request.POST['submit'] == 'copyQuestion'):
            newq = question.copyQuestion()
            newq.save()

            for i in range(len(newq.embeds)):
                embed = newq.embeds[i]
                urllib.request.urlretrieve(embed.body,"questions/" +newq.q_id +"/tex/" + str(embed.e_id) + ".jpg")
        

        elif(request.POST['submit'] == 'Cancel'):
            print("cancel")
        else:
            return HttpResponse("ERROR VAR 2")
    
        return redirect('/question/edit/{}/'.format(q_id))
        
    except KeyError:
        return render(request, 'question/edit.html', {
            'question': question,
            'formAction': '/question/edit/{}/'.format(q_id)
        })
