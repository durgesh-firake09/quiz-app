from django.shortcuts import render, HttpResponse
from authentication.views import checkLoggedIn, getUser
# Create your views here.


def home(request):
    context = {}

    context["loggedIn"] = checkLoggedIn(request)
    context['user'] = getUser(request)
    return render(request, 'home.html', context=context)
