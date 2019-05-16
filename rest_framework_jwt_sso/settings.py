from django.conf import settings
from django.test.signals import setting_changed
from rest_framework.settings import APISettings

USER_SETTINGS = getattr(settings, "REST_JWT_SSO", None)

DEFAULTS = {
    "SIGN_SALT": None,
    "SALT_METHOD": "rest_framework_jwt_sso.edjwt.algorithm.DefaultSalt"
}

IMPORT_STRINGS = (
    "SALT_METHOD",
)

api_settings = APISettings(USER_SETTINGS, DEFAULTS, IMPORT_STRINGS)


def reload_api_settings(*args, **kwargs):
    global api_settings
    setting, value = kwargs["setting"], kwargs["value"]
    if setting == "REST_JWT_SSO":
        api_settings = APISettings(value, DEFAULTS, IMPORT_STRINGS)


setting_changed.connect(reload_api_settings)
