from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('chat/', views.chat, name='chat_view'),
    path('chat/<int:other_user_id>/', views.chat, name='user_chat'),


]