from django.urls import path
from .views import index

urlpatterns = [
    path('', index),  # Main page of the frontend app
    path('home', index),  # Home page of the frontend app
    path('account-creation', index)
]
