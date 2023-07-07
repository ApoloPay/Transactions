from rest_framework import fields, serializers
from .models import *
from django.db.models import Q

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"

class UserBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBalance
        fields = "__all__"

class TransactionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields=['id','user','asset','amount','origin','type','description','status','datetime','parent_transaction','id_transaction','parent','children','releated']
    
    releated = serializers.SerializerMethodField('LoadReleated')
    def LoadReleated(self, obj):
        return TransactionSerializer(Transaction.objects.filter(Q(id_transaction=obj.id_transaction,id_transaction__isnull=False),~Q(id=obj.id)),many=True).data
    

    children = serializers.SerializerMethodField('LoadChildren')
    def LoadChildren(self, obj):
        return TransactionSerializer(Transaction.objects.filter(Q(parent_transaction=obj),~Q(id=obj.id)),many=True).data

    parent = serializers.SerializerMethodField('LoadParent')
    def LoadParent(self, obj):
        if obj.parent_transaction:
            return TransactionSerializer(Transaction.objects.filter(id=obj.parent_transaction.id),many=True).data
        else:
            return []

        