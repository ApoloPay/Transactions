from rest_framework.authtoken import views as vx
from rest_framework import routers
from django.urls import include, path
from . import views

router = routers.DefaultRouter()

router.register(r'Transactions', views.TransactionViewset)


urlpatterns = [
    path('', include(router.urls)),
]