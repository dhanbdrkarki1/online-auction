from django.urls import path
from . import views

app_name = 'auctionapp'

urlpatterns = [
    path('login/', views.index, name='login'),
]