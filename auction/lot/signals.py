# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Bid
# from .tasks import email_on_bid_placed

# @receiver(post_save, sender=Bid)
# def sent_email_after_bid(sender, instance, created, **kwargs):
#     if created:
#         print("bid created......")
#         email_on_bid_placed.delay(instance.id, instance.lot.id)