from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api.views import paid_lots, unpaid_lots, lot_shipment, lot_shipment_update

app_name='api'

urlpatterns = [
    path('lots/won/paid/', paid_lots, name='paid_lots'),
    path('lots/won/unpaid/', unpaid_lots, name='unpaid_lots'),
    path('lots/ship/list/', lot_shipment, name='lot_shipment'),
    path('lots/ship/update/', lot_shipment_update, name='lot_shipment_update'),

]
urlpatterns = format_suffix_patterns(urlpatterns)