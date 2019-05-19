from rest_framework_jwt_sso.settings import jwt_sso_api_settings


class Claims(object):
    # Header
    ALGORITHM = jwt_sso_api_settings.JWT_CLAIM_ALGORITHM
    TYPE = jwt_sso_api_settings.JWT_CLAIM_TYPE
    VALIDATE_KEY = jwt_sso_api_settings.JWT_CLAIM_VALIDATE_KEY

    # Payload
    ISSUER = jwt_sso_api_settings.JWT_CLAIM_ISSUER
    SUBJECT = jwt_sso_api_settings.JWT_CLAIM_SUBJECT
    AUDIENCE = jwt_sso_api_settings.JWT_CLAIM_AUDIENCE
    EXPIRATION_TIME = jwt_sso_api_settings.JWT_CLAIM_EXPIRATION_TIME
    NOT_BEFORE = jwt_sso_api_settings.JWT_CLAIM_NOT_BEFORE
    ISSUED_AT = jwt_sso_api_settings.JWT_CLAIM_ISSUED_AT
    JWT_ID = jwt_sso_api_settings.JWT_CLAIM_JWT_ID

    USER_ID = jwt_sso_api_settings.JWT_CLAIM_USER_ID
    EMAIL = jwt_sso_api_settings.JWT_CLAIM_EMAIL
