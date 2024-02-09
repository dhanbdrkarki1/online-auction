from django.contrib import admin
from .models import *

# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     prepopulated_fields = {'slug': ('name',)}
#     list_display = ['name', 'slug']
#     list_filter = ['name','created','updated']
#     search_fields = ['name', 'description']

# @admin.register(SubCategory)
# class SubCategoryAdmin(admin.ModelAdmin):
#     prepopulated_fields = {'slug': ('name',)}
#     list_display = ['name', 'slug']
#     list_filter = ['name','created','updated']
#     search_fields = ['name', 'description']

# @admin.register(Item)
# class ItemAdmin(admin.ModelAdmin):
#     list_display = ['name', 'slug']
#     list_filter = ['created','updated']
#     search_fields = ['name', 'description']
#     prepopulated_fields = {'slug': ('name',)}
#     ordering = ['is_live', 'is_active','created']