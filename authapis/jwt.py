import jwt
from django.conf import settings
from django.utils import timezone
from authapis.exceptions import BaseException


class JWTService:
    ALGO = "HS256"

    class JWTServiceException(BaseException):
        pass

    class InvalidTokenException(JWTServiceException):
        pass

    @classmethod
    def encode_with_ttl(cls, payload: dict, ttl: int) -> str:
        # ttl is seconds
        payload["exp"] = timezone.now() + timezone.timedelta(seconds=ttl)
        return jwt.encode(payload, settings.SECRET_KEY, algorithm=cls.ALGO)

    @classmethod
    def decode(cls, token: str) -> dict:
        try:
            return jwt.decode(token, settings.SECRET_KEY, algorithms=[cls.ALGO])
        except jwt.ExpiredSignatureError:
            raise cls.InvalidTokenException("Token has expired")
        except jwt.InvalidTokenError:
            raise cls.InvalidTokenException("Invalid token")
        except jwt.InvalidSignatureError:
            raise cls.InvalidTokenException("Invalid token")
        except jwt.PyJWTError:
            raise cls.JWTServiceException("Something went wrong with token")
