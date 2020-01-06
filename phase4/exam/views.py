from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Exam, QuestionId
from question.models import Question
from qbank.models import Qbank

# Create your views here.
def index(request):
    # get all question
    exam = Exam.objects.all()
    context ={
        'exams' : exam
    }
    return render(request, 'exam/index.html', context)

def details(request, e_id):
    exam = Exam.objects.get(e_id = e_id)
    questions = []
    for x in exam.question_list:
        q = Question.objects.get(q_id = x)
        questions.append(q)

    context ={
        'exam': exam,
        'questions': questions,
        'formAction': '/exam/details/{}/'.format(e_id)
    }

    try:
        if(request.POST['submit'] == 'createShuffled'):
            n = int(request.POST['shuffleNumber'])
            exam.createShuffled(n)
            exam.save()

        elif(request.POST['submit'] == 'getLatexExam'):
            no = int(request.POST['examNumber'])
            # res = exam.getLatexExam(no)
            # return res

        elif(request.POST['submit'] == 'getLatexKey'):
            no = int(request.POST['examNumber'])
            # res = exam.getLatexKey(no)
            # return res
        
        elif(request.POST['submit'] == 'getPDFExam'):
            no = int(request.POST['examNumber'])
            res = exam.getPDFExam(no)
            # Opens a tab containing pdf
            return res

        elif(request.POST['submit'] == 'getPDFKey'):
            no = int(request.POST['examNumber'])
            res = exam.getPDFKey(no)
            # Opens a tab containing pdf key
            return res

        elif(request.POST['submit'] == 'getCSVKey'):
            res = exam.getCSVKey()
            return res

        elif(request.POST['submit'] == 'refresh'):        
            return render(request, 'exam/details.html', context)
        
        elif(request.POST['submit'] == 'getLatex'):
            qbank = Qbank()
            iterator = iter(questions)
            qbank.getLatex(iterator,False)
        
        elif(request.POST['submit'] == 'deleteExam'):
            Exam.objects.get(e_id = e_id).delete()
            return redirect('/exam')

        return render(request, 'exam/details.html', context)

    except KeyError:

        return render(request, 'exam/details.html', context)

def filterquestion(questions, rhs):

    notselected_questions = []
    for allq in rhs:
        if allq in questions:
            # it is selected
            continue
        else:
            notselected_questions.append(allq)

    return notselected_questions

def edit(request, e_id):

    # find exam
    exam = Exam.objects.get(e_id = e_id)
    # fill exam's questions
    questions = []
    for x in exam.question_list:
        q = Question.objects.get(q_id = x)
        questions.append(q)

    all_questions = Question.objects.all()
    notselected_questions = []

    context ={
        'exam': exam,
        'questions': questions,
        'formAction': '/exam/edit/{}/'.format(e_id)
    }

    try:
        if(request.POST['submit'] == 'editExamName'):
            exam.editExamName(request.POST['examname'])
            exam.save()

        elif(request.POST['submit'] == 'searchByTopic'):
            qbank = Qbank()
            search_results = qbank.searchByTopic(request.POST['topic'])

            notselected_questions = filterquestion(questions, search_results)

        elif(request.POST['submit'] == 'searchByDate'):
            qbank = Qbank()
            search_results = qbank.searchByAskDate(request.POST['start'], request.POST['end'])

            notselected_questions = filterquestion(questions, search_results)
        
        elif(request.POST['submit'] == 'updateAskDate'):
            
            qbank = Qbank()
            iterator = iter(questions)
            # update selected questions' ask date
            qbank.updateAskDate(iterator,request.POST['date'])
            # update exam's ask date
            exam.updateAskDate(request.POST['date'])
            exam.save()
        
            notselected_questions = filterquestion(questions, all_questions)
        
        elif(request.POST['submit'] == 'addQuestion'):

            r = request.POST['question']
            # create question_id object
            new_question = QuestionId()
            new_question.q_id = r
            # append to the exam
            exam.question_list.append(new_question)

            context['questions'].append(Question.objects.get(q_id = r))
            exam.save()

            notselected_questions = filterquestion(questions, all_questions)
        
        elif(request.POST['submit'] == 'remove'):
            # remove qustion from selected list
            r = request.POST['question']
            index = 0

            for q in exam.question_list:
                if r == q.q_id:
                    del exam.question_list[index]
                    break
                index += 1

            for q in context['questions']:
                if r == q.q_id:
                    context['questions'].remove(q)
                    break

            exam.save()

            notselected_questions = filterquestion(questions, all_questions)

        context['notselected_questions'] = notselected_questions

        return render(request, 'exam/edit.html', context)

    except KeyError:
        
        notselected_questions = filterquestion(questions, all_questions)
        context['notselected_questions'] = notselected_questions
        return render(request, 'exam/edit.html', context)

def create(request):
    '''
        create exam with:
        name, creation date, id
    '''

    try:
        e_id = ""
        if(request.POST['submit'] == 'createExam'):
            exam = Exam()
            exam.createExam(request)
            e_id = exam.e_id
            exam.save()

        return redirect('/exam/edit/{}/'.format(e_id))

    except KeyError:
        return render(request, 'exam/create.html',
        {'formAction': '/exam/create/'})
