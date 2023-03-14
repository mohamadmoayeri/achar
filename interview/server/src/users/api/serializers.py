from users.messages import Messages
from users.models import UserModel
from users.utils import validate_mobile_number, get_client_ip, check_wrong_ip,\
                        check_wrong_mobile_number

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from django.core.cache import cache
from django.contrib.auth import password_validation


class CheckMobileNumberSerializer(serializers.Serializer):
    mobile_number = serializers.SlugField()

    def validate_mobile_number(self, value):
        validate_mobile_number(mobile_number=value)
        return value
    
    def validate(self, attrs):
        mobile_number = attrs['mobile_number']
        check_wrong_mobile_number(mobile_number=mobile_number)
        return attrs
            

class LoginSerializer(serializers.Serializer):
    mobile_number = serializers.SlugField()
    password = serializers.SlugField()

    def validate_mobile_number(self, value):
        validate_mobile_number(mobile_number=value)
        return value
    
    def validate(self, attrs):
        mobile_number = attrs['mobile_number']
        check_wrong_mobile_number(mobile_number=mobile_number)
        return attrs


class VerificationCodeSerializer(serializers.Serializer):
    mobile_number = serializers.SlugField()
    code = serializers.SlugField(write_only=True)

    def validate_mobile_number(self, value):
        validate_mobile_number(mobile_number=value)
        return value

    def validate(self, attrs):
        mobile_number, code = attrs['mobile_number'], attrs['code']
        check_wrong_mobile_number(mobile_number=mobile_number)
        if not cache.has_key(f'code_{mobile_number}'):
            raise ValidationError(
                detail=Messages.NOT_REQUEST_FOR_CODE.value,
                code=f"translated_{ValidationError.default_code}"
            ) 
        self.check_code(mobile_number=mobile_number, code=code)
        return attrs

    def check_code(self, mobile_number, code):
        if not cache.get(f'code_{mobile_number}') == code:
            ip = self.context.get('ip')
            UserModel.lock_ip(ip=ip)
            UserModel.lock_mobile_number(mobile_number=mobile_number)
            raise ValidationError(
                detail=Messages.INCORRECT_CODE.value,
                code=f"translated_{ValidationError.default_code}"
            )
        cache.delete(f'code_{mobile_number}')


class PersonalInformationSerializer(serializers.Serializer):
    mobile_number = serializers.SlugField()
    first_name = serializers.CharField(max_length=50, min_length=3) 
    last_name = serializers.CharField(max_length=50, min_length=3)

    def validate_mobile_number(self, value):
        validate_mobile_number(mobile_number=value)
        return value
    
    def validate(self, attrs):
        mobile_number = attrs['mobile_number']
        check_wrong_mobile_number(mobile_number=mobile_number)
        if not cache.has_key(f'{mobile_number}_status'):
            raise ValidationError(
                detail=Messages.PRE_VERIFY_CODE.value,
                code=f"translated_{ValidationError.default_code}"
            )   
        return attrs
    
class InputPasswordSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = ('mobile_number', 'password')

    def validate(self, attrs):
        mobile_number = attrs['mobile_number']
        check_wrong_mobile_number(mobile_number=mobile_number)
        if not cache.has_key(f'{mobile_number}_info'):
            raise ValidationError(
                detail=Messages.PRE_PERSONAL_INFO.value,
                code=f"translated_{ValidationError.default_code}"
            )   
        return attrs

    def validate_mobile_number(self, value):
        validate_mobile_number(mobile_number=value)
        return value
    
    def validate_password(self, value):
        password_validation.validate_password(value)
        return value
    
    def  create(self, validated_data):
        obj = super().create(validated_data)
        mobile_number = validated_data['mobile_number']
        personal_info = cache.get(f'{mobile_number}_info')
        obj.first_name = personal_info[0]
        obj.last_name = personal_info[1]
        obj.set_password(validated_data['password'])
        obj.save()
        cache.delete_many([f'{mobile_number}_info', f'{mobile_number}_is_verified'])
        return obj
