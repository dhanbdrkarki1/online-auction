from django.contrib import admin
from reviews.models import SellerReview

@admin.register(SellerReview)
class SellerReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'reviewer', 'seller', 'feedback', ]
    list_filter = ('seller', 'rating',)
    search_fields = ()
    list_display_links = ('seller',)

