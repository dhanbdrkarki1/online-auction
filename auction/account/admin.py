from django.contrib import admin
from django.db.models import fields
from django.contrib.auth.admin import UserAdmin
from account.models import CustomUser, ShippingAddress


class CutomUserAdmin(UserAdmin):
    list_display = ('email','username','first_name','last_name', 'phone_number','phone_number_confirmation', 'email_confirmation',  'is_admin','is_verified','is_staff','is_active')
    list_filter = ('email', 'is_admin','is_staff','is_active')
    ordering = ('-created_at', 'email',)
    search_fields = ('email','username','first_name','last_name',)
    fieldsets = (
        (None, {'fields': ('username','email', 'password',)}),
        ('Personal Info', {'fields': ('first_name','last_name', 'phone_number',)}),
        ('Permissions', {'fields': ('is_verified','is_staff', 'is_active', 'is_admin', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','password1', 'password2',),
            }),
        ('Personal Info', {'fields': ('first_name','last_name', 'phone_number',)}),
        ('Permissions', {'fields': ('is_verified','is_staff', 'is_active', 'is_admin', 'is_superuser')}),
    
    )

admin.site.register(CustomUser, CutomUserAdmin)
admin.site.register(ShippingAddress)