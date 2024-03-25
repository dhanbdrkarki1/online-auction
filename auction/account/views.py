from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from account.models import CustomUser
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.http import HttpResponse
from uuid import uuid4
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group
from .decorators import *

# email
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail, BadHeaderError
from django.core.mail import EmailMultiAlternatives
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator

from django.contrib.auth import update_session_auth_hash
from django.utils import timezone

from account.models import *

# User Login
def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        redirect_url = request.GET.get('next')

        # get user detail
        user_email = CustomUser.objects.filter(email = email).first() 
        if not user_email: # checking if mail exist
            messages.error(request, 'Email not found !')
            return redirect('auctionapp:home')
        # verifying user
        user = authenticate(request, email = email, password = password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # if next in url, return to its value page
                if(redirect_url):
                    return redirect(redirect_url)
                return redirect('auctionapp:home')
            else:
                messages.info(request, 'Your account has been disabled!')
                return redirect('auctionapp:home') # redirecting to homepage
        else:
            messages.error(request, 'Your email or password is incorrect!')
            return redirect('auctionapp:home') 
    return render(request, 'account/login.html')


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
        print(request.user.check_password(old_password))
        if not request.user.check_password(old_password):
            return JsonResponse({'status': 'error', 'message': 'The old password is incorrect.'})

        if new_password1 != new_password2:
            return JsonResponse({'status': 'error', 'message': 'The new passwords do not match.'})

        request.user.set_password(new_password1)
        request.user.save()
        update_session_auth_hash(request, request.user)
        return JsonResponse({'status': 'ok', 'message': 'Your password has been chanaged.'})


# Send email verification mail to user
@login_required
def send_verification_email(request):
    try:
        user_obj = get_object_or_404(CustomUser, email=request.user)
        token_string = str(uuid4())
        print(token_string)
        email_confirmation_token = token_string
        user_obj.email_confirmation_token = email_confirmation_token
        # expire token in 12 hours
        user_obj.email_confirmation_token_expiry = timezone.now() + timezone.timedelta(hours=12)
        user_obj.save()

        print(request.META.get('HTTP_HOST'))
        print(request.scheme)
        # sending email
        # email details

        context = {
            'protocol':'https',
            'domain' : request.META.get('HTTP_HOST'),
            'token': email_confirmation_token,
            'site_name': 'Website',
            'user_id': user_obj.pk,
            }
        
        subject = 'Verify Your Email'
        html_message = render_to_string('account/verification_email.html', context)
        msg = strip_tags(html_message)
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [request.user.email]

        try:
            msg = EmailMultiAlternatives(
                subject, 
                msg,
                from_email,
                recipient_list
            )
            msg.attach_alternative(html_message, "text/html")
            msg.send()
            print("email sent-----------------")
        except BadHeaderError:
            return JsonResponse({'status': 'error', 'message': 'Invalid header found.'})
        return JsonResponse({'status': 'ok', 'message': 'We have resent you the email to verify your email address. Check our inbox.'})

    except Exception as e:
        print(e)
        return JsonResponse({'status': 'error', 'message': 'Error in sending verification email.'})



@login_required
def confirm_email(request, user_id, token):
    print("confirm email-------------")
    user_obj = get_object_or_404(CustomUser, id=user_id)
    if str(token) == str(user_obj.email_confirmation_token) and user_obj.email_confirmation_token_expiry > timezone.now():
        user_obj.is_email_confirmed = True
        user_obj.save()
        print("Email confirmed successfully")
        messages.success(request, 'Your email has been verified!')

        return redirect('auctionapp:home')
    elif user_obj.is_email_confirmed:
        messages.info(request, 'Your email has already been verified!')
        return
    else:
        messages.error(request, 'Invalid or confirmation token expired!')
        return





# Logout User
@login_required
def user_logout(request):
    logout(request)
    return redirect('auctionapp:home')


def password_reset_request(request):
    if request.method == 'POST':
        user_email = request.POST.get('email')
        try:
            user_obj = CustomUser.objects.get(email=user_email)
            uid = urlsafe_base64_encode(force_bytes(user_obj.pk))
            protocol = request.scheme
            domain = request.META.get('HTTP_HOST')
            token = default_token_generator.make_token(user_obj)
            site_name = "Bidme"
            context = {
                'protocol': protocol,
                'domain' : domain,
                'token': token,
                'site_name': site_name,
                'user_id': uid,
                }
            
            subject = 'Reset your account password'
            html_message = render_to_string('account/password_mail_template.html', context)
            msg = strip_tags(html_message)
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user_email]

            try:
                msg = EmailMultiAlternatives(
                    subject, 
                    msg,
                    from_email,
                    recipient_list
                )
                msg.attach_alternative(html_message, "text/html")
                msg.send()
                messages.success(request, 'We have sent you the email to reset the password. Check your inbox.')
                return redirect('account:password_reset_sent')

            except BadHeaderError:
                messages.error(request, 'Invalid header found.')
       
        except CustomUser.DoesNotExist:
            messages.error(request, 'The provided email address is not associated with any account.')

        except Exception as e:
            print(e)
            messages.error(request, 'Error in sending password reset mail.')
    return render(request, 'account/forgot_password_form.html')




def password_reset_confirm(request, user_id, token):
    try:
        uid = force_str(urlsafe_base64_decode(user_id))
        print(uid)
        user = CustomUser.objects.get(pk=uid)
        if user is not None and default_token_generator.check_token(user, token):
            if request.method == 'POST':
                new_password = request.POST.get('new_password')
                confirm_password = request.POST.get('confirm_password')
                if new_password != confirm_password:
                    messages.error(request, "Passwords do not match.")
                    return
                else:
                    user.set_password(confirm_password)
                    user.save()
                    messages.success(request, "Password reset successfully.")
                    return redirect('auctionapp:home')

            return render(request, 'account/password_reset_form.html')
        else:
            messages.error(request, "Invalid password reset link.")
    except Exception as e:
        print(e)


def password_reset_sent(request):
    return render(request, 'account/password_reset_sent.html')

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

