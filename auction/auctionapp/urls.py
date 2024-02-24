from django.urls import path
from . import views

app_name = 'auctionapp'

urlpatterns = [
    path('', views.index, name='home'),
    path('categories/<slug:catgory_slug>/', views.lots_based_on_category, name='lots_based_on_category'),
    path('favorite/lots/', views.favorite_lots, name='favorite_lots'),

]