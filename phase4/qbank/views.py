from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Question


# Create your views here.
def index(request):

    try:
        question = Question.objects.all()
    except:
        return HttpResponse("ERROR VAR")

    context ={
        'questions' : question
    }


    return render(request, 'qbank/index.html', context)

