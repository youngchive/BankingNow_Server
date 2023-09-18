
from django.contrib import admin
from django.urls import path, include
#from django.conf.urls import url
# from .serializers import
from . import views
# from .views import deposit_view, withdraw_view, transfer_view
from .views import BalanceCheckView, TransferView, AccountCheckView
app_name = 'money'

urlpatterns = [
    path('check_balance/', BalanceCheckView.as_view(), name='check_password'),
    path('transfer/', TransferView.as_view(), name='transfer'),
    path('account-check/', AccountCheckView.as_view(), name='account-check'),
]
