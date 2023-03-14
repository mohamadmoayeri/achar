import re

from django.core.cache import cache

from rest_framework.exceptions import ValidationError, PermissionDenied
from random import sample

from users.messages import Messages
from reusable.utils import translate_number


def otp_generate():
    chars = '0123456789'
    return ''.join(sample(chars,6))

def validate_mobile_number(mobile_number):
    if not re.match('^09\d{9}$', mobile_number):
        raise ValidationError(Messages.INCORRECT_PHONE_NUMBER.value)
    return True

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def check_wrong_ip(ip):
    number_of_wrong_ip = 0
    if cache.has_key(f'{ip}_wrong_number'):
            number_of_wrong_ip = cache.get(f'{ip}_wrong_number')
    print(number_of_wrong_ip)
    if number_of_wrong_ip >= 3:
        ttl = translate_number(cache.ttl(f'{ip}_wrong_number'))
        raise PermissionDenied({"error" : Messages.TTL_ERROR.value.format(ttl)})
    return True
         
def check_wrong_mobile_number(mobile_number):
    number_of_wrong_mobile_number = 0
    if cache.has_key(f'{mobile_number}_wrong_number'):
            number_of_wrong_mobile_number = cache.get(f'{mobile_number}_wrong_number')
    if number_of_wrong_mobile_number >= 3:
        ttl = translate_number(cache.ttl(f'{mobile_number}_wrong_number'))
        raise PermissionDenied({"error" : Messages.TTL_ERROR.value.format(ttl)})
    return True

