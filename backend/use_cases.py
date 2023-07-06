from .models import * 
from .serializers import * 
from django.db import transaction
import requests as external_requests
import datetime
import math
def checkBalance(user):
    return UserBalanceSerializer(instance=UserBalance.objects.get(user=user)).data

def createBalance(user):
    r = external_requests.post('http://control-center:6003/api/asset/', json={})
    rdata = r.json()
    for asset in rdata:
        balance, created = UserBalance.objects.get_or_create(user=user,asset=asset["id"])
        balance.save()
    return 'Created'

def checkAvailable(user,asset,amount):
    return True if UserBalance.objects.get(user=user,asset=asset).available >= amount else False 

def checkBlocked(user,asset,amount):
    return True if UserBalance.objects.get(user=user,asset=asset).blocked >= amount else False

def blockAvailableFunds(user,asset,amount,origin='P2P',id_transaction=None):
    assert checkAvailable(user,asset,amount), 'insufficient available funds'
    balance = UserBalance.objects.get(user=user,asset=asset)
    balance.available =  balance.available - amount
    balance.blocked = balance.blocked + amount
    balance.save()
    new_transaction = Transaction(user=user,asset=asset,amount=amount,type='blocked',description='blocked funds',origin=origin,id_transaction=id_transaction)
    new_transaction.save()
    return TransactionSerializer(instance=new_transaction).data
    
def releaseBlockedFunds(user_origin,user_destination,amount,asset,parent_transaction=None,origin='P2P',id_transaction=None):
    assert checkBlocked(user_origin,asset,amount), 'insufficient blocked funds'
    balance_origin = UserBalance.objects.get(user=user_origin,asset=asset)
    balance_origin.blocked = balance_origin.blocked - amount
    balance_origin.save()
    balance_destination = UserBalance.objects.get(user=user_destination,asset=asset)
    balance_destination.available = balance_destination.available + amount
    balance_destination.save()
    if(parent_transaction):
        p_transaction=Transaction.objects.get(id=parent_transaction)
        new_transaction = Transaction(user=user_destination,asset=asset,amount=amount,type='Release',description='release blocked funds',parent_transaction=p_transaction,origin=p_transaction.origin)
    else:
        new_transaction = Transaction(user=user_destination,asset=asset,amount=amount,type='Release',description='release blocked funds',origin=origin,id_transaction=id_transaction)
    new_transaction.save()
    return TransactionSerializer(instance=new_transaction).data

##transfer method
@transaction.atomic
def transfer(user_origin,user_destination,amount,asset):
    try:
        origen = blockAvailableFunds(user_origin,asset,amount,origin='Transfer')
    except Exception as e:
        return str(e)
    try:
        trx = releaseBlockedFunds(user_origin,user_destination,amount,asset,origen["id"],origin='Transfer')
    except Exception as e:
        return str(e)
    return TransactionSerializer(instance=Transaction.objects.get(id=origen["id"])).data

##deposit method
def deposit(user,asset,amount,id_transaction,description,origin='Tron-Service'):
    if(id_transaction):
        assert Transaction.objects.filter(user=user,asset=asset,id_transaction=id_transaction).count() == 0 , 'id transaction repeated'
        balance_destination = UserBalance.objects.get(user=user,asset=asset)
        balance_destination.available += amount
        balance_destination.save()
        new_transaction = Transaction(user=user,asset=asset,amount=amount,type='deposit',description=description,id_transaction=id_transaction,origin=origin)
        new_transaction.save()
        return TransactionSerializer(instance=new_transaction).data
    else:
        raise "id transaction required"

##Process withdraw
@transaction.atomic
def startWithdraw(user,asset,amount,address):
    if(asset=="1"):
        origen = blockAvailableFunds(user,asset,amount,origin='Withdraw')
        json = {"userid": str(user),"toaddress": address,"amount": float(amount), "token": str(asset)}
        resp = external_requests.post('http://micro-tron:6007/micro-service-tron/account/withdraw/', json=json)
        if resp.status_code == 200:
            return releaseWithdraw(origen)
        else:
            return "ups... some went wrong"
    else:
        return "asset in develop"

##release withdraw
@transaction.atomic
def releaseWithdraw(origen):
    parent_transaction = Transaction.objects.get(id=origen["id"])
    balance_destination = UserBalance.objects.get(user=parent_transaction.user,asset=parent_transaction.asset)
    balance_destination.blocked -= parent_transaction.amount
    balance_destination.save()
    new_transaction = Transaction(user=parent_transaction.user,asset=parent_transaction.asset,amount=parent_transaction.amount,type='release withdraw',description=parent_transaction.description,parent_transaction=parent_transaction,origin=parent_transaction.origin)
    new_transaction.save()
    return TransactionSerializer(instance=new_transaction).data

def getBalance(user):
    assert UserBalance.objects.filter(user=user).count()>0, 'Sorry, no info for you'
    return UserBalanceSerializer(instance=UserBalance.objects.get(user=user)).data

def getAssetBalance(user,asset):
    assert UserBalance.objects.filter(user=user,asset=asset).count()>0, 'Sorry, no info for you'
    return UserBalanceSerializer(instance=UserBalance.objects.get(user=user,asset=asset)).data

def getUserHistory(user,start_date,end_date,type,page):
    start_date = datetime.datetime.strptime(start_date, '%d/%m/%Y')
    end_date = datetime.datetime.strptime(end_date+' 23:59:59', '%d/%m/%Y %H:%M:%S')
    data=[]
    if(type=='all'):
        transactions=Transaction.objects.filter(user=user,datetime__range=(start_date,end_date)).order_by('-datetime')
    else:
        transactions=Transaction.objects.filter(user=user,datetime__range=(start_date,end_date),type=type).order_by('-datetime')
    for transaction in transactions:
         data.append(TransactionSerializer(instance=transaction).data)
    records = len(data)
    total_pages = math.floor(records/10)+1
    data.sort(key=lambda r: r['datetime'], reverse=True)
    to_return = [data[i:i+10] for i in range(0, len(data), 10)]
    if (records >0):
        if (page <= total_pages and page > 0):
            data_to_return = to_return[page-1]
        else:
            data_to_return = []
    else:
        data_to_return = []
    return {'total_pages':total_pages,'total_records':records,'current_page':page,'data':data_to_return} 

