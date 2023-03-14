from rest_framework.permissions import BasePermission
from reusable.permissions import NeedToAnonymous
from users.utils import check_wrong_ip, get_client_ip

class NotAuthenticatedPermission(BasePermission):

    def has_permission(self, request, view):
        if bool(request.user and request.user.is_authenticated):
            raise NeedToAnonymous
        ip = get_client_ip(request=request)
        print(ip, 4444444444444444444444)
        check_wrong_ip(ip=ip)
        return True