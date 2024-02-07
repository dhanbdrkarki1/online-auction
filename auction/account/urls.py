from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('settings/profile/address/', views.shippingAddress, name="shipping_address"),
    path('settings/profile/', views.profileInfo, name="profile_info"),

]