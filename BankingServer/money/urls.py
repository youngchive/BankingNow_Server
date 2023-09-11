from django.urls import path

from .views import BalanceCheckView
app_name = 'money'

urlpatterns = [
    path('check_balance/', BalanceCheckView.as_view(), name='check_password'),
]