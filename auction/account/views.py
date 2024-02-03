from django.shortcuts import render
from account.models import *

def index(request):
    return render(request, 'account/login.html')
