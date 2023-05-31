from django.db import models
from simple_history.models import HistoricalRecords


class Transaction(models.Model):
    user_id=models.TextField(default=None, null=True,blank =False)
    user_name=models.TextField(default=None, null=True,blank =False)
    asset_id=models.TextField(default=None, null=True,blank =False)
    asset_name=models.TextField(default=None, null=True,blank =False)
    amount=models.DecimalField(max_digits=20,decimal_places = 4,default=0.0)
    type=models.TextField(default=None, null=True,blank =False)
    description=models.TextField(default=None, null=False,blank =True)
    datetime=models.DateTimeField(auto_now_add=True)
    history =HistoricalRecords()

class UserBalance(models.Model):
    user_id=models.TextField(default=None, null=True,blank =False)
    available=models.DecimalField(max_digits=20,decimal_places = 4,default=0.0)
    blocked=models.DecimalField(max_digits=20,decimal_places = 4,default=0.0)
    history = HistoricalRecords()