from django.db import models
from subscription.models import Subscription

# Create your models here.


class Subscriber(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=101, unique=True)
    password = models.CharField(max_length=512)
    mobile = models.IntegerField()
    org = models.CharField(max_length=100)
    active_subscription = models.ForeignKey(
        to=Subscription, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{str(self.sno)} - {self.name} - {self.active_subscription}"
