from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from .choices import *
from django.utils.text import slugify
from django.utils import timezone
from .utils import rename_image

User=get_user_model()

class Category(models.Model):
    name = models.TextField(unique=True, max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, null=True)
    description = models.CharField(max_length=500, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='sub_category')
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        indexes = [
            models.Index(fields=['name'])
        ]

class Lot(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='lots')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lots')
    name=models.CharField(max_length=255,db_index=True)
    slug=models.SlugField(max_length=255,db_index=True)

    condition = models.CharField(max_length=255, default='New', choices=ConditionChoices.choices)

    description = models.TextField(blank=True)

    # selling details
    starting_price=models.PositiveIntegerField()
    buy_it_now_price=models.PositiveIntegerField(null=True, blank=True)
    reserve_price=models.PositiveIntegerField(null=True, blank=True)

    auction_start_time = models.DateTimeField(null=True, blank=True)
    auction_duration = models.IntegerField(default=2, choices=DurationChoices.choices) # auctioning period of time
    scheduled_time = models.DateTimeField(null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_auction_over = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('lots:lot_detail',args=[self.slug])

    class Meta:
        ordering=('name',)
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created'])
        ]
    
    def __str__(self):
        return self.name


class LotShippingDetails(models.Model):
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE, related_name="lotShippingDetails")
    package_type = models.CharField(max_length=50, choices=PackageTypeChoices.choices)  # e.g., box, envelope
    dimensions = models.CharField(max_length=50)  # e.g., 10x10x10
    weight = models.CharField(max_length=50, choices=WeightRangeChoices.choices)  # e.g., box, envelope
    item_location = models.CharField(max_length=100)  # e.g., city, state, country
    carrier = models.CharField(max_length=50, choices=WeightRangeChoices.choices)  # e.g., Trucking, Air Freight, Courier services like FedEx, UPS
    shipment_cost = models.PositiveIntegerField(null=True, blank=True) 
    shipping_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.lot.name}'s Shipping Details"




class LotImage(models.Model):
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE, related_name="lotImages")
    image = models.ImageField(null=False, blank=False, upload_to=rename_image)

    def __str__(self):
        return self.lot.name
    