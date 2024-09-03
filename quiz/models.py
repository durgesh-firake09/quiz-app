from django.db import models
from authentication.models import Subscriber
import datetime
# Create your models here.


class Quiz(models.Model):
    id = models.AutoField(primary_key=True, null=False, unique=True)
    quiz_name = models.CharField(max_length=40)
    no_of_questions = models.IntegerField()
    created_on = models.DateTimeField(default=datetime.datetime.now())
    is_active = models.BooleanField(default=False)
    created_by = models.ForeignKey(to=Subscriber, on_delete=models.CASCADE)


    def __str__(self) -> str:
        return f"{self.id} - {self.quiz_name}"


class Question(models.Model):
    id = models.AutoField(primary_key=True, null=False, unique=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.CharField(max_length=100)
    marks = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.id} - {self.question}"

    def getAnswers(self):
        answer_objs = list(Answer.objects.filter(question=self))
        data = []
        for answer_obj in answer_objs:
            data.append({'answerId': answer_obj.id, 'answer': answer_obj.answer,
                        'isCorrect': answer_obj.is_correct})
        return data


class Answer(models.Model):
    id = models.AutoField(primary_key=True, null=False, unique=True)
    answer = models.CharField(max_length=100)
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.answer
