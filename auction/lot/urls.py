from django.urls import path
from . import views

app_name = 'lots'

urlpatterns = [
    path('lots/', views.lot_list, name='lots_list'),
    path('lot/create', views.lot_create, name='lot_create'),
    path('lot/received', views.lot_received, name='lot_received'),

    path('search-categories/', views.search_categories, name='search_categories'),


   
]
