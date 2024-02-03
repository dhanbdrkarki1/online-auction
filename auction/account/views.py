from django.shortcuts import render, redirect
from django.db.models import Q
from account.models import CustomUser
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from uuid import uuid4
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm

from account.models import *

def index(request):
    return render(request, 'account/login.html')


def loginUser(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        profile_email = CustomUser.objects.filter(email = email).first()
        if not profile_email:
            messages.success(request, 'Email not found !')
            return redirect('index')

        # profile_verify = CustomUser.objects.filter(
        #     Q(is_verified = True) & 
        #     Q(email = profile_email)
        #     )

        # if not profile_verify:
        #     messages.success(request, 'Your account has not been verified yet..')
        #     return redirect('login')

        user = authenticate(request, email = email, password = password)
        if user is None:
            messages.info(request, 'Password is incorrect...')
            return redirect('auctionapp:home')

        login(request, user)
        return redirect('home')
    return render(request, 'accounts/login.html')

