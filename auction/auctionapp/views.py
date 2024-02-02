from django.shortcuts import render
from auctionapp.models import *

def index(request):
    return render(request, 'auctionapp/index.html')
