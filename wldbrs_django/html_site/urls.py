from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeIndex.as_view(), name='home')
]