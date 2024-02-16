from django.urls import path
from . import views

app_name = 'lots'

urlpatterns = [
    path('seller/lots/', views.lot_list, name='lots_list'),
    path('seller/lot/create/', views.lot_create, name='lot_create'),
    path('seller/lot/images/save/', views.save_lot_images, name='save_lot_images'),
    path('lots/<slug:slug>/', views.lot_detail, name='lot_detail'),

    path('lot/received/', views.lot_received, name='lot_received'),

    path('search-categories/', views.search_categories, name='search_categories'),


   
]
