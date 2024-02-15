from django.shortcuts import render
from django.http import JsonResponse
from .models import Category, ConditionChoices

# Create your views here.
def lot_list(request):
    return render(request, "lot/lot/list.html")


def lot_create(request):

    if request.method == 'POST':
        category = request.POST.get('category')
        lot_name = request.POST.get('lot_name')
        lot_condition = request.POST.get('lot_condition')
        lot_description = request.POST.get('lot_description')
        starting_price = request.POST.get('starting_price')
        buy_it_now_price = request.POST.get('buy_it_now_price')
        reserve_price = request.POST.get('reserve_price')
        quantity = request.POST.get('quantity')
        receiver_name = request.POST.get('receiver_name')
        phone_number = request.POST.get('phone_number')
        street_address = request.POST.get('street_address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')
    context = {
        'lot_condition_choices': [(choice.name, choice.value) for choice in ConditionChoices]
    }
    return render(request, "lot/lot/create.html", context)


def lot_received(request):

    return render(request, 'lot/')


def search_categories(request):
    if request.method == 'GET':
        print("search cateogires")
        search_query = request.GET.get('search_query', '')
        categories = Category.objects.filter(name__icontains=search_query)
        categories_list = [category.name for category in categories]
        print("--------\n", categories_list)
        return JsonResponse({'categories': categories_list})
    return JsonResponse({}, status=400)