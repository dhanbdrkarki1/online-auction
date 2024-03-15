from rest_framework.response import Response
from rest_framework.decorators import api_view
from lot.models import Lot, Bid, LotShippingStatus
from payment.models import Transaction
from django.db.models import Max, OuterRef, Subquery, F
from datetime import datetime
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404


@api_view(['GET'])
def paid_lots(request):
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

        # Exclude lots without transactions
        paid_lots = won_lots.exclude(transactions__isnull=True)

        data = []
        for lot in paid_lots:
            data.append({
                'id': lot.id,
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
                'payment_method': lot.transactions.payment_method,
                'shipment_id': lot.shipping_status.id,
                'shipping_status': lot.shipping_status.status,
                'highest_bid_amount': lot.highest_bid_amount
            })

        return Response(data)
    except Exception as e:
        print("Error in retrieving paid lots", e)
        return Response({'error': str(e)})




@api_view(['GET'])
def unpaid_lots(request):
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

        unpaid_lots = won_lots.exclude(transactions__isnull=False)



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
                 'highest_bid_amount': lot.highest_bid_amount} for lot in unpaid_lots]

        return Response(data)
    except Exception as e:
        print("Error in user unpaid lots", e)
        return Response({'error': str(e)})




@api_view(['GET'])
def lot_shipment(request):
    try:
        # Filter transactions where the seller is the current user
        transactions = Transaction.objects.filter(lot__seller=request.user).select_related('lot__shipping_status').all()


        data = []
        for transaction in transactions:
            shipment_status = transaction.lot.shipping_status.status
            payment_method = transaction.payment_method
            lot_name = transaction.lot.name
            shipment_id = transaction.lot.shipping_status.id
            shipping_date = transaction.lot.shipping_status.delivery_date
            data.append({
                'shipment_id': shipment_id,
                'lot_id': transaction.lot.id,
                'slug': transaction.lot.slug,
                'lot_name': lot_name,
                'shipment_status': shipment_status,
                'shipping_date': shipping_date,
                'payment_method': payment_method
            })

        return Response(data)
    except Exception as e:
        print("Error in retrieving shipment list:", e)
        return Response({'error': str(e)})
    

@api_view(['POST'])
def lot_shipment_update(request):
    try:
        shipment_id = request.data.get("shipment_id")
        delivery_date = request.data.get("shipment_date")
        print("Delivery Date", delivery_date)
        shipment_status = request.data.get("shipment_status")
        print(shipment_id, shipment_status)

        shipment_status_obj = LotShippingStatus.objects.get(id=shipment_id)
        print(shipment_status_obj)

        shipment_status_obj.status = shipment_status

        # if none, it is used to Mark as delivered by the buyer
        if delivery_date:
            print(delivery_date)
            delivery_date = datetime.strptime(delivery_date, "%Y/%m/%d %H:%M:%S")
            shipment_status_obj.delivery_date = delivery_date
        print(shipment_status_obj)
        shipment_status_obj.save()

        return Response({'message': 'Shipment status updated successfully'}, status=200)

    except Exception as e:
        return Response({'error': str(e)}, status=400)

