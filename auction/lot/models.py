from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.text import slugify

User=get_user_model()

class Category(models.Model):
    name = models.CharField(unique=True, max_length=200, db_index=True)
    slug = models.SlugField(max_length=255, blank=True)
    description = models.CharField(max_length=1000, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='sub_category')

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        indexes = [
            models.Index(fields=['name'])
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Lot(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='lots')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lots')
    name=models.CharField(max_length=255,db_index=True)
    slug=models.SlugField(max_length=255,blank=True)
    description = models.TextField(blank=True)
    starting_price=models.DecimalField(max_digits=12, decimal_places=2)
    current_price=models.DecimalField(max_digits=12, decimal_places=2, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_auction_over = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('auction:single-item',args=[self.slug])

    class Meta:
        ordering=('name',)
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created'])
        ]
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class ItemImage(models.Model):
    item = models.ForeignKey(Lot, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="upload_to='lots/%Y/%m/%d")

    def __str__(self):
        return self.item.name
    