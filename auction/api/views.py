from rest_framework.response import Response
from rest_framework.decorators import api_view
from lot.models import Lot, Bid
from django.db.models import Max, OuterRef, Subquery, F


@api_view(['GET'])
def user_won_lots(request):
    try:
        # Get the highest bid amount for each lot
        highest_bids = Bid.objects.filter(lot=OuterRef('pk')).values('lot').annotate(max_amount=Max('amount'))
        
        # Retrieve lots where the auction is over and bids are accepted
        won_lots = Lot.objects.filter(is_auction_over=True, bids__accepted=True)

        # Filter lots where the current user has the highest bid
        won_lots = won_lots.annotate(
            highest_bid_amount=Subquery(highest_bids.filter(lot=OuterRef('pk')).values('max_amount')[:1])
        ).filter(
            highest_bid_amount=F('bids__amount'),
            bids__bidder=request.user
        ).distinct()

        data = [{'id': lot.id,
                 'name': lot.name,
                 'slug': lot.slug,
                 'condition': lot.condition,
                 'description': lot.description,
                 'starting_price': lot.starting_price,
                 'buy_it_now_price': lot.buy_it_now_price,
                 'reserve_price': lot.reserve_price,
                 'auction_start_time': lot.auction_start_time,
                 'auction_duration': lot.auction_duration,
                 'scheduled_time': lot.scheduled_time,
                 'quantity': lot.quantity,
                 'is_auction_over': lot.is_auction_over,
                 'is_active': lot.is_active,
                 'created': lot.created,
                 'updated': lot.updated,
                 'category': {'id': lot.category.id, 'name': lot.category.name},
                 'seller': {'id': lot.seller.id, 'name': lot.seller.get_user_full_name()}, 
                 'highest_bid_amount': lot.highest_bid_amount} for lot in won_lots]

        return Response(data)
    except Exception as e:
        print("Error in user won lots", e)
        return Response({'error': str(e)})
