from django.shortcuts import render
from auctionapp.models import *
from django.shortcuts import render
from lot.models import Category, Lot
from django.contrib.auth.decorators import login_required

def index(request):
    categories = Category.objects.all()
    art_category = Category.objects.filter(name="Fine Art").first()
    jwellery_category = Category.objects.filter(name="Jewelry").first()

    furniture_category = Category.objects.filter(name="Furnitures").first()
    context = {
        'jwellery_category': jwellery_category,
        'furniture_category': furniture_category,
        'art_category':art_category,  
        'categories': categories
        }

    return render(request, 'auctionapp/index.html', context)


def lots_based_on_category(request, catgory_slug):
    lots_based_on_category = Category.objects.filter(slug=catgory_slug).first()
    print("---------------------------------")

    print(lots_based_on_category)
    context = {
        'lots_based_on_category':lots_based_on_category,  
        }

    return render(request, 'auctionapp/categories/list.html', context)

@login_required
def favorite_lots(request):
    favorite_lots = request.user.favorite_lots.all()
    return render(request, 'auctionapp/favorite_lots.html', {'favorite_lots': favorite_lots})