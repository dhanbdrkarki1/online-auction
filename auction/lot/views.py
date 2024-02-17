from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from datetime import datetime

from .choices import ConditionChoices, DurationChoices, PackageTypeChoices, WeightRangeChoices, CarrierTypeChoices
from django.utils import timezone
from .models import Lot, LotShippingDetails, Category, LotImage

def lot_list(request):
    lots = Lot.objects.all()

    context = {
        'lots_list' : lots
    }
    return render(request, "lot/lot/list.html", context)

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
        
        auction_start_time = None
        if scheduled_time is None:
            scheduled_time = None
            auction_start_time = timezone.now()
        else:
            scheduled_time = datetime.strptime(scheduled_time, "%Y/%m/%d %H:%M:%S")
        starting_price = int(starting_price) if starting_price else None
        buy_it_now_price = int(buy_it_now_price) if buy_it_now_price else None
        reserve_price = int(reserve_price) if reserve_price else None

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
    lot = get_object_or_404(Lot, slug=slug)
    return render(request, 'lot/lot/detail.html', {'lot': lot})

def lot_received(request):
    return render(request, 'lot/lot/received.html')


def search_categories(request):
    if request.method == 'GET':
        print("search categories")
        search_query = request.GET.get('search_query', '')
        categories = Category.objects.filter(name__icontains=search_query)
        categories_dict = [{'id': category.id, 'name': category.name} for category in categories]
        return JsonResponse({'categories': categories_dict})
    return JsonResponse({}, status=400)