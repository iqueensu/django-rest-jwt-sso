from jwt.api_jwt import PyJWT
from jwt.exceptions import InvalidTokenError
from jwt.utils import force_unicode
from nacl.signing import VerifyKey, SigningKey
from nacl.encoding import URLSafeBase64Encoder
from rest_framework_jwt_sso.edjwt.algorithm import EdDSA25519Algorithm

try:
    # import required by mypy to perform type checking, not used for normal execution
    from typing import Callable, Dict, List, Optional, Union
except ImportError:
    pass


class EdJWT(PyJWT):
    def __init__(self):
        PyJWT.__init__(self, algorithms=["none"])
        self.register_algorithm(alg_id="ED512", alg_obj=EdDSA25519Algorithm())

    def encode(self,
               payload,  # type: Union[Dict, bytes]
               key=None,  # type: str
               algorithm='ED512',  # type: str
               headers=None,  # type: Optional[Dict]
               json_encoder=None  # type: Optional[Callable]
               ):
        if algorithm != 'ED512':
            return super(EdJWT, self).encode(payload, key, algorithm, headers, json_encoder)

        if key is not None:
            print("Expecting None, Ignoring the Key passed in.")

        alg_obj = self._algorithms["ED512"]
        sign_key = alg_obj.prepare_key(None)
        verify_key = SigningKey(sign_key, encoder=URLSafeBase64Encoder).verify_key.encode(encoder=URLSafeBase64Encoder)

        header = {'key': force_unicode(verify_key)}
        if headers:
            header.update(headers)

        return super(EdJWT, self).encode(payload, "---KEY---" + force_unicode(sign_key), algorithm, header, json_encoder)

    def decode(self,
               jwt,  # type: str
               key=None,   # type: str
               verify=True,  # type: bool
               algorithms=None,  # type: List[str]
               options=None,  # type: Dict
               **kwargs):
        if key is not None:
            return super(EdJWT, self).decode(jwt, key, verify, algorithms, options, **kwargs)
        elif 'key' in self.get_unverified_header(jwt).keys():
            verify_key = self.get_unverified_header(jwt).get('key')
            return super(EdJWT, self).decode(jwt, "---KEY---" + force_unicode(verify_key), verify, algorithms, options, **kwargs)
        else:
            raise InvalidTokenError("JWT is invalid")
