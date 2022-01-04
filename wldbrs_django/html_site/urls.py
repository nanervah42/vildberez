from django.urls import path
from .views import *


urlpatterns = [
    path('', HomeIndex.as_view(), name='home'),
    path('category/<str:product_type>/', CategoryView.as_view(), name='category'),
    path('telegram/', TelegramView.as_view(), name='telegram'),
    path('about/', AboutView.as_view(), name='about'),
    path('thanks/', ThanksView.as_view(), name='thanks'),
    path('feedback/', FeedBackView.as_view(), name='feedback'),
]