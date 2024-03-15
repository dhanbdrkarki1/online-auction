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

    path('password/reset/', views.password_reset_request, name="request_password_reset"),
    path('password/reset/sent', views.password_reset_sent, name="password_reset_sent"),

    path('password/reset/<str:user_id>/<str:token>/', views.password_reset_confirm, name="password_reset_confirm"),





    path('settings/profile/send-verification-email/', views.send_verification_email, name='send_verification_email'),
    path('confirm-email/<str:user_id>/<str:token>/', views.confirm_email, name='confirm_email'),




]