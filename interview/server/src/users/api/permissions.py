from rest_framework.permissions import BasePermission
from reusable.permissions import NeedToAnonymous, BannedIp

from users.utils import check_wrong_ip, get_client_ip
from users.messages import Messages


class NotAuthenticatedPermission(BasePermission):

    def has_permission(self, request, view):
        if bool(request.user and request.user.is_authenticated):
            raise NeedToAnonymous
        ip = get_client_ip(request=request)
        if check_wrong_ip(ip=ip):
            ttl = check_wrong_ip(ip=ip)
            raise BannedIp(detail=Messages.TTL_ERROR.value.format(ttl))
        return True