from enum import Enum
from django.utils.translation import gettext_lazy as _

unique_details = {
    "email is being used by another user" : "ایمیل توسط کاربر دیگری استفاده می شود",
    "user with this email already exists." : "کاربر با این ایمیل وجود دارد",
}

invalid_details = {
    "A valid number is required.": ".یک عدد معتبر مورد نیاز است",
    "Enter a valid \"slug\" consisting of letters, numbers, underscores or hyphens.": \
        ".مقدار وارد شده فقط می تواند شامل حروف، اعداد و خط تیره یا خط زیرین باشد",
}

def does_not_exist(detail): return ".این آبجکت وجود ندارد"

def blank(detail): return ".این فیلد نمی تواند خالی باشد"

def required(detail): return ".این فیلد الزامی است"

def invalid_choice(detail):
    choice = detail.split()[0]
    return  "انتخاب معتبری نیست {}".format(eval(choice))

def not_authenticated(detail): return "برای دسترسی به این قسمت باید ابتدا وارد سامانه شوید"

def method_not_allowed(detail): return "مجاز تیست {} متد".format(eval(detail.split()[1]))

def not_found(detail): return ".پیدا نشد"

def unique(detail): return unique_details.get(detail, detail)

def password_too_short(detail): return ".رمز عبور باید حداقل 8 کاراکتر داشته باشد"

def password_too_common(detail): return ".این رمز عبور بسیار رایج است"

def password_entirely_numeric(detail): return ".رمز عبور باید شامل حروف باشد"

def password_too_similar(detail): return ".رمز عبور شما نمی تواند خیلی شبیه سایر اطلاعات شخصی شما باشد."

def invalid(detail): return invalid_details.get(detail, detail)

def no_active_account(detail): return "نام کاربری یا رمز عبور اشتباه می باشد"

def permission_denied(detail): return "شما اجازه انجام این عمل را ندارید"

def not_allowed_to_ask(detail): return "در حال حاضر امکان ثبت درخواست وجود ندارد جند دقیقه بعد دوباره تلاش کنید"

def need_to_login(detail): return "برای دسترسی به این قسمت باید ابتدا وارد سامانه شوید"

def need_to_kyc(detail): return ".برای دسترسی به این قسمت ابتدا باید احراز هویت انجام دهید"

def need_to_id_card(detail): return ".برای دسترسی به این قسمت ابتدا باید احراز هویت کارت شناسایی را انجام دهید"

def need_to_national_card(detail): return ".برای دسترسی به این قسمت ابتدا باید احراز هویت تطبیق چهره و کارت شناسایی را انجام دهید"
    
def need_to_anonymous(detail): return ".برای دسترسی به این قسمت باید از سایت خارج شوید"

def link_is_wrong(detail): return ".لینک معتبر نمی باشد"

class Messages(Enum):
    translate_to_persian = {
        "wallet_foreinaddress.label" : "آدرس دیگری با این نام در سامانه موجود می باشد",
        "wallet_personaladdress.label" : "آدرس دیگری با این نام در سامانه موجود می باشد",
        "wallet_wallet.label" : "آدرس دیگری با این نام در سامانه موجود می باشد",
        "Invalid value.": "مقدار نامعتبر",
        "token_not_valid": "توکن نامعتبر است یا منقضی شده است",
        "throttled": "درخواست مسدود شد انتظار می رود در {} ثانیه در دسترس باشد",
        "valid ObjectId": '{}  معتبر نیست',
        "NOT_AUTHENTICATED": 'شما از سایت خارج شدید برای ورود مجدد لاگین کنید',
        'Token is blacklisted': 'توکن منقضی شده است',
        'Token is invalid or expired': 'توکن نامعتبر است یا منقضی شده است'
    }
  