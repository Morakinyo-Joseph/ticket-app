from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser


class User(AbstractUser, models.Model):
    ig_handle = models.CharField(max_length=250)
    pass


class Game(models.Model):
    REMARK = (
        ("safe", "safe"),
        ("risky", "risky"),
        ("very risky", "very risky"),
    )
    ticket_ID = models.CharField(max_length=500)
    booking_code = models.CharField(max_length=200)
    odds = models.DecimalField(max_digits=5, decimal_places=2)
    remarks = models.CharField(max_length=20, choices=REMARK)
    date_created = models.DateTimeField(auto_now=True)



class History(models.Model):
    ticket_ID = models.CharField(max_length=500)
    booking_code = models.CharField(max_length=200)
    odds = models.IntegerField(default=0)
    remarks = models.CharField(max_length=20)
    date_created = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.booking_code
