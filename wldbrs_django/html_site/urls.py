from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeIndex.as_view(), name='home'),
    path('category/<str:product_type>/', Category.as_view(), name='category'),
    path('telegram/', Telegram.as_view(), name='telegram'),
    path('about/', About.as_view(), name='about'),
]