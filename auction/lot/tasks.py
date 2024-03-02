from celery import shared_task
from django.core.mail import send_mail
from .models import Bid, Lot
from django.contrib.humanize.templatetags import humanize
from django.conf import settings
from django.utils import timezone

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


@shared_task
def notify_winner_and_close_bidding(lot_id):
    try:
        lot = Lot.objects.get(id=lot_id)
        
        end_time = lot.auction_start_time + timezone.timedelta(hours=lot.auction_duration)
        # check if the lot has any bids
        has_bids_on_lot = lot.bids.exists()
        print("Total bids: " , lot.bids.count())

        # if bids on lot, send mail to winner otherwise seller informing no bids placed.
        if has_bids_on_lot:
            highest_bid = Bid.objects.filter(lot=lot).order_by('-amount').first()
            
            if highest_bid:
                highest_bidder_email = highest_bid.bidder.email
                sender = settings.EMAIL_HOST_USER

                subject = f'Bid Won for {lot.name}🎉🎊'
                message = f'Congratulations! You have the highest bid for lot {lot.name}. You have the highest bid for lot {lot.name}. Your bid amount is {highest_bid.amount}. Your lot will be delivered soon within the business days.'
                
                # Send email to the highest bidder
                send_mail(subject, message, sender, [highest_bidder_email])
                print(f"Notification sent to {highest_bidder_email} for winning lot {lot.name}")

            lot.is_auction_over = True
            lot.save()
            print(f"Auction for lot {lot_id} has ended. Winner notified and bidding closed.")
        else:
            seller_mail = lot.seller.email
            subject = f'Auction for lot {lot.name} has ended'
            message = f'The auction for lot {lot.name} has ended, but no bids were placed.'
            send_mail(subject, message, sender, [seller_mail])
            print(f"Auction for lot {lot_id} has ended. Notification sent to {seller_mail} for lot {lot.name}. No bids placed.")
        
    except Lot.DoesNotExist:
        print("Lot does not exist")
