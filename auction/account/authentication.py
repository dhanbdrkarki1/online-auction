from account.models import CustomUser

def create_profile(backend, user=None, *args, **kwargs):
    """
    Create user profile for social authentication
    """
    if user is None:
        CustomUser.objects.get_or_create(user=user)
    else:
        # directly confirming email if it is from social auth
        user_obj = CustomUser.objects.get(email=user)
        if not user_obj.is_email_confirmed:
            user_obj.is_email_confirmed  = True
            user_obj.save()
        


