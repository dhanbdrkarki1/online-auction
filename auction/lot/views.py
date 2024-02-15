from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Category, ConditionChoices

# Create your views here.
def lot_list(request):
    return render(request, "lot/lot/list.html")


def lot_create(request):

    if request.method == 'POST':
        #category
        category = request.POST.get('category_type')

        #lot
        lot_name = request.POST.get('lot_name')
        lot_condition = request.POST.get('lot_condition')
        lot_description = request.POST.get('lot_description')

        # selling
        auction_duration = request.POST.get('auction_duration')
        auction_start_date_time = request.POST.get('auction_start_date_time')
        scheduled_time = request.POST.get('scheduled_time')


        starting_price = request.POST.get('starting_price')
        buy_it_now_price = request.POST.get('buy_it_now_price')
        reserve_price = request.POST.get('reserve_price')
        quantity = request.POST.get('quantity')

        # shipping
       
        return redirect('lots:lot_received')
    context = {
        'lot_condition_choices': [(choice.name, choice.value) for choice in ConditionChoices]
    }
    return render(request, "lot/lot/create.html", context)


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