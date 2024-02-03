from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from uuid import uuid4

User = settings.AUTH_USER_MODEL

class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, phone_number, password):
        if not email:
            raise ValueError(_('The email must be set'))
        
        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            phone_number = phone_number,
        )
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_superuser(self, email, first_name, last_name, phone_number, password):
        user = self.create_user(
            email,
            password = password,
            first_name = first_name,
            last_name = last_name,
            phone_number = phone_number,
        )
        user.is_admin = True
        user.is_verified = True
        user.is_staff =True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    user = models.OneToOneField(User, null=True, blank= True, on_delete=models.CASCADE)
    username = models.CharField(max_length=50, unique=True, null = True)
    first_name = models.CharField(_('first name'),max_length=150)
    last_name = models.CharField(_('last name'),max_length=150)

    email = models.CharField(_('email address'), max_length=150, unique=True)
    email_confirmation = models.BooleanField(default=False)
    phone_number = models.CharField(_('phone number'),max_length=20, null = False)
    phone_number_confirmation = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    is_verified = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager() # setting customer user namanger to the account

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [ 'first_name','last_name', 'phone_number']

    def __str__(self):
        # TypeError: __str__ returned non-string (type NoneType)
        if not self.email:
            return ""
        return self.email
    
    def save(self, *args, **kwargs):
        if not self.username:
            # Auto-generate a random username with "user-" prefix
            self.username = f"user-{str(uuid4())[:8]}"
        super().save(*args, **kwargs)


