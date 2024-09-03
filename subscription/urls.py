from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('pricing/', view=views.pricing,name='Pricing'),
    path('upgrade/', view=views.upgrade,name='Upgrade'),
]
