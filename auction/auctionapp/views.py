from django.shortcuts import render
from auctionapp.models import *

def item_list(request):
    return render(request, 'auctionapp/item/list.html')
