from django.contrib import admin
from django.urls import path
from .views import CreateUserView, TestSignalRollbackAPIView
urlpatterns = [
    path('registration/', CreateUserView.as_view(), name='user-register'),
    path('testRollback/', TestSignalRollbackAPIView.as_view(), name='test-rollback'),
]