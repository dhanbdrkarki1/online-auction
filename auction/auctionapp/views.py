from django.shortcuts import render
from auctionapp.models import *
from django.shortcuts import render
from lot.models import Category, Lot

def index(request):
    categories = Category.objects.all()
    art_category = Category.objects.filter(name="Fine Art").first()


    return render(request, 'auctionapp/index.html', {'art_category':art_category, 'categories': categories})
