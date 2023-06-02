from .models import * 
from django.db import transaction


def check_balance(user):
    return UserBalance.objects.get(user_id=user)
    
def deposit(user,asset,amount,description):
    new_transaction = Transaction(user_id=user,asset_id=asset,amount=amount,type=type,description=description)
    return new_transaction.save()

def withdraw(user,asset,amount,type,description):
    new_transaction = Transaction(user_id=user,asset_id=asset,amount=amount,type=type,description=description)
    return new_transaction.save()

def blockFounds(user,asset,amount):
    if checkAvailable(user,asset,amount):
        balance = UserBalance.objects.get(user=user,asset=asset)
        balance.available -= amount
        balance.blocked +=amount

def ReleaseBlockedFounds(user_origin,user_destination,amount,asset):
    balance_origin = UserBalance.objects.get(user=user_origin,asset=asset)
    balance_destination = UserBalance.objects.get(user=user_destination,asset=asset)
    balance_origin.blocked = balance_origin.blocked - ammount
    balance_destination.available = balance_destination.available + ammount


##transfer method
@transaction.atomic
def transfer(user_origin,user_destination,amount,asset):
    ##block user_origin
    blockFounds(user_origin,asset,amount)
    ##release blocked founds to destination
    ReleaseBlockedFounds(user_origin,user_destination,amount,asset)





    
