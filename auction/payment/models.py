from django.db import models
from django.contrib.auth import get_user_model
from lot.models import Lot, Bid
User = get_user_model()


PAYMENT_METHOD = (
    ('Esewa', 'Esewa'),
    ('Khalti', 'Khalti'),
)

class Transaction(models.Model):
    lot = models.OneToOneField(Lot, on_delete=models.CASCADE, related_name='transactions')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    final_price =models.PositiveIntegerField()
    transaction_time = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_METHOD, default="")
    status = models.BooleanField(default=False)

    
    def __str__(self):
        return f"{self.buyer.first_name} purchased {self.lot.name} for Rs.{self.final_price}"
    