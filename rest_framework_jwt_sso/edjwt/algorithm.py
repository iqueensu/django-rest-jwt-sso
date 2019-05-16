from jwt.algorithms import Algorithm
from jwt.exceptions import InvalidKeyError
from jwt.utils import force_unicode

from nacl.utils import random as ran
from nacl.signing import SigningKey, VerifyKey
from nacl.bindings import crypto_sign_SEEDBYTES
from nacl.encoding import URLSafeBase64Encoder
from nacl.exceptions import BadSignatureError

from rest_framework_jwt_sso.settings import api_settings


class EdDSA25519Algorithm(Algorithm):
    def prepare_key(self, key):
        if key is None or key == "":
            return SigningKey(ran(crypto_sign_SEEDBYTES)).encode(encoder=URLSafeBase64Encoder)
        else:
            if force_unicode(key).startswith("---KEY---"):
                return force_unicode(key)[9:]
            else:
                raise InvalidKeyError

    def sign(self, msg, key):
        signing_key = SigningKey(key, encoder=URLSafeBase64Encoder)

        assert issubclass(ADST, SaltMethod)
        msg = ADST.add_salt(msg, b'abcdefg')

        return signing_key.sign(msg).signature

    def verify(self, msg, key, sig):
        verify_key = VerifyKey(key, encoder=URLSafeBase64Encoder)

        assert issubclass(ADST, SaltMethod)
        msg = ADST.add_salt(msg, b'abcdefg')

        try:
            verify_key.verify(msg, sig)
            return True
        except BadSignatureError:
            return False

    @staticmethod
    def to_jwk(key_obj):
        raise NotImplementedError

    @staticmethod
    def from_jwk(jwk):
        raise NotImplementedError


class SaltMethod(object):
    @staticmethod
    def add_salt(msg,  # type: bytes
                 salt,  # type: bytes
                 ):
        """
        Performs everything needed to mix the salt into msg
        :param msg: The source message
        :param salt: Salt from settings
        :return: msg salted
        """
        raise NotImplementedError


class DefaultSalt(SaltMethod):
    @staticmethod
    def add_salt(msg, salt):
        assert isinstance(msg, bytes) and isinstance(salt, bytes), "You have to pass in bytes"
        msg_arr = bytearray(msg)

        out = msg_arr[:int(len(msg) / 2)]
        out.extend(salt)
        out.extend(msg_arr[int(len(msg) / 2):])
        return bytes(out)


ADST = api_settings.SALT_METHOD
