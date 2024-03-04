from django.contrib import admin

from .models import Category, Lot, LotImage, LotShippingDetails, Bid


admin.site.register(Category)

@admin.register(Lot)
class LotAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'auction_start_time', 'is_auction_over', 'category', 'seller', 'condition', 'starting_price', 'buy_it_now_price', 'reserve_price']
    list_filter = ('seller', 'category', 'is_auction_over', 'auction_duration',  'condition',)
    ordering = ('-auction_start_time', 'created',)
    search_fields = ('name', 'seller', 'category',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(LotShippingDetails)
class LotShippingDetailsAdmin(admin.ModelAdmin):
    list_display = ['id', 'lot', 'package_type', 'carrier', 'shipment_cost',]
    list_filter = ('package_type', 'carrier',)
    search_fields = ('lot', 'package_type', 'carrier',)

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


