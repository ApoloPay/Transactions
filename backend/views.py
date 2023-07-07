from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import *
from rest_framework.response import Response
from rest_framework import viewsets, status, generics
from rest_framework.decorators import api_view,permission_classes
from .serializers import * 
from django.views.decorators.csrf import csrf_exempt
from .use_cases import *
import datetime
from decimal import Decimal
#Generics
class TransactionViewset(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

@api_view(["POST"])
@csrf_exempt
@permission_classes([AllowAny])
def Deposit(request):
    return Response(deposit(request.data["user"],request.data["asset"],Decimal(request.data["amount"]),request.data["id_transaction"],request.data["description"]), status=status.HTTP_200_OK)

@api_view(["POST"])
@csrf_exempt
@permission_classes([AllowAny])
def Transfer(request):
    try:
        return Response(transfer(request.data["user_origin"],request.data["user_destination"],Decimal(request.data["amount"]),request.data["asset"]), status=status.HTTP_200_OK)
    except Exception as e:
        return Response(e,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
@csrf_exempt
@permission_classes([AllowAny])
def ReleaseWithdraw(request):
    try:
        return Response(releaseWithdraw(request.data["trx"]), status=status.HTTP_200_OK)
    except Exception as e:
        return Response(e,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
@csrf_exempt
@permission_classes([AllowAny])
def Withdraw(request):
    #try:
        return Response(startWithdraw(request.data["user"],request.data["asset"],Decimal(request.data["amount"]),request.data["wallet"]), status=status.HTTP_200_OK)
    #except Exception as e:
     #   return Response(e,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
@csrf_exempt
@permission_classes([AllowAny])
def ReleaseBlocked(request):
    try:
        return Response(ReleaseBlockedFunds(request.data["user_origin"],request.data["user_destination"],Decimal(request.data["amount"]),request.data["asset"]), status=status.HTTP_200_OK)
    except Exception as e:
        return Response(e,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
@csrf_exempt
@permission_classes([AllowAny])
def GetBalance(request):
    try:
        return Response(getBalance(request.data["user"]), status=status.HTTP_200_OK)
    except Exception as e:
        return Response(e,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
@csrf_exempt
@permission_classes([AllowAny])
def GetAssetBalance(request):
    try:
        return Response(getAssetBalance(request.data["user"],request.data["asset"]), status=status.HTTP_200_OK)
    except Exception as e:
        return Response(e,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
@csrf_exempt
@permission_classes([AllowAny])
def CreateBalance(request):
    return Response(createBalance(request.data["user"]), status=status.HTTP_200_OK)

#############Historical
@api_view(["POST"])
@csrf_exempt
@permission_classes([AllowAny])
def UserHistory(request):
    return Response(getUserHistory(user=request.data.get("user"),start_date=request.data.get("start_date"),end_date=request.data.get("end_date"),type=request.data.get("type"),page=request.data.get("page"),origin=request.data.get("origin")or{}), status=status.HTTP_200_OK)

@api_view(["POST"])
@csrf_exempt
@permission_classes([AllowAny])
def GetHistoryDetail(request):
    return Response(getHistoryDetail(id_transaction=request.data.get("id_transaction")), status=status.HTTP_200_OK)

#####FOR P2P
@api_view(["POST"])
@csrf_exempt
@permission_classes([AllowAny])
def BlockAvailableFunds(request):
    return Response(blockAvailableFunds(request.data["user"],request.data["asset"],Decimal(request.data["amount"]),id_transaction=request.data["id_transaction"]), status=status.HTTP_200_OK)

@api_view(["POST"])
@csrf_exempt
@permission_classes([AllowAny])
def ReleaseBlockedFunds(request):
    return Response(releaseBlockedFunds(request.data["user_origin"],request.data["user_destination"],Decimal(request.data["amount"]),request.data["asset"],id_transaction=request.data["id_transaction"]), status=status.HTTP_200_OK)
