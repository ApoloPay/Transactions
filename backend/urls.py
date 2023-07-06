from rest_framework.authtoken import views as vx
from rest_framework import routers
from django.urls import include, path
from . import views

router = routers.DefaultRouter()
#router.register(r'Transactions', views.TransactionViewset)

urlpatterns = [
    path('', include(router.urls)),
    path('deposit/', views.Deposit),
    path('withdraw/', views.Withdraw),
    path('release-withdraw/', views.ReleaseWithdraw),
    path('release-blocked/', views.ReleaseBlocked),
    path('block-available-funds/', views.BlockAvailableFunds),
    path('release-blocked-funds/', views.ReleaseBlockedFunds),
    path('transfer/', views.Transfer),
    path('create-balance/',views.CreateBalance),
    path('get-balance/',views.GetBalance),
    path('get-asset-balance/',views.GetAssetBalance),
    path('get-history/',views.UserHistory),
]