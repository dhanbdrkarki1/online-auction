from django.contrib import admin
from payment.models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['lot', 'buyer', 'final_price', 'transaction_time',]
    list_filter = ('buyer__email',)
    search_fields = ('lot__name', 'buyer__email',)
    list_display_links = ('lot',)