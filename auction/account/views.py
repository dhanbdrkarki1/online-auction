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

# User Login
def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')


        print("Hello world-----------------------")

        user_email = CustomUser.objects.filter(email = email).first()
        if not user_email:
            messages.success(request, 'Email not found !')
            return redirect('auctionapp:home')

        # profile_verify = CustomUser.objects.filter(
        #     Q(is_verified = True) & 
        #     Q(email = user_email)
        #     )

        # if not profile_verify:
        #     messages.success(request, 'Your account has not been verified yet..')
        #     return redirect('login')

        user = authenticate(request, email = email, password = password)
        if user is not None:
            if user.is_active:
                login(request, user)
                print(" User logged in..")

                return redirect('auctionapp:home')
            else:
                messages.info(request, 'Your account has been disabled!')

                return redirect('auctionapp:home')
        else:
            print("Your email or password is incorrect!-----------------------")
            messages.info(request, 'Your email or password is incorrect!')
            return redirect('auctionapp:home')
        
    return render(request, 'account/modal/loginModal.html')


# Register User
def register_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        try:
            if CustomUser.objects.filter(email = email).first():
                messages.info(request, 'Email is already taken!')
                return redirect('auctionapp:home')
            
            user_obj = CustomUser.objects.create(email = email, first_name=first_name, last_name=last_name)
            user_obj.set_password(password)
            user_obj.save()
            login(request, user_obj)
            messages.success(request, 'Your account has been created successfully.')
            return redirect('auctionapp:home')

        except Exception as e:
            print(e)

# Logout User
def user_logout(request):
    logout(request)
    return redirect('auctionapp:home')


def user_settings(request):
    return render(request, 'account/settings.html')