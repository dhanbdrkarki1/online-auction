from django.urls import path
from . import views

app_name = 'auctionapp'

urlpatterns = [
    path('', views.index, name='item_list'),
]