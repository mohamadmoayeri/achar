from abc import ABC, abstractmethod
import logging
import re
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from .error_translation import does_not_exist, blank, required, invalid_choice,\
                               Messages, not_authenticated, method_not_allowed,\
                               not_found, invalid, no_active_account, permission_denied,\
                               not_allowed_to_ask, need_to_login, need_to_id_card,\
                               unique, password_too_short, password_too_common,\
                               password_entirely_numeric, password_too_similar,\
                               need_to_kyc, need_to_national_card, need_to_anonymous,\
                               link_is_wrong, ip_is_locked

from rest_framework.exceptions import ErrorDetail


logger = logging.getLogger(__name__)


def base_exception_handler(exc, context):
    logger.error("Exception occurred", exc_info=True)
    try:
        error_class = eval(exc.__class__.__name__)(exc, context)
    except NameError:
        error_class = Error(exc, context)
    return error_class.result()


class Error(ABC):

    def __init__(self, exc, context):
        self.translate = Messages.translate_to_persian.value
        self.exc = exc
        self.context = context
    
    @property
    def response(self):
        result = exception_handler(self.exc, self.context)
        if type(result.data) == list:
            result.data = {'error': result.data}
        return result

    def result(self):
        response = self.response
        response.data.clear()
        response.data['error'] = eval(self.exc.get_codes())(self.exc.__str__())
        return response


class ValidationError(Error):

    def pretify(self, response):
        for i in response.data.keys():
            if type(response.data[i]) == list:
                response.data[i] = response.data[i][0]
        return response

    def result(self):
        self.check_response()
        res = self.pretify(self.response)
        return res
    
    def check_response(self):
        for i in self.response.data.items():
            if not i[1][0].code.startswith("translated"):
                self.response.data[i[0]] = eval(i[1][0].code)(i[1][0].__str__())


class IntegrityError(Error):

    def result(self):
        detail = str(self.exc)
        error_msg = detail.split()[-1]
        data = {'error': self.translate.get(error_msg, detail.split(":")[0])}
        return Response(data, status=status.HTTP_406_NOT_ACCEPTABLE)


class Http404(Error):

    def result(self):
        detail = self.response.data.get('detail')
        response = self.response
        response.data.clear()
        response.data['error'] = eval(detail.code)(detail.__str__())
        return response

class MethodNotAllowed(Error):
    pass

class NotAuthenticated(Error):
    pass

class PermissionDenied(Error):
    pass

class NeedAllowinToAsk(Error):
    pass

class NeedToLogin(Error):
    pass

class NeedToCertificateRow(Error):
    pass

class TokenError(Error):

     def result(self):
        data = {"error" : self.translate.get(str(self.exc), str(self.exc))}
        return Response(data, status=401)
   

class InvalidToken(Error):

    def result(self):
        detail = self.response.data.pop('detail')
        code = self.response.data.pop('code')
        self.response.data.pop('messages', None)
        error = self.translate.get(code, detail)
        self.response.data.update({'error': error})
        return self.response


class Throttled(Error):
    
    def result(self):
        code = self.exc.get_codes()
        detail = self.response.data.pop('detail')
        time = re.findall(r'\d+', detail)[0]
        self.response.data['error'] = self.translate.get(
            code, detail).format(eval(time))
        return self.response


class DoesNotExist(Error):

    def result(self):
        data = {'error': 'پیدا نشد'}
        return Response(data, status=status.HTTP_404_NOT_FOUND)


class AttributeError(Error):
    pass


class ParseError(Error):
    pass

class AuthenticationFailed(Error):
    pass
class NotAcceptable(Error):
    pass

class UnsupportedMediaType(Error):
    pass
