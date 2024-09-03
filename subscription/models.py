from django.db import models

# Create your models here.
class Subscription(models.Model):
    subId = models.CharField(max_length=10,primary_key=True)
    price = models.IntegerField()
    max_questions = models.IntegerField()
    max_quizes = models.IntegerField()

    def __str__(self) -> str:
        return self.subId +" : "+ str(self.price)