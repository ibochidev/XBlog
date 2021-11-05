from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from pyfull.validators import PhoneValidator

class UserManager(BaseUserManager):
    def __create_user(self, username, password, *args, **kwargs):
        # username = PhoneValidator.clean(username)
        # if not PhoneValidator.validate(username):
        #     raise ValidationError('Phone Number emas')

        user = User(username=username, **kwargs)
        user.set_password(password)
        user.save()

    def create_user(self, *args, **kwargs):
        kwargs.setdefault('is_staff', False)
        kwargs.setdefault('is_superuser', False)

        if kwargs.get('is_staff') or kwargs.get('is_superuser'):
            raise ValidationError('Error')

        return self.__create_user(*args, **kwargs)


    def create_superuser(self, *args, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)

        if not kwargs.get('is_staff') or not kwargs.get('is_superuser'):
            raise ValidationError('Error')

        return self.__create_user(*args, **kwargs)


class User(AbstractUser):
    objects = UserManager()

    phone = models.CharField(max_length=14, default=None, null=True, unique=True)