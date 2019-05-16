from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse

from rest_framework_jwt_sso.edjwt.api_edjwt import EdJWT


import logging

logger = logging.getLogger(__name__)


class ObtainTokenTest(APIView):
    def post(self, request, *args, **kwargs):
        jwt_api = EdJWT()
        res = jwt_api.encode({'some': 'payload'})
        return Response({"token": res})


obtain_token_test = ObtainTokenTest.as_view()
