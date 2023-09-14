from django.contrib import admin
from django.urls import path, include
#from django.conf.urls import url
# from .serializers import
from . import views
# from .views import deposit_view, withdraw_view, transfer_view

urlpatterns = [
    path('employee-signup/', views.TransferView.as_view()),
    #path('student-signup/', views.StudentCreate.as_view()),
]