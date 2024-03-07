from django.contrib import admin

from .models import Category, Lot, LotImage, LotShippingDetails, Bid, LotShippingStatus


admin.site.register(Category)

@admin.register(Lot)
class LotAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'auction_start_time', 'auction_duration', 'is_auction_over', 'category', 'seller', 'condition', 'starting_price', 'buy_it_now_price', 'reserve_price']
    list_filter = ('seller','is_auction_over', 'category',  'auction_duration',  'condition',)
    ordering = ('-auction_start_time', 'created',)
    search_fields = ('name', 'seller__first_name',  'category__name',)
    prepopulated_fields = {'slug': ('name',)}
    list_display_links = ('name',)



@admin.register(LotShippingDetails)
class LotShippingDetailsAdmin(admin.ModelAdmin):
    list_display = ['id', 'lot', 'package_type', 'carrier', 'shipment_cost',]
    list_filter = ('package_type', 'carrier',)
    search_fields = ('lot__name', 'package_type', 'carrier',)
    list_display_links = ('lot',)


@admin.register(LotImage)
class LotImageAdmin(admin.ModelAdmin):
    list_filter = ('lot',)
    search_fields = ('lot__name',)



@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ['id', 'lot', 'bidder', 'amount', 'accepted', 'bidded_at',]
    list_filter = ('bidder', 'accepted', 'lot',)
    ordering = ('-bidded_at', 'amount',)
    search_fields = ('lot','bidder',)
    list_display_links = ('lot',)


@admin.register(LotShippingStatus)
class LotShippingStatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'lot', 'status', 'status_updated_at', 'delivery_date',]
    list_filter = ('status',)
    ordering = ('-status_updated_at', 'delivery_date',)
    search_fields = ('lot',)