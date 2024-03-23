from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('request/esewa/', views.esewa_request, name='esewa_request'),
    path('verify/esewa/', views.esewa_verify, name='esewa_verify'),
    path('request/khalti/', views.khalti_request, name='khalti_request'),
    path('verify/khalti/', views.khalti_verify, name='khalti_verify'),
]