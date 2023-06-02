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

@transaction.atomic
def transfer(user_origin,user_destination,amount,asset):
    ##block user_origin
    blockFounds(user_origin,asset,amount)
    ##block deposit destiny
    blockDeposit(user_destination,asset,amount)
    ##clear user_origin block
    clearBlockFounds(user_origin,asset,amount)
    ##release deposit destiny
    releaseBlockFounds(user_destination,asset,amount)

def blockFounds(user,asset,amount):
    if checkAvailable(user,asset,amount):
        balance = UserBalance.objects.get(user=user,asset=asset)
        balance.available -= amount
        balance.blocked +=amount

def blockDeposit(user,asset,amount):
    balance = UserBalance.objects.get(user=user,asset=asset)
    balance.blocked +=amount

def clearBlockFounds(user,asset,amount):
    balance = UserBalance.objects.get(user=user,asset=asset)
    balance.blocked -=amount

def releaseBlockFounds(user,asset,amount):
    balance = UserBalance.objects.get(user=user,asset=asset)
    balance.available += amount
    balance.blocked -=amount

def checkAvailable(user,asset,amount):
    return True if UserBalance.objects.get(user=user,asset=asset).available >= amount else False
