from django.shortcuts import render
from django.http import JsonResponse
from .models import Category, ConditionChoices

# Create your views here.
def lot_list(request):
    return render(request, "lot/lot/list.html")


def lot_create(request):
    context = {
        'lot_condition_choices': [(choice.value, choice.value) for choice in ConditionChoices]
    }
    return render(request, "lot/lot/create.html", context)


def search_categories(request):
    if request.method == 'GET':
        print("search cateogires")
        search_query = request.GET.get('search_query', '')
        categories = Category.objects.filter(name__icontains=search_query)
        categories_list = [category.name for category in categories]
        print("--------\n", categories_list)
        return JsonResponse({'categories': categories_list})
    return JsonResponse({}, status=400)