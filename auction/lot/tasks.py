from celery import shared_task
from django.core.mail import send_mail
from .models import Bid
from django.contrib.humanize.templatetags import humanize
from django.conf import settings

# @shared_task
# def bid_placed(bid_id):
#     """
#     Task to send an e-mail notification when an bid is
#     successfully created.
#     """
#     try:
#         bid = Bid.objects.get(id=bid_id)
#         bid_amount = str(humanize.intcomma(bid.amount))
#         print("bid_id..........", bid_id)
#         subject = f'Your bid has been placed successfully'
#         message = f'Dear {bid.bidder.first_name},\n\n' \
#                   f'You have successfully placed a bid.\n' \
#                   f'Your bid ID is {bid.id}.\n' \
#                   f'Bid amount: {bid_amount}\n'
#         sender = 'hunterdbk5@gmail.com'
#         receipient_list = ['dhan.karki@study.lbef.edu.np']
#         mail_sent = send_mail(subject, message, sender, receipient_list)
#         if(mail_sent):
#             print("email sent...")
#         else:
#             print("email not sent...")

#         return mail_sent
#     except Bid.DoesNotExist:
#         print("Bid does not exist.......................")
#         return False 
    
@shared_task
def email_on_bid_placed(bid_id, lot_id):
    """
    Task to send e-mail notifications when a bid is successfully placed to bidder
    as well as other bidder informing highest bid is made.
    """
    try:
        bid = Bid.objects.get(id=bid_id)
        bid_amount = str(humanize.intcomma(bid.amount))
        
        # Email to the bidder
        subject_bidder = 'Your bid has been placed successfully'
        message_bidder = f'Dear {bid.bidder.first_name},\n\n' \
                         f'You have successfully placed a bid.\n' \
                         f'Your bid ID is {bid.id}.\n' \
                         f'Bid amount: {bid_amount}\n'
        sender = settings.EMAIL_HOST_USER
        print("sender............",sender)
        recipient_bidder = [bid.bidder.email]
        mail_sent_bidder = send_mail(subject_bidder, message_bidder, sender, recipient_bidder)

        # Check if there are other bidders on the same lot
        other_bidders = Bid.objects.filter(lot=bid.lot).exclude(bidder=bid.bidder)
        print(other_bidders)
        if other_bidders.exists():
            # Email to all users engaged in bidding on the same lot (excluding current bidder)
            subject_users = 'New highest bid placed on lot you bidded'
            message_users = f'A new bid has been placed on the lot.\n' \
                            f'New highest Bid amount: {bid_amount}\n'
            recipient_users = set([user.bidder.email for user in other_bidders])  # Exclude current bidder
            print("recipient users", recipient_users)
            mail_sent_users = send_mail(subject_users, message_users, sender, recipient_users)

            if not mail_sent_users:
                print("Failed to send email to other bidders")
        else:
            print("No other bidders on the lot")

        if mail_sent_bidder:
            print("Email sent successfully to bidder")
        else:
            print("Failed to send email to bidder")
    except Bid.DoesNotExist:
        print("Bid does not exist.......................")
        return False 