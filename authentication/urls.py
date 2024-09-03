from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.login, name='Login'),
    path('sign-up/', views.signUp, name='SignUp'),
    path('logout/', views.logout, name='Logout'),
]
