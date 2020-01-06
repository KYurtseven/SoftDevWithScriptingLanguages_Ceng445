from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Question

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
            
            print("inside post")
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
        if(request.POST['submit'] == 'updateParent'):
            question.updateParent(request.POST['p_id'])
            question.save()

        elif(request.POST['submit'] == 'updateAskDate'):
            question.updateAskDate(request.POST['ask_date'])
            question.save()

        elif(request.POST['submit'] == 'add_embed'):
            question.addEmbed(request.POST['embed'])
            question.save()

        elif(request.POST['submit'] == 'add_topic'):
            question.addTopic(request.POST['topic'])
            question.save()

        elif(request.POST['submit'] == 'add_choice'):
            question.addChoice(
                request.POST['body'],
                request.POST['correct'],
                request.POST['position']
            )
            question.save()

        elif(request.POST['submit'] == 'update_body'):
            question.updateBody(request.POST['body'])
            question.save()

        elif(request.POST['submit'] == 'updateEmbed'):
            question.updateEmbed(
                request.POST['e_id'],
                request.POST['body']
            )
            question.save()

        elif(request.POST['submit'] == 'updateTopic'):
            question.updateTopic(
                request.POST['t_id'],
                request.POST['body']
            )
            question.save()

        elif(request.POST['submit'] == 'updateChoice'):
            question.updateChoice(
                request.POST['c_id'],
                request.POST['body'],
                request.POST['iscorrect'],
                request.POST['position']
            )
            question.save()

        elif(request.POST['submit'] == 'delEmbed'):
            question.delEmbed(request.POST['e_id'])
            question.save()

        elif(request.POST['submit'] == 'delTopic'):
            question.delTopic(request.POST['t_id'])
            question.save()

        elif(request.POST['submit'] == 'delChoice'):
            question.delChoice(request.POST['c_id'])
            question.save()

        elif(request.POST['submit'] == 'copyQuestion'):
            newq = question.copyQuestion()
            newq.save()

        # TODO
        # getlatex should be a GET
        elif(request.POST['submit'] == 'getLatex'):
            question.getLatex(False)
            print("inside getlatex")

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
