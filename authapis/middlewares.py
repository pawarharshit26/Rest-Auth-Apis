from rest_framework.response import Response
from rest_framework.authentication import get_authorization_header

from rest_framework.status import HTTP_401_UNAUTHORIZED
from authapis.jwt import JWTService
from django.http import JsonResponse

class DecodeJWTTokenMiddleware:
    tokenkey = "Bearer"

    def __init__(self, get_response):
        self.get_response = get_response

    @staticmethod
    def process_unauthorised(message):
        return JsonResponse({"message": message}, status=HTTP_401_UNAUTHORIZED)

    def __call__(self, request):
        # Get the jwt token from the request header and attach rest_token to request
        auth_headers = get_authorization_header(request).split()
        if auth_headers:
            if auth_headers[0].decode() != self.tokenkey:
                return self.process_unauthorised("Invalid token")
            elif len(auth_headers) == 1:
                return self.process_unauthorised("Token is missing")
            elif len(auth_headers) > 2:
                return self.process_unauthorised("Invalid token")
            jwt_token = auth_headers[1].decode()
            try:
                token_payload = JWTService.decode(jwt_token)
                setattr(request, "token_payload", token_payload)
            except JWTService.InvalidTokenException as e:
                return self.process_unauthorised("Invalid token")
        return self.get_response(request)
