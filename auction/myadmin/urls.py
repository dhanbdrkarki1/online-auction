from django.urls import path
from . import views

app_name = 'myadmin'

urlpatterns = [
    path('', views.index, name='index'),
    path('category/create/', views.createCategory, name='category_create'),
    path('category/<str:slug>/', views.categoryDetail, name='category_detail'),
]