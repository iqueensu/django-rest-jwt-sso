from rest_framework_jwt_sso.edjwt.api_edjwt import EdJWT
import time

jwt_api = EdJWT()
res = jwt_api.encode({'some': 'payload'})
print(res)
out = jwt_api.decode(res)
