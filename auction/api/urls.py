from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api.views import user_won_lots

app_name='api'

urlpatterns = [
    path('lots/won/', user_won_lots, name='user_won_lots'),
]
urlpatterns = format_suffix_patterns(urlpatterns)