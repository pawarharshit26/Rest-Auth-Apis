from authapis.exceptions import BaseException
from authapp.models import User
from rest_framework.authtoken.models import Token
from authapis.jwt import JWTService


class AuthService:
    TOKEN_TTL = 60 * 60  # 1 hour

    class AuthServiceException(BaseException):
        pass

    class UserAlreadyExistsException(AuthServiceException):
        pass

    class UserDoesNotExistsException(AuthServiceException):
        pass
    class UserIsInactivatedException(AuthServiceException):
        pass

    class WrongPasswordException(AuthServiceException):
        pass

    @classmethod
    def signup_new_user(cls, email: str, password: str):
        if User.objects.filter(email=email).exists():
            raise cls.UserAlreadyExistsException(f"User already exists with {email}")
        User.objects.create_user(username=email, email=email, password=password)

    @classmethod
    def signin_user(cls, email, password) -> str:
        user = User.objects.filter(email=email).first()
        if user is None:
            raise cls.UserDoesNotExistsException(f"User does not exists with {email}")
        if not user.check_password(password):
            raise cls.WrongPasswordException("Wrong password")
        if user.is_active is False:
            raise cls.UserIsInactivatedException("Your account was inactive or deleted. please contact support.")
        rest_token, _ = Token.objects.get_or_create(user=user)
        jwt_token = JWTService.encode_with_ttl(
            {"rest_token": rest_token.key}, ttl=cls.TOKEN_TTL
        )  # 1 hour expiry
        return jwt_token

    @classmethod
    def refresh_token(cls, rest_token_key: str):
        if not rest_token_key:
            raise cls.AuthServiceException("Token not provided")
        jwt_token = JWTService.encode_with_ttl({"rest_token": rest_token_key}, ttl=cls.TOKEN_TTL)
        return jwt_token
