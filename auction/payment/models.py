from django.db import models
from django.contrib.auth import get_user_model
from lot.models import Lot, Bid
User = get_user_model()

class Transaction(models.Model):
    lot = models.OneToOneField(Lot, on_delete=models.CASCADE, related_name='transactions')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    final_price =models.PositiveIntegerField()
    transaction_time = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.buyer.username} purchased {self.lot.name} for ${self.final_price}"
    