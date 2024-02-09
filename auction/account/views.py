from django.shortcuts import render, redirect
from django.db.models import Q
from account.models import CustomUser
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from uuid import uuid4
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth import update_session_auth_hash
from django.utils import timezone

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
            # must provide backend for multiple authentication backends
            login(request, user_obj,  backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'Your account has been created successfully.')
            return redirect('auctionapp:home')

        except Exception as e:
            print(e)

# Change User Password
@login_required
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('password1')
        new_password2 = request.POST.get('password2')
        print(new_password1, new_password2)
        print("check 1")
        print(request.user.check_password(old_password))
        if not request.user.check_password(old_password):
            print("check 2")

            return JsonResponse({'status': 'error', 'message': 'The old password is incorrect.'})

        if new_password1 != new_password2:
            print("check 3")

            return JsonResponse({'status': 'error', 'message': 'The new passwords do not match.'})

        print("check 4")

        request.user.set_password(new_password1)
        request.user.save()
        update_session_auth_hash(request, request.user)
        print("check 5")

        # Send a success response
        return JsonResponse({'status': 'ok', 'message': 'Your password has been chanaged.'})


# Send email verification mail to user
@login_required
def send_verification_email(request):
    try:
        user_obj = get_object_or_404(CustomUser, user=request.user)

        email_confirmation_token = str(uuid4())
        user_obj.email_confirmation_token = email_confirmation_token
        # expire token in 12 hours
        user_obj.email_confirmation_token_expiry = timezone.now() + timezone.timedelta(hours=12)
        user_obj.save()

        # sending email
        subject = 'Verify Your Email'
        message = render_to_string('account/verification_email.html', {'user': user_obj, 'token': email_confirmation_token})
        from_email = settings.EMAIL_HOST_USER
        print(request.user.email)
        print("Email SEnt----------")
        recipient_list = [request.user.email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        return JsonResponse({'status': 'ok', 'message': 'We have resent you the email to verify your email address.'})

    except Exception as e:
        print(e)
        return JsonResponse({'status': 'error', 'message': 'Error in sending verification email.'})



@login_required
def confirm_email(request, user_id, token):
    user_obj = get_object_or_404(CustomUser, user=request.user)
    if str(token) == str(user_obj.email_confirmation_token) and user_obj.email_confirmation_token_expiry > timezone.now():
        user_obj.is_email_confirmed = True
        user_obj.save()
        print("Email confirmed successfully")
        return redirect('account:home')
    elif user_obj.is_email_confirmed:
        messages.info(request, 'Your email has already been verified!')
        return
    else:
        messages.info(request, 'Invalid or confirmation token expired!')
        return





# Logout User
@login_required
def user_logout(request):
    logout(request)
    return redirect('auctionapp:home')


def user_settings(request):
    return render(request, 'account/settings.html')

@login_required
def profileInfo(request):
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
            return JsonResponse({'status': 'ok', 'message':'Profile updated successfully.'})
        except CustomUser.DoesNotExist as e:
            print(e)
        
        return JsonResponse({'status': 'error', 'message': 'Error submitting profile info!' })
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

            shipping_address_obj, created= ShippingAddress.objects.get_or_create(user=request.user)
            
            shipping_address_obj.first_name = first_name
            shipping_address_obj.last_name = last_name
            shipping_address_obj.country = country
            shipping_address_obj.city = city
            shipping_address_obj.address_line1 = address_line1
            shipping_address_obj.address_line2 = address_line2
            shipping_address_obj.state = state
            shipping_address_obj.postal_code = postal_code

            shipping_address_obj.save()
            return JsonResponse({'status': 'ok', 'message': 'Successfully updated details.' })
        except Exception as e:
            print(e)
        
        return JsonResponse({'status': 'error', 'message': 'Error updating shipping address details!' })
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

