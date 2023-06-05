from .models import * 
from .serializers import * 
from django.db import transaction

def checkBalance(user):
    return UserBalanceSerializer(instance=UserBalance.objects.get(user_id=user)).data

def checkAvailable(user,asset,amount):
    return True if UserBalance.objects.get(user_id=user,asset=asset).available >= amount else False 

def blockAvailableFounds(user,asset,amount):
    if checkAvailable(user,asset,amount):
        balance = UserBalance.objects.get(user=user,asset=asset)
        balance.available -= amount
        balance.blocked +=amount
        balance.save()
        new_transaction = Transaction(user_id=user,asset_id=asset,amount=amount,type='blocked',description='blocked founds')
        new_transaction.save()
        return new_transaction
    
def ReleaseBlockedFounds(user_origin,user_destination,amount,asset,parent_transaction):
    balance_origin = UserBalance.objects.get(user=user_origin,asset=asset)
    balance_destination = UserBalance.objects.get(user=user_destination,asset=asset)
    balance_origin.blocked = balance_origin.blocked - amount
    balance_destination.available = balance_destination.available + amount
    new_transaction = Transaction(user_id=user_destination,asset_id=asset,amount=amount,type='transfer',description='release blocked founds',parent_transaction=parent_transaction)
    new_transaction.save()
    return new_transaction


##transfer method
@transaction.atomic
def transfer(user_origin,user_destination,amount,asset):
    ##block user_origin
    origen = blockAvailableFounds(user_origin,asset,amount)
    ##release blocked founds to destination
    trx = ReleaseBlockedFounds(user_origin,user_destination,amount,asset,origen)
    return TransactionSerializer(instance=trx).data

    
def deposit(user,asset,amount,description):
    balance_destination = UserBalance.objects.get(user=user,asset=asset)
    balance_destination.available += amount
    balance_destination.save()
    new_transaction = Transaction(user_id=user,asset_id=asset,amount=amount,type='deposit',description=description)
    return new_transaction.save()

def blockWithdraw(user,asset,amount):
    origen = blockAvailableFounds(user,asset,amount)
    return TransactionSerializer(instance=origen).data

def releaseWithdraw(origen):
    parent_transaction = Transaction.objects.get(id=origen)
    balance_destination = UserBalance.objects.get(user=parent_transaction.user,asset=parent_transaction.asset)
    balance_destination.blocked -= parent_transaction.amount
    balance_destination.save()
    new_transaction = Transaction(user_id=parent_transaction.user,asset_id=parent_transaction.asset,amount=parent_transaction.amount,type='release withdraw',description=parent_transaction.description,parent_transaction=parent_transaction)
    new_transaction.save()
    return TransactionSerializer(instance=new_transaction).data
    
