from django.urls import path
from . import views

app_name = 'auctionapp'

urlpatterns = [
    path('', views.item_list, name='item_list'),
    # path('<int:id>/', views.post_detail, name='item_detail'),
]