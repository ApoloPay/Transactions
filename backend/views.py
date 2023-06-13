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
#Generics
class TransactionViewset(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

@api_view(["POST"])
@csrf_exempt
@permission_classes([AllowAny])
def Deposit(request):
    try:
        return Response(deposit(request.data["user"],request.data["asset"],request.data["amount"],request.data["id_transaction"],request.data["description"]), status=status.HTTP_200_OK)
    except Exception as e:
        return Response(e,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
@csrf_exempt
@permission_classes([AllowAny])
def Transfer(request):
    try:
        return Response(transfer(request.data["user_origin"],request.data["user_destination"],request.data["amount"],request.data["asset"]), status=status.HTTP_200_OK)
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
    try:
        return Response(transfer(request.data["user_origin"],request.data["user_destination"],request.data["amount"],request.data["asset"]), status=status.HTTP_200_OK)
    except Exception as e:
        return Response(e,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
@csrf_exempt
@permission_classes([AllowAny])
def ReleaseBlocked(request):
    try:
        return Response(ReleaseBlockedFunds(request.data["user_origin"],request.data["user_destination"],request.data["amount"],request.data["asset"]), status=status.HTTP_200_OK)
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


#############Historical
@api_view(["POST"])
@csrf_exempt
@permission_classes([AllowAny])
def UserHistory(request):
    try:
        return Response(getUserHistory(request.data["user"],request.data["start_date"],request.data["end_date"],request.data["type"],request.data["page"]), status=status.HTTP_200_OK)
    except Exception as e:
        return Response(e,status=status.HTTP_500_INTERNAL_SERVER_ERROR)