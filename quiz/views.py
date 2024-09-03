from django.shortcuts import render, HttpResponse, redirect
import json
from django.http import JsonResponse
from django.contrib import messages
from authentication.views import checkLoggedIn, getUser, getUserEmail
from quiz.models import Quiz, Question, Answer
from authentication.models import Subscriber
import datetime
# Create your views here.

# from django import template
# from django.template.defaultfilters import stringfilter

# register = template.Library()


# @register.filter
# @stringfilter
# def tojson(s):
#     return json.loads(s)


def window(request):
    context = {}
    context['loggedIn'] = checkLoggedIn(request)
    context['user'] = getUser(request)
    if request.method == 'POST':
        q_id = request.POST['quizID']
        quiz = Quiz.objects.filter(id=q_id).first()
        context['email'] = request.POST['email']

        context['name'] = request.POST['name']
        if (quiz == None):
            messages.error(request, "Quiz Not Found")
            return redirect('/quiz/join/')
        questions = Question.objects.filter(quiz=quiz)
        quiz_obj = {
            "quizName": quiz.quiz_name,
            "quizID": quiz.id,
            "que_num": quiz.no_of_questions,
            "questions": [
                {
                    "queId": question.id,
                    "que": question.question,
                    "options": question.getAnswers()
                } for question in questions
            ]
        }
        # for i in range(len(quiz_obj['questions'])):
        #     quiz_obj['questions'][i] = json.loads(quiz_obj['questions'][i])

        print(quiz_obj)
        context['quiz_obj'] = quiz_obj
        # TODO Designing quiz display page
        # return render(request,'quizTemplates/window.html',context=context)
        return render(request, 'quizTemplates/window.html', context=context)


def join(request):

    context = {}
    context['loggedIn'] = checkLoggedIn(request)
    context['user'] = getUser(request)
    if request.method == 'POST':
        q_id = request.POST['quizID']
        quiz = Quiz.objects.filter(id=q_id).first()
        if (quiz == None):
            messages.error(request, "Quiz Not Found")
            return redirect('/quiz/join/')
        elif not quiz.is_active:
            messages.error(request, "Quiz not Started")
            return redirect('/quiz/join/')
        context['quizID'] = q_id

    # if request.method == 'POST':
    #     q_id = request.POST['quizID']
    #     quiz = Quiz.objects.filter(id=q_id).first()
    #     if (quiz == None):
    #         messages.error("Quiz Not Found")
    #         return redirect('/quiz/join/')
    #     questions = Question.objects.filter(quiz=quiz)
    #     quiz_obj = {
    #         "quizID": quiz.id,
    #         "questions": [
    #             {
    #                 "queId": question.id,
    #                 "que": question.question,
    #                 "options": question.getAnswers()
    #             } for question in questions
    #         ]
    #     }

    #     print(quiz_obj)
    #     context['quiz_obj'] = quiz_obj

        return render(request, 'quizTemplates/startquiz.html', context=context)

    return render(request, 'quizTemplates/join.html', context=context)


def create_quiz(request):
    context = {}
    context['loggedIn'] = checkLoggedIn(request)
    context['user'] = getUser(request)
    if (request.method == "POST"):

        title = request.POST['title']
        numQue = request.POST['numberQuestions']

        quiz = Quiz(quiz_name=title, no_of_questions=numQue,
                    created_by=Subscriber.objects.filter(email=getUserEmail(request)).first())
        if (quiz.created_by.active_subscription.max_quizes >= len(Quiz.objects.filter(created_by=Subscriber.objects.filter(email=getUserEmail(request)).first()))):
            messages.error(request,"Max Limit Exceeded, Please Buy a Subscription")
            return redirect('/quiz/dashboard/')
        quiz.save()
        print(quiz)
        context['quizID'] = quiz.id
        messages.success(request, "Quiz Created")
        return redirect('/quiz/dashboard/')
    return render(request, 'quizTemplates/create.html', context=context)


def add(request, id):
    context = {}
    context['loggedIn'] = checkLoggedIn(request)
    context['user'] = getUser(request)
    if (context['loggedIn']):
        quiz = Quiz.objects.filter(id=id).first()
        context['quid'] = quiz.no_of_questions+1
        if (quiz == None):
            messages.error(request, "Quiz Doesn't Exist")
            return redirect('/quiz/dashboard/')
        elif (quiz.created_by != Subscriber.objects.filter(email=getUserEmail(request)).first()):
            return redirect('/quiz/dashboard/')
        context['quizID'] = quiz.id
        if request.method == 'POST':
            if (quiz.no_of_questions >= quiz.created_by.active_subscription.max_questions):
                messages.error(
                    request, 'Maximum Questions Limit Exceeded, Please Buy a Subscription...')
                return redirect('/quiz/dashboard/')
            question = request.POST['question']
            op1 = request.POST['option-1-q-'+id]
            op2 = request.POST['option-2-q-'+id]
            op3 = request.POST['option-3-q-'+id]
            op4 = request.POST['option-4-q-'+id]
            correct = request.POST['correct']
            que = Question(quiz=Quiz.objects.filter(
                id=id).first(), question=question, marks=1)
            que.save()
            ans1 = Answer(answer=op1, question=que,
                          is_correct=(correct == '1'))
            ans2 = Answer(answer=op2, question=que,
                          is_correct=(correct == '2'))
            ans3 = Answer(answer=op3, question=que,
                          is_correct=(correct == '3'))
            ans4 = Answer(answer=op4, question=que,
                          is_correct=(correct == '4'))
            ans1.save()
            ans2.save()
            ans3.save()
            ans4.save()
            # print(question)
            print(op1, op2, op3, op4, correct)
            print(ans2.is_correct)
            quiz.no_of_questions += 1
            quiz.created_on = datetime.datetime.now()
            quiz.save()
            redirect('/quiz/create/'+str(quiz.id)+'/add/')
        # print(id)
        return render(request, "quizTemplates/addQuestions.html", context=context)
    return redirect('/')


def dashboard(request):
    context = {}
    context['loggedIn'] = checkLoggedIn(request)
    context['user'] = getUser(request)
    quizes = Quiz.objects.filter(created_by=Subscriber.objects.filter(
        email=getUserEmail(request)).first())
    print(quizes)
    context['quizes'] = quizes
    context['subscription'] = quizes[0].created_by.active_subscription
    return render(request, 'quizTemplates/dashboard.html', context=context)


def deleteQuiz(request, id):
    context = {}
    context['loggedIn'] = checkLoggedIn(request)
    context['user'] = getUser(request)
    if (context['loggedIn']):
        quiz = Quiz.objects.filter(id=id).first()
        if (quiz == None):
            messages.error(request, "Quiz Doesn't Exist")
        elif (quiz.created_by != Subscriber.objects.filter(email=getUserEmail(request)).first()):
            return redirect('/quiz/dashboard/')
        else:
            quiz.delete()
            messages.error(request, "Quiz Deleted Successfully")
        return redirect('/quiz/dashboard/')
    return redirect('/')


def manageQue(request, id):
    context = {}
    context['loggedIn'] = checkLoggedIn(request)
    context['user'] = getUser(request)
    if (context['loggedIn']):
        quiz = Quiz.objects.filter(id=id).first()
        if (quiz == None):
            messages.error(request, "Quiz Doesn't Exist")
        elif (quiz.created_by != Subscriber.objects.filter(email=getUserEmail(request)).first()):
            return redirect('/quiz/dashboard/')
        else:
            questions = Question.objects.filter(quiz=quiz)
            print(questions)
            context['questions'] = [
                {
                    "que": question,
                    "answers": question.getAnswers(),
                    "correct": [ans['answer'] for ans in question.getAnswers() if ans['isCorrect']][0]
                }for question in questions
            ]
            print(context['questions'])
        return render(request, 'quizTemplates/manageQuestions.html', context=context)


def deleteQue(request, queid):
    context = {}
    context['loggedIn'] = checkLoggedIn(request)
    context['user'] = getUser(request)
    if (context['loggedIn']):
        que = Question.objects.filter(id=queid).first()
        qid = que.quiz.id
        if (que == None):
            messages.error(request, "Question Doesn't Exist")
        elif (que.quiz.created_by != Subscriber.objects.filter(email=getUserEmail(request)).first()):
            return redirect('/quiz/dashboard/')
        else:
            que.quiz.no_of_questions -= 1
            que.quiz.save()
            que.delete()

            messages.error(request, "Question Deleted Successfully")
        return redirect('/quiz/manage/'+str(qid)+'/')
    return redirect('/')


def activateQuiz(request, id):
    context = {}
    context['loggedIn'] = checkLoggedIn(request)
    context['user'] = getUser(request)
    if (context['loggedIn']):
        quiz = Quiz.objects.filter(id=id).first()
        if (quiz == None):
            messages.error(request, "Quiz Doesn't Exist")
        elif (quiz.created_by != Subscriber.objects.filter(email=getUserEmail(request)).first()):
            return redirect('/quiz/dashboard/')
        else:
            quiz.is_active = True
            quiz.save()
            messages.success(request, "Quiz Activated Successfully")
        return redirect('/quiz/dashboard/')
    messages.error(request, "Not Authorized")
    return redirect('/quiz/dashboard/')


def deactivateQuiz(request, id):
    context = {}
    context['loggedIn'] = checkLoggedIn(request)
    context['user'] = getUser(request)
    if (context['loggedIn']):
        quiz = Quiz.objects.filter(id=id).first()
        if (quiz == None):
            messages.error(request, "Quiz Doesn't Exist")
        elif (quiz.created_by != Subscriber.objects.filter(email=getUserEmail(request)).first()):
            return redirect('/quiz/dashboard/')
        else:
            quiz.is_active = False
            quiz.save()
            messages.success(request, "Quiz Activated Successfully")
        return redirect('/quiz/dashboard/')
    messages.error(request, "Not Authorized")
    return redirect('/quiz/dashboard/')
