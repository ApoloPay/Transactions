from django.db import models
from simple_history.models import HistoricalRecords


class Transaction(models.Model):
    STATUS = (
        ('P', 'Pending'),
        ('R', 'Rejected'),
        ('A', 'Aproved'),
    )
    user=models.TextField(default=None, null=True,blank =False)
    asset=models.TextField(default=None, null=True,blank =False)
    amount=models.DecimalField(max_digits=20,decimal_places = 4,default=0.0)
    type=models.TextField(default=None, null=True,blank =False)
    description=models.TextField(default=None, null=False,blank =True)
    status =models.CharField(max_length=1, choices=STATUS, default='P')
    datetime=models.DateTimeField(auto_now_add=True)
    parent_transaction=models.ForeignKey('self', on_delete=models.PROTECT, null=True)
    id_transaction=models.TextField(default=None, null=True,blank =True)
    history =HistoricalRecords()

class UserBalance(models.Model):
    user=models.TextField(default=None, null=True,blank =False)
    asset=models.TextField(default=None, null=True,blank =False)
    available=models.DecimalField(max_digits=20,decimal_places = 4,default=0.0)
    blocked=models.DecimalField(max_digits=20,decimal_places = 4,default=0.0)
    history = HistoricalRecords()