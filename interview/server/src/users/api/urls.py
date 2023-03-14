from rest_framework.routers import DefaultRouter
from users.api.views import AuthenticationViewSet

router = DefaultRouter()
router.register(r'auth', AuthenticationViewSet, basename="auth")