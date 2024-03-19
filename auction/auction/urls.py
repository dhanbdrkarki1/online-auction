from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
    path('admin/', admin.site.urls),
    path('', include('auctionapp.urls', namespace='auctionapp')),
    path('account/', include('account.urls', namespace='account')),
    path('', include('lot.urls', namespace='lots')),
    path('', include('chat.urls', namespace='chat')),

    path('social-auth/', include('social_django.urls', namespace='social')),

    # auction api
    path('api/', include('api.urls', namespace='auction_api')),
    path('payment/', include('payment.urls', namespace='payment')),
    path('', include('reviews.urls', namespace='reviews')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
