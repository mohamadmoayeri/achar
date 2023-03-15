from rest_framework.exceptions import APIException
from rest_framework import status


class NeedToAnonymous(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_code = 'need_to_anonymous'


class BannedIp(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_code = 'ip_is_locked'

