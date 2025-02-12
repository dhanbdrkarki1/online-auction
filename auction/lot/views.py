from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from datetime import datetime
from datetime import timedelta
from django.contrib import messages
from .choices import ConditionChoices, DurationChoices, PackageTypeChoices, WeightRangeChoices, CarrierTypeChoices
from django.utils import timezone
from .models import Lot, LotShippingDetails, Category, LotImage, Bid
import json
from django.contrib.humanize.templatetags import humanize
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .tasks import notify_winner_and_close_bidding
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.core import serializers
from django.db.models import Max, OuterRef, Subquery, F
from django.contrib.auth import get_user_model
from reviews.models import SellerReview


User=get_user_model()



def lot_list(request):
    try:
        lots = Lot.objects.filter(seller=request.user)
        context = {
            'lots_list' : lots
        }
        return render(request, "lot/lot/list.html", context)
    except Lot.DoesNotExist as e:
        print(e)


def lot_create(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_type')
        category = Category.objects.get(name=category_name)
        lot_name = request.POST.get('lot_name')
        lot_condition = request.POST.get('lot_condition')
        lot_description = request.POST.get('lot_description')
        auction_duration = request.POST.get('auction_duration')
        scheduled_time = request.POST.get('auction_scheduled_time')
        starting_price = request.POST.get('starting_price')
        buy_it_now_price = request.POST.get('buy_it_now_price')
        reserve_price = request.POST.get('reserve_price')
        quantity = request.POST.get('quantity')
        package_type = request.POST.get('package_type')
        dimensions = f"{request.POST.get('item_length')}x{request.POST.get('item_breadth')}x{request.POST.get('item_height')}"
        package_weight = request.POST.get('package_weight')
        item_location = request.POST.get('item_location')
        shipment_cost = request.POST.get('shipment_cost')
        carrier_type = request.POST.get('carrier_type')
        shipping_notes = request.POST.get('shipping_notes')
        
        current_time = datetime.now()

        if scheduled_time is None:
            auction_start_time = current_time
            scheduled_time = auction_start_time
        else:
            scheduled_time = datetime.strptime(scheduled_time, "%Y/%m/%d %H:%M:%S")
            print("strptime", scheduled_time)
            auction_start_time = scheduled_time
        
        bidding_closing_time = auction_start_time + timedelta(days=int(auction_duration))
        print("bidding closing time", bidding_closing_time)

        starting_price = int(starting_price) if starting_price else None
        buy_it_now_price = int(buy_it_now_price) if buy_it_now_price else None
        reserve_price = int(reserve_price) if reserve_price else None

        try:

            lot = Lot.objects.create(
                category=category,
                seller=request.user,
                name=lot_name,
                condition=lot_condition,
                description=lot_description,
                starting_price=starting_price,
                buy_it_now_price=buy_it_now_price,
                reserve_price=reserve_price,
                auction_start_time=auction_start_time, 
                auction_duration=auction_duration,
                scheduled_time=scheduled_time,
                quantity=quantity
            )
            
            LotShippingDetails.objects.create(
                lot=lot,
                package_type=package_type,
                dimensions=dimensions,
                weight=package_weight,
                item_location=item_location,
                shipment_cost=shipment_cost,
                carrier=carrier_type,
                shipping_notes=shipping_notes
            )

            images = request.FILES.getlist('lot_images')
            print(images)
            for image in images:
                print(image)
                LotImage.objects.create(lot=lot, image=image)
        except Exception as e:
            print(e)

        # Schedule task if auction is scheduled for a future time
        if scheduled_time:
            delay = (bidding_closing_time - current_time).total_seconds()
            print("Delayed by.......", delay)

            # apply_async -> alternative to delay but allow customization like task routing, task expiration time, priority
            notify_winner_and_close_bidding.apply_async(args=[lot.id], countdown=120)
            # notify_winner_and_close_bidding.apply_async(args=[lot.id], countdown=delay)



        # storing lot_id for saving images
        request.session['lot_id'] = lot.pk
        return redirect('lots:lot_received')
    
    context = {
        'lot_condition_choices': [(label, value) for label, value in ConditionChoices.choices],
        'lot_duration_choices': [(label, value) for label, value in DurationChoices.choices],
        'lot_packages_type_choices': [(label, value) for label, value in PackageTypeChoices.choices],
        'lot_weight_range_choices': [(label, value) for label, value in WeightRangeChoices.choices],
        'lot_carrier_type_choices': [(label, value) for label, value in CarrierTypeChoices.choices],
    }
    return render(request, "lot/lot/create.html", context)

def lot_detail(request, slug):
    try:
        lot = get_object_or_404(Lot, slug=slug)
        lot_images = LotImage.objects.filter(lot=lot)
        shipping_details = LotShippingDetails.objects.filter(lot=lot)[0]
        print(shipping_details)
        bids = Bid.objects.filter(lot=lot).order_by('-amount')
        context = {'lot': lot, 'lot_images':lot_images, 'shipping_details':shipping_details, 'bids': bids}
        return render(request, 'lot/lot/detail.html', context)
    except Exception as e:
        print("Error found", e)

def lot_received(request):
    return render(request, 'lot/lot/received.html')


def search_categories(request):
    if request.method == 'GET':
        print("search categories")
        search_query = request.GET.get('search_query', '')
        try:
            categories = Category.objects.filter(name__icontains=search_query)
            categories_dict = [{'id': category.id, 'name': category.name} for category in categories]
            return JsonResponse({'categories': categories_dict})
        except Category.DoesNotExist as e:
            print(e)
            return JsonResponse({}, status=400)

def seller_detail(request, username):
    seller = get_object_or_404(User, username=username)
    try:
        seller_lots = Lot.objects.filter(seller=seller)
        seller_review_count = SellerReview.objects.filter(seller=seller).count()

        context = {
            'seller': seller,
            'seller_lots': seller_lots,
            'seller_review_count': seller_review_count
        }
        return render(request, 'lot/seller/detail.html', context)
    except Lot.DoesNotExist as e:
        print(e)


def place_bid(request, lot_id):
    lot = get_object_or_404(Lot, id=lot_id)
    if request.method == 'POST':
        data = json.loads(request.body)
        bid_amount = data.get('bid_amount')
        print(bid_amount)
        try:
            bid = Bid.objects.create(lot=lot, bidder=request.user, amount=bid_amount)
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'error'})
        return JsonResponse({'status': 'ok'})



def get_latest_bids(request, lot_id):
    lot = get_object_or_404(Lot, id=lot_id)
    try:
        bids = lot.bids.order_by('-amount') 
        bids_count = lot.bids.count()
        print(bids_count)

        # bids data
        data = []
        for bid in bids:
            formatted_bidded_at = humanize.naturaltime(bid.bidded_at)
            formatted_amount = humanize.intcomma(bid.amount)
            data.append({
                'bidder': bid.bidder.get_username_display(),
                'amount': formatted_amount,
                'bidded_at': formatted_bidded_at
            })
        return JsonResponse(data, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse({}, status=400)


def check_bid(request, lot_id):
    lot = get_object_or_404(Lot, id=lot_id)
    
    # Check if there is any bid for the lot
    try:
        bid_exists = Bid.objects.filter(lot=lot).exists()
    
        return JsonResponse({'bid_exists': bid_exists})
    except Bid.DoesNotExist as e:
        print(e)
        return JsonResponse({'status': 'error'})

@login_required
@require_POST
def toggle_favorite(request):
    lot_id = request.POST.get('id')
    action = request.POST.get('action')
    if lot_id and action:
        try:
            lot = Lot.objects.get(pk=lot_id)
            user = request.user
            if action == 'add-to-favourite':
                lot.favorites.add(user)
                print('added')
                return JsonResponse({'status': 'ok'})
            else:
                lot.favorites.remove(user)
                print('remove')

                return JsonResponse({'status': 'ok'})

        except Lot.DoesNotExist:
            return JsonResponse({'status': 'error'})
    else:
        return JsonResponse({'status': 'error'})
    

def sold_lots(request):
    try:
        sold_lots = Lot.objects.filter(is_auction_over=True)
        print("Sold lots########", sold_lots)
        return render(request, 'lot/lot/sold.html', {'sold_lots': sold_lots})
    except Lot.DoesNotExist as e:
        print(e)


def user_bids(request):
    try:
        user_bids = Bid.objects.filter(bidder=request.user).order_by('-bidded_at')
        return render(request, 'lot/lot/bids.html', {'user_bids': user_bids})
    except Bid.DoesNotExist as e:
        print(e)


def user_won_lots(request):
    return render(request, 'lot/lot/won.html')
