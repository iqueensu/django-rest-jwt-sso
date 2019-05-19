from django.conf import settings
from django.test.signals import setting_changed
from rest_framework.settings import APISettings

USER_SETTINGS = getattr(settings, "REST_JWT_SSO", None)

DEFAULTS = {
    "SIGN_SALT": None,
    "SALT_METHOD": "rest_framework_jwt_sso.edjwt.algorithm.DefaultSalt",
    "AUTH_TOKEN_PREFIX": "JWT_SSO",

    # JWT Claim Settings
    # --Header
    "JWT_CLAIM_ALGORITHM": "alg",
    "JWT_CLAIM_TYPE": "typ",
    "JWT_CLAIM_VALIDATE_KEY": "key",
    # --Payload
    "JWT_CLAIM_ISSUER": "iss",
    "JWT_CLAIM_SUBJECT": "sub",
    "JWT_CLAIM_AUDIENCE": "aud",
    "JWT_CLAIM_EXPIRATION_TIME": "exp",
    "JWT_CLAIM_NOT_BEFORE": "nbf",
    "JWT_CLAIM_ISSUED_AT": "iat",
    "JWT_CLAIM_JWT_ID": "jti",
    "JWT_CLAIM_USER_ID": "uid",
    "JWT_CLAIM_EMAIL": "eml",
}

IMPORT_STRINGS = (
    "SALT_METHOD",
)

jwt_sso_api_settings = APISettings(USER_SETTINGS, DEFAULTS, IMPORT_STRINGS)


def reload_api_settings(*args, **kwargs):
    global jwt_sso_api_settings
    setting, value = kwargs["setting"], kwargs["value"]
    if setting == "REST_JWT_SSO":
        jwt_sso_api_settings = APISettings(value, DEFAULTS, IMPORT_STRINGS)


setting_changed.connect(reload_api_settings)
