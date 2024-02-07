from django.shortcuts import render, redirect
from django.db.models import Q
from account.models import CustomUser
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from uuid import uuid4
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import PasswordResetForm
from django.shortcuts import get_object_or_404
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

@login_required
def profileInfo(request):
    print("------profile info-----------")
    if request.method == 'POST':
        print(request.POST)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        print('user email--------------', email, first_name)
        phone_number = request.POST.get('phone_number')
        try:

            profile = CustomUser.objects.get(email=request.user) 
            profile.first_name = first_name
            profile.last_name = last_name
            profile.email = email
            profile.phone_number = phone_number
            profile.save()
            return JsonResponse({'status': 'ok'})
        except CustomUser.DoesNotExist as e:
            print(e)
        
        return JsonResponse({'status': 'error' })
    else:
        user_profile = get_object_or_404(CustomUser,email=request.user)
        context = {
            'first_name': user_profile.first_name,
            'last_name': user_profile.last_name,
            'email': user_profile.email,
            'phone_number': user_profile.phone_number
        }
    return render(request, 'account/settings.html', context)

@login_required
def shippingAddress(request):
    print("---------------Shipping Addresss")
    if request.method == 'POST':
        print(request.POST)
        first_name = request.POST.get('shippingAddressFirstName')
        last_name = request.POST.get('shippingAddressLastName')
        country = request.POST.get('country')
        city = request.POST.get('city')
        address_line1 = request.POST.get('addressLine1')
        address_line2 = request.POST.get('addressLine2')
        state = request.POST.get('state')
        postal_code = request.POST.get('postalCode')
        print(first_name, address_line1)
        # phone_number = request.POST.get('phone_number')
        try:

            print("obj--------------")
            shipping_address_obj, created = ShippingAddress.objects.get_or_create(user=request.user)

            # shipping_address_obj = ShippingAddress.objects.create(user=user_profile.user)
            # shipping_address_obj = get_object_or_404(ShippingAddress, user=user_profile.user)
            print(shipping_address_obj)
            print("gotcha--------------")
            shipping_address_obj.first_name = first_name
            shipping_address_obj.last_name = last_name
            shipping_address_obj.country = country
            shipping_address_obj.city = city
            shipping_address_obj.address_line1 = address_line1
            shipping_address_obj.address_line2 = address_line2
            shipping_address_obj.state = state
            shipping_address_obj.postal_code = postal_code

            print("before saving-----------")
            shipping_address_obj.save()
            print("after saving-----------")

            return JsonResponse({'status': 'ok'})
        except Exception as e:
            print(e)
        
        return JsonResponse({'status': 'error' })
    else:
        user_profile = get_object_or_404(CustomUser,email=request.user)
        shipping_address_obj = get_object_or_404(ShippingAddress, user=request.user)
        if user_profile.first_name is None:
            shipping_address_obj.first_name = user_profile.first_name
        if user_profile.last_name is None:
            shipping_address_obj.last_name = user_profile.last_name
            
        context = {
            'first_name': shipping_address_obj.first_name,
            'last_name': shipping_address_obj.last_name,
            'country': shipping_address_obj.country,
            'city': shipping_address_obj.city,
            'address_line1': shipping_address_obj.address_line1,
            'address_line2': shipping_address_obj.address_line2,
            'state': shipping_address_obj.state,
            'postal_code': shipping_address_obj.postal_code,
        }
        return JsonResponse(context)

    # return render(request, 'account/settings.html', context)


