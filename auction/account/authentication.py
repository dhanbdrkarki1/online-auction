from account.models import CustomUser

def create_profile(backend, user=None, *args, **kwargs):
    """
    Create user profile for social authentication
    """
    CustomUser.objects.get_or_create(user=user)

