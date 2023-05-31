from .models import * 
def check_balance(user):
    return UserBalance.objects.get(user_id=user)
    
def deposit(user,amount,type,description):
    #new transaction
    return pass

def withdraw(user,amount,type,description):
    return pass

def transfer(user_origin,user_destination,amount,asset,description):
    return pass

    

