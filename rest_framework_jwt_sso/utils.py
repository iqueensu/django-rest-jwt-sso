from rest_framework_jwt_sso.edjwt.api_edjwt import EdJWT


def decode_jwt(token):
    jwt_api = EdJWT()
    # TODO: Finish other checking against token
    return jwt_api.decode(token)
