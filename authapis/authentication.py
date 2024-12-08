from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed


class BearerAuthentication(TokenAuthentication):

    def authenticate(self, request):
        if hasattr(request, "token_payload") and isinstance(
            request.token_payload, dict
        ):
            rest_token_key = request.token_payload.get("rest_token")
            token = (
                Token.objects.filter(key=rest_token_key)
                .select_related("user")
                .first()
            )
            if token is None:
                raise AuthenticationFailed("Your token was expired, please login again.")
            if not token.user.is_active:
                raise AuthenticationFailed("Your account was inactive or deleted. please contact support.")
            return token.user, token
        return None