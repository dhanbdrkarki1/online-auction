from django.contrib import admin

from .models import Category, Lot


# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Lot)
class LotAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}