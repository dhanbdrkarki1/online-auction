from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User=get_user_model()


class SellerReview(models.Model):
    RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]

    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_received')
    rating = models.IntegerField(choices=RATING_CHOICES)
    feedback = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)
    
    def __str__(self):
        return f"{self.reviewer.username} -> {self.seller.username}: {self.rating}"

    def get_absolute_url(self):
        return reverse('auction:seller_detail', args=[str(self.seller.id)])

