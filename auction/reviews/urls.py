from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path("seller/<slug:username>/feedback/", views.seller_review, name="seller_reviews"),
]