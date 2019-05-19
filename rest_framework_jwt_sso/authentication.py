from rest_framework.authentication import BaseAuthentication, get_authorization_header
from django.utils.encoding import smart_text
from django.utils.translation import ugettext
from rest_framework.exceptions import AuthenticationFailed
from jwt.exceptions import *

from rest_framework_jwt_sso.settings import jwt_sso_api_settings
from rest_framework_jwt_sso.utils import decode_jwt


class JWTSSOAuthentication(BaseAuthentication):
    """
    JWT based SSO authentication

    Simple token based authentication.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "JWT_SSO ".  For example:

        Authorization: JWT_SSO eyJ0eXAiOiJKV1QiLCJhbGciOiJFRDUxMiIsImtleSI6IlBjLUUtbmN0WHA3eEg1WVFtamtiQjQ2bzlpY2RfS3lvbHdOZjNlWXBHUVU9In0.eyJzb21lIjoicGF5bG9hZCJ9.LEG43tkDgRJbtWUdANPLYj_KJVygpAjQr1H6Pf3pLwJutIGg0XI88ZDefGmMfSIRqoqMJxSDUoIcN4wrIJpHBQ
    """

    def authenticate(self, request):
        token = get_authorization_header(request).split()
        auth_prefix = self.auth_prefix()

        if not token or smart_text(token[0].lower()) != auth_prefix.lower():
            return None

        if len(token) != 2:
            res = ugettext("Invalid authenticate request structure")
            raise AuthenticationFailed(res)

        try:
            token = token[1].decode()
        except UnicodeError:
            res = ugettext("Invalid token encode")
            raise AuthenticationFailed(res)

        try:
            payload = decode_jwt(token)
        except ExpiredSignature:
            pass
        except DecodeError:
            pass
        except InvalidKeyError:
            pass
        except InvalidTokenError:
            pass

        return None  # TODO: finish credential pass

    @staticmethod
    def auth_prefix():
        return jwt_sso_api_settings.AUTH_TOKEN_PREFIX
