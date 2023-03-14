from enum import Enum
from django.utils.translation import gettext_lazy as _


class Messages(Enum):
    INCORRECT_CODE = _(".کد وارد شده اشتباه می باشد")
    INCORRECT_PASSWORD_OR_MOBILE_NUMBER = _('.رمز عبور یا موبایل اشتباه می باشد')
    INCORRECT_PHONE_NUMBER = _(".شماره موبایل صحیح نیست")
    SEND_CODE = _(".کد تایید برای شما ارسال شد")
    TTL_ERROR = _('{} ثانیه دیگر تلاش کنید ')
    REGISTER_SUCCESSFULL = _(".ثبت نام با موقیت انجام شد")
    PRE_VERIFY_CODE = _("مرحله تایید کد ارسال شده را انجام نداده اید")
    PRE_PERSONAL_INFO = _("مرحله وارد کردن اطلاعات شخصی را انجام نداده اید")
    GET_PERSONAL_INFO = _("اطلاعات شخصی با موفقیت ثبت شد")
    GET_VERIFICATION_CODE = _("کد وارد شده صحیح می باشد")
    NOT_REQUEST_FOR_CODE = _("درخواست ارسال کد را انجام نداده اید")
