from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api.views import paid_lots, unpaid_lots
# from api.views import user_won_lots


app_name='api'

urlpatterns = [
    # path('lots/won/', user_won_lots, name='user_won_lots'),
    path('lots/won/paid/', paid_lots, name='paid_lots'),
    path('lots/won/unpaid/', unpaid_lots, name='unpaid_lots'),

]
urlpatterns = format_suffix_patterns(urlpatterns)