from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import Subscriber
from subscription.models import Subscription
from django.contrib import messages

# Create your views here.


def getUser(request):
    try:
        if (request.session["loggedIn"]):
            return request.session['userName']
    except Exception as e:
        return None

def getUserEmail(request):
    try:
        if (request.session["loggedIn"]):
            return request.session['userEmail']
    except Exception as e:
        return None

def checkLoggedIn(request):
    try:
        if request.session["loggedIn"] == True:
            return True
        else:
            return False

    except Exception as e:
        return False


def login(request):
    if (checkLoggedIn(request)):
        return redirect('/')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print(email)
        try:
            user = Subscriber.objects.filter(email=email).first()
            print(user)
            if (check_password(password, user.password)):
                request.session["userEmail"] = email
                request.session["userName"] = user.name
                request.session["loggedIn"] = True
                messages.success(request, "Logged in as "+user.name)
                return redirect('/')
            else:
                messages.error(request, "Invalid Credentials")
        except Exception as e:
            messages.error(request, "User Not Found")
    return render(request, 'authTemplates/login.html')


def signUp(request):
    if checkLoggedIn(request):
        return redirect('/')
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['mobile']
        org = request.POST['org']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        # print(name,email,phone,org,pass1,pass2)
        if (pass1 == pass2):
            user = Subscriber.objects.filter(email=email)
            if (len(user) > 0):
                messages.error(request, email+" - User Already Exists")
                return redirect('/auth/sign-up/')
            password = make_password(pass1)
            freeSub = Subscription.objects.filter(
                subId__contains='FREE').first()
            # print(freeSub)
            user = Subscriber(name=name, email=email, password=password,
                              mobile=phone, org=org, active_subscription=freeSub)
            # print(user)
            user.save()
            messages.success(
                request, "User Created Successfully! Please Login")
            return redirect('/auth/login/')
        else:
            messages.error(
                request, 'Password and Confirm Password must be same')
    return render(request, 'authTemplates/signUp.html')


def logout(request):
    request.session.flush()
    messages.info(request, "Logged Out Successfully")
    return redirect('/auth/login/')
