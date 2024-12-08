from django.core.exceptions import ValidationError


class BaseException(ValidationError):
    pass