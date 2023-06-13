from .models import * 
from .serializers import * 
from django.db import transaction

def checkBalance(user):
    return UserBalanceSerializer(instance=UserBalance.objects.get(user_id=user)).data

def checkAvailable(user,asset,amount):
    return True if UserBalance.objects.get(user_id=user,asset=asset).available >= amount else False 

def blockAvailableFunds(user,asset,amount):
    assert checkAvailable(user,asset,amount), 'insufficient funds'
    balance = UserBalance.objects.get(user=user,asset=asset)
    balance.available -= amount
    balance.blocked +=amount
    balance.save()
    new_transaction = Transaction(user_id=user,asset_id=asset,amount=amount,type='blocked',description='blocked funds')
    new_transaction.save()
    return TransactionSerializer(instance=new_transaction).data
    
def ReleaseBlockedFunds(user_origin,user_destination,amount,asset,parent_transaction=None):
    balance_origin = UserBalance.objects.get(user=user_origin,asset=asset)
    balance_destination = UserBalance.objects.get(user=user_destination,asset=asset)
    balance_origin.blocked = balance_origin.blocked - amount
    balance_destination.available = balance_destination.available + amount
    new_transaction = Transaction(user_id=user_destination,asset_id=asset,amount=amount,type='Release',description='release blocked funds',parent_transaction=parent_transaction)
    new_transaction.save()
    return TransactionSerializer(instance=new_transaction).data

##transfer method
@transaction.atomic
def transfer(user_origin,user_destination,amount,asset):
    ##block user_origin
    origen = blockAvailableFunds(user_origin,asset,amount)
    ##release blocked funds to destination
    trx = ReleaseBlockedFunds(user_origin,user_destination,amount,asset,origen)
    trx.save()
    return TransactionSerializer(instance=trx).data

##deposit method
def deposit(user,asset,amount,id_transaction,description):
    balance_destination = UserBalance.objects.get(user=user,asset=asset)
    balance_destination.available += amount
    balance_destination.save()
    assert Transaction.objects.filter(id_transaction=id_transaction).count()>0, 'id transaction repeated'
    new_transaction = Transaction(user_id=user,asset_id=asset,amount=amount,type='deposit',description=description)
    new_transaction.save()
    return TransactionSerializer(instance=new_transaction).data

##start withdraw
def blockWithdraw(user,asset,amount):
    origen = blockAvailableFunds(user,asset,amount)
    return TransactionSerializer(instance=origen).data

##release withdraw
@transaction.atomic
def releaseWithdraw(origen):
    parent_transaction = Transaction.objects.get(id=origen)
    balance_destination = UserBalance.objects.get(user=parent_transaction.user,asset=parent_transaction.asset)
    balance_destination.blocked -= parent_transaction.amount
    balance_destination.save()
    new_transaction = Transaction(user_id=parent_transaction.user,asset_id=parent_transaction.asset,amount=parent_transaction.amount,id_transaction=str(origen),type='release withdraw',description=parent_transaction.description,parent_transaction=parent_transaction)
    new_transaction.save()
    return TransactionSerializer(instance=new_transaction).data
    
def getBalance(user):
    assert UserBalance.objects.filter(user=user).count()>0, 'Sorry, no info for you'
    return UserBalanceSerializer(instance=UserBalance.objects.get(user=user)).data

def getUserHistory(user,start_date,end_date,type,page):
    start_date = datetime.datetime.strptime(start_date)
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
        if (request.data['pagina'] <= total_pages and page > 0):
            data_to_return = to_return[page-1]
        else:
            data_to_return = []
    else:
        data_to_return = []
    return {'total_pages':total_pages,'total_records':records,'current_page':page,'data':data_to_return} 