from django.contrib import admin

from .models import Category, Lot, LotImage, LotShippingDetails, Bid


admin.site.register(Category)

admin.site.register(Lot)
admin.site.register(LotShippingDetails)


admin.site.register(LotImage)
admin.site.register(Bid)

