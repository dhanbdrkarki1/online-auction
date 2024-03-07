from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from .choices import *
from datetime import timedelta

from django.utils.text import slugify
from django.utils import timezone
from .utils import rename_image
from channels.db import database_sync_to_async

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
    auction_duration = models.IntegerField(default=2, choices=DurationChoices.choices) # auctioning period of time: 2 ,4 ,5, 10
    scheduled_time = models.DateTimeField(null=True, blank=True) # start auction only at scheduled time
    quantity = models.PositiveIntegerField(default=1)
    favorites = models.ManyToManyField(User, blank=True, related_name='favorite_lots')

    is_auction_over = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)



    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    # time left to complete the live auction
    def get_time_left(self):
        if self.auction_start_time and self.auction_duration:
            closing_time = self.auction_start_time + timedelta(days=self.auction_duration)
            now = timezone.now()

            if now >= closing_time:
                return "Bid closed."

            time_left = closing_time - now
            days_left = time_left.days
            hours_left = time_left.seconds // 3600
            minutes_left = (time_left.seconds % 3600) // 60

            if days_left > 0:
                return f"{days_left} day{'s' if days_left > 1 else ''} left"
            elif hours_left > 0:
                return f"{hours_left} hour{'s' if hours_left > 1 else ''} left"
            else:
                return f"{minutes_left} minute{'s' if minutes_left > 1 else ''} left"

    def get_absolute_url(self):
        return reverse('lots:lot_detail',args=[self.slug])
    
    def get_absolute_url_full_name(self):
        url_string = f"{self.seller.first_name.lower()}-{self.seller.last_name.lower()}"
        url_string = url_string.replace(' ', '-')
        return reverse('lots:seller_detail', kwargs={'full_name': url_string})

    # closing time based on auction start time and duration
    def get_closing_time(self):
        closing_time = self.auction_start_time + timezone.timedelta(days=self.auction_duration)
        return closing_time

    # Checking if the bidding for this lot is closed
    def is_bidding_closed(self):
        return self.get_closing_time() <= timezone.now()
    
    
    class Meta:
        ordering=('name',)
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created'])
        ]
    
    def __str__(self):
        return self.name

    @database_sync_to_async
    def get_seller_name(self):
        return self.seller.get_username_display()

class LotShippingDetails(models.Model):
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE, related_name="lotShippingDetails")
    package_type = models.CharField(max_length=50, choices=PackageTypeChoices.choices)  # e.g., box, envelope
    dimensions = models.CharField(max_length=50)  # e.g., 10x10x10
    weight = models.CharField(max_length=50, choices=WeightRangeChoices.choices)  # e.g., box, envelope
    item_location = models.CharField(max_length=100)  # e.g., city, state, country
    carrier = models.CharField(max_length=50, choices=WeightRangeChoices.choices)  # e.g., Trucking, Air Freight, Courier services like FedEx, UPS
    shipment_cost = models.PositiveIntegerField(null=True, blank=True) 
    shipping_notes = models.TextField(blank=True, null=True)

    # shipment status

    def __str__(self):
        return f"{self.lot.name}'s Shipping Details"


class LotImage(models.Model):
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE, related_name="lotImages")
    image = models.ImageField(null=False, blank=False, upload_to=rename_image)

    def __str__(self):
        return self.lot.name
    

class Bid(models.Model):
    lot = models.ForeignKey('Lot', on_delete=models.CASCADE, related_name='bids')
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    amount = models.PositiveIntegerField()
    bidded_at = models.DateTimeField(default=timezone.now)
    accepted = models.BooleanField(default=False)

    # return the highest bid for the lot
    def is_highest_bid(self):
            highest_bid = Bid.objects.filter(lot=self.lot).order_by('-amount').first()
            return self == highest_bid


SHIPPING_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )

class LotShippingStatus(models.Model):
    lot = models.OneToOneField(Lot, on_delete=models.CASCADE, related_name="shipping_status")
    status = models.CharField(max_length=20, choices=SHIPPING_STATUS_CHOICES, default='pending')
    status_updated_at = models.DateTimeField(auto_now=True)
    delivery_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Shipping status for {self.lot.name}"
