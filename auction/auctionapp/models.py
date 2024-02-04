from django.db import models
from datetime import datetime
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    name = models.CharField(unique=True, max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def get_absolute_url(self):
        return reverse('auction:items_by_category', args=[self.slug])
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        indexes = [
            models.Index(fields=['name']),
        ]
    
    def __str__(self):
        return self.name 

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(unique=True, max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def get_absolute_url(self):
        return reverse('auction:items_by_subcategory', args=[self.slug])
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'subcategory'
        verbose_name_plural = 'subcategories'
        indexes = [
            models.Index(fields=['name']),
        ]
    
    def __str__(self):
        return self.name
    
class Item(models.Model):
    # category=models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    # seller =models.ForeignKey(Seller,on_delete=models.DO_NOTHING)
    # winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='winner')
    
    name=models.CharField(max_length=200,db_index=True)
    slug=models.SlugField(max_length=200,db_index=True)
    image=models.ImageField(upload_to='items/%Y/%m/%d', null=True, blank=True)
    description = models.TextField(blank=True)

    starting_price=models.DecimalField(max_digits=12, decimal_places=2)
    current_price=models.DecimalField(max_digits=12, decimal_places=2, blank=True)

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    is_live=models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def get_absolute_url(self):
        return reverse('auction:single-item',args=[self.id,self.slug])
    
    class Meta:
        ordering=('name',)
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created'])
        ]
    
    def __str__(self):
        return self.name






