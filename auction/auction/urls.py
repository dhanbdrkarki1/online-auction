from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('auctionapp.urls', namespace='auctionapp')),
    path('myadmin/', include('myadmin.urls', namespace='myadmin')),
    path('account/', include('account.urls', namespace='account')),
    path('social-auth/', include('social_django.urls', namespace='social')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
