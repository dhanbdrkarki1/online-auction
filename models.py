from django.db import models
from datetime import datetime
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model


User=get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)

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

class Seller(models.Model):
    name=models.CharField(max_length=200)
    seller_photo=models.ImageField(upload_to='photos/seller/%Y/%m/%d/')
    contact_no =models.CharField(max_length=200)
    email=models.CharField(max_length=200)
    def get_absolute_url(self):
        return reverse('auction:seller-page',args=[self.id])
    
    def __str__(self):
        return self.name
    
class Item(models.Model):
    category=models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    seller =models.ForeignKey(Seller,on_delete=models.DO_NOTHING)
    
    name=models.CharField(max_length=200,db_index=True)
    slug=models.SlugField(max_length=200,db_index=True)
    image=models.ImageField(upload_to='items/%Y/%m/%d', null=True, blank=True)
    description = models.TextField(blank=True)

    starting_price=models.DecimalField(max_digit=12, decimal_places=2)
    current_price=models.DecimalField(max_digit=12, decimal_places=2, blank=True)

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='winner')

    
    # is_live=models.BooleanField(default=False)
    # is_trending=models.BooleanField(default=False)
    # on_banner=models.BooleanField(default=False)
    # year_published=models.DateTimeField(default=datetime.now())

    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    #  tags:one to many fields 
    
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



class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="upload_to='items/%Y/%m/%d")

    def __str__(self):
        return self.item.name
    
    
# class Bid(models.Model):
#     bidder = models.ForeignKey(User, on_delete=models.CASCADE)
#     item = models.ForeignKey(Item, on_delete=models.CASCADE)
#     bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     bid_time = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.bidder.username} bid ${self.bid_amount} on {self.item.title}"

# class Transaction(models.Model):
#     item = models.OneToOneField(Item, on_delete=models.CASCADE)
#     buyer = models.ForeignKey(User, on_delete=models.CASCADE)
#     final_price = models.DecimalField(max_digits=10, decimal_places=2)
#     transaction_time = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.buyer.username} purchased {self.item.title} for ${self.final_price}"
    
# class Wishlist(models.Model):
#     lot=models.CharField(max_length=1000)
#     name=models.CharField(max_length=200)
#     slug=models.SlugField(max_length=200,db_index=True,null=True,blank=True)
#     lot_id=models.IntegerField()
#     Wishlisted_date=models.DateTimeField(default=datetime.now,blank=True)
#     user_id=models.IntegerField(blank=False)
    
#     def get_absolute_url(self):
#         return reverse('auction:single-item',args=[self.lot_id,self.slug])
#     def __srt__(self):
#         return self.name


# class SellerReview(models.Model):
#     RATING_CHOICES = [
#         (1, '1'),
#         (2, '2'),
#         (3, '3'),
#         (4, '4'),
#         (5, '5'),
#     ]

#     reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given')
#     seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_received')
#     rating = models.IntegerField(choices=RATING_CHOICES)
#     feedback = models.TextField()
#     created = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ('-created',)
    
#     def __str__(self):
#         return f"{self.reviewer.username} -> {self.seller.username}: {self.rating}"

#     # def get_absolute_url(self):
#     #     return reverse('auction:seller_detail', args=[str(self.seller.id)])


# class Contact(models.Model):
#     lot=models.CharField(max_length=1000)
#     lot_id=models.IntegerField()
#     name=models.CharField(max_length=200)
#     email=models.CharField(max_length=200)
#     slug=models.SlugField(max_length=200,db_index=True,null=True,blank=True)
#     message=models.TextField(blank=True)
#     contact_date=models.DateTimeField(default=datetime.now,blank=True)
#     user_id=models.IntegerField(blank=True)
    
#     def get_absolute_url(self):
#         return reverse('auction:single-item',args=[self.lot_id,self.slug])
    