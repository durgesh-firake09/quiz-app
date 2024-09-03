from django.shortcuts import render, HttpResponse
from authentication.views import checkLoggedIn, getUser, getUserEmail
from authentication.models import Subscriber,Subscription
from django.contrib import messages
# Create your views here.


def pricing(request):
    return render(request, 'subscriptionTemplates/pricing.html')


def upgrade(request):
    context = {}
    context['loggedIn'] = checkLoggedIn(request)
    context['user'] = getUser(request)
    context['email'] = getUserEmail(request)
    if (context['loggedIn']):
        user = Subscriber.objects.filter(email=context['email']).first()
        context['subscription'] = user.active_subscription
        context['availableSubs'] = Subscription.objects.all().exclude(subId=user.active_subscription.subId)
        # print(availableSubs)
        if(request.method == 'POST'):
            if context['subscription'].subId == request.POST['activeSub']:
                print(request.POST['price'])

                newSub = Subscription.objects.filter(subId=request.POST['selectedSub']).first()
                if newSub!=None:
                    # TODO: Subscription Payment
                    user.active_subscription = newSub
                    user.save()
                    messages.success(request,"Subscription Added")
        return render(request, 'subscriptionTemplates/upgrade.html', context=context)
