from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('settings/profile/', views.profileInfo, name="profile_info"),
    path('settings/profile/address/', views.shippingAddress, name="shipping_address"),
    path('settings/profile/change-password/', views.change_password, name="change_password"),


    path('send-verification-email/', views.send_verification_email, name='send-verification-email'),
    path('confirm-email/<int:user_id>/<slug:token>/', views.confirm_email, name='confirm-email'),




]