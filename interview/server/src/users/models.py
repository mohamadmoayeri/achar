import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.cache import cache

from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from users.messages import Messages
from users.tasks import send_sms
from users.utils import otp_generate


class UserProfileManager(BaseUserManager):

    def create_user(self, mobile_number, password=None):
        """ Create a new user profile """
        if not mobile_number:
            raise ValueError('User must have an mobile number')

        # mobile_number= self.normalize_email(email)
        user = self.model(mobile_number=mobile_number)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile_number, password):
        """ Create a new superuser profile """
        user = self.create_user(mobile_number, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class UserModel(AbstractUser):
    id = models.UUIDField(_("Id"), default=uuid.uuid4, primary_key=True, unique=True)
    username = models.CharField(_("Username"), max_length=150, null=True, blank=True)
    mobile_number = models.SlugField(_("Mobile_number"), max_length=11, unique=True)
    mobile_is_verified = models.BooleanField(_("Mobile_is_verified"), default=False)
    updated_at = models.DateTimeField(_("Updated_At"), auto_now=True)
    created_at = models.DateTimeField(_("Created_At"), auto_now_add=True)

    USERNAME_FIELD = 'mobile_number'
    objects = UserProfileManager()
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return f'{self.email}'

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }
    
    @staticmethod
    def send_code_to_mobile_number(mobile_number):
        code = otp_generate()
        cache.set(f'code_{mobile_number}', code, 120)
        send_sms.delay(mobile_number, code)

    @staticmethod
    def lock_ip(ip):
        number_of_wrong = 1
        if cache.has_key(f'{ip}_wrong_number'):
            number_of_wrong = cache.get(f'{ip}_wrong_number')
            number_of_wrong += 1
        cache.set(f'{ip}_wrong_number', number_of_wrong, 3600)

    @staticmethod
    def lock_mobile_number(mobile_number):
        number_of_wrong = 1
        if cache.has_key(f'{mobile_number}_wrong_number'):
            number_of_wrong = cache.get(f'{mobile_number}_wrong_number')
            number_of_wrong += 1
        cache.set(f'{mobile_number}_wrong_number', number_of_wrong, 3600)
    
    @staticmethod
    def check_mobile_number(mobile_number):
        if UserModel.objects.filter(mobile_number=mobile_number).exists():
            detail = True
        else:
            UserModel.send_code_to_mobile_number(mobile_number=mobile_number)
            detail = False
        return detail, status.HTTP_200_OK

    def login(self, password, ip):
        validate_password = self.check_password(password)
        if not validate_password:
            UserModel.lock_ip(ip=ip)
            UserModel.lock_mobile_number(self.mobile_number)
            raise ValidationError({'error': Messages.INCORRECT_PASSWORD_OR_MOBILE_NUMBER.value})
        return {
                'refresh': self.tokens()['refresh'],
                'access': self.tokens()['access']
        }, status.HTTP_200_OK
