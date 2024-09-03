from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('join/', views.join, name="JoinQuiz"),
    path('create/', views.create_quiz, name="CreateQuiz"),
    path('window/', views.window, name="QuizWindow"),
    path('create/<str:id>/add/', views.add, name="AddQue"),
    path('dashboard/', views.dashboard, name="QuizDashboard"),
    path('delete/<str:id>/', views.deleteQuiz, name="DeleteQuiz"),
    path('manage/<str:id>/', views.manageQue, name="ManageQue"),
    path('delete/que/<str:queid>/', views.deleteQue, name="DeleteQue"),
    path('activate/<str:id>/', views.activateQuiz, name="ActivateQuiz"),
    path('deactivate/<str:id>/', views.deactivateQuiz, name="DeactivateQuiz"),
]
