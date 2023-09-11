from django.urls import path
from .views import PasswordCheckView

app_name = 'accounts'

urlpatterns = [
    path('check_password/', PasswordCheckView.as_view(), name='check_password'),
]