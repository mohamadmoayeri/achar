from django.shortcuts import get_object_or_404
from django.core.cache import cache

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from users.api.serializers import CheckMobileNumberSerializer, LoginSerializer,\
                                  VerificationCodeSerializer, PersonalInformationSerializer,\
                                  InputPasswordSerializer
from users.models import UserModel
from users.api.permissions import NotAuthenticatedPermission
from users.messages import Messages
from users.utils import get_client_ip



class AuthenticationViewSet(ViewSet):
    permission_classes = (NotAuthenticatedPermission,)
    #throttle_scope = 'login'

    @swagger_auto_schema(request_body=CheckMobileNumberSerializer,
                         responses={200: openapi.Response('return true or false')})
    @action(detail=False, methods=['post'])
    def check_mobile_number(self, request, *args, **kwargs):
        serializer = CheckMobileNumberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        detail, status = UserModel.check_mobile_number(**serializer.data)
        return Response({'detail': detail}, status=status)

    @swagger_auto_schema(request_body=LoginSerializer,
                         responses={200: openapi.Response("return refresh and access token")})
    @action(detail=False, methods=['post'])
    def login(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ip = get_client_ip(request=request)
        password, mobile_number = request.data['password'], serializer.data['mobile_number']
        user = get_object_or_404(UserModel, mobile_number=mobile_number)
        detail, status = user.login(password=password, ip=ip)
        return Response({'detail': detail}, status=status)
    
    @swagger_auto_schema(request_body=VerificationCodeSerializer,
                         responses={200: openapi.Response(Messages.GET_VERIFICATION_CODE.value)})
    @action(detail=False, methods=['post'])
    def verification_code(self, request, *args, **kwargs):
        ip = get_client_ip(request=request)
        print(ip, 55555555555555555)
        serializer = VerificationCodeSerializer(data=request.data, context={'ip':ip})
        serializer.is_valid(raise_exception=True)
        mobile_number = serializer.data['mobile_number']
        cache.set(f'{mobile_number}_status', 'is_verified')
        return Response({'detail':Messages.GET_VERIFICATION_CODE.value}, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=PersonalInformationSerializer,
                         responses={200: openapi.Response(Messages.GET_PERSONAL_INFO.value)})
    @action(detail=False, methods=['post'])   
    def personal_information(self, request, *args, **kwargs):
        serializer = PersonalInformationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile_number = serializer.data['mobile_number']
        first_name = serializer.data['first_name']
        last_name = serializer.data['last_name']
        cache.set(f'{mobile_number}_info',[first_name, last_name])
        return Response({'detail': Messages.GET_PERSONAL_INFO.value}, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=InputPasswordSerializer,
                         responses={200: openapi.Response(Messages.REGISTER_SUCCESSFULL.value)})
    @action(detail=False, methods=['post'])
    def input_password(self, request, *args, **kwargs):
        serializer = InputPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': Messages.REGISTER_SUCCESSFULL.value}, status=status.HTTP_200_OK)
