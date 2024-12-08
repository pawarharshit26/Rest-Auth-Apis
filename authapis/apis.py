from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from django.core.exceptions import ValidationError
from authapis.serializers import BaseSerializer

class BaseApi(GenericAPIView):
    input_serializer_class = None
    output_serializer_class = None

    def validate_input_data(self) -> dict:
        serializer = self.input_serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data

    def get_input_serializer(self, data)  -> BaseSerializer:
        if self.input_serializer_class is None:
            raise ValidationError("input_serializer_class is not defined")
        return self.input_serializer_class(data=data)

    def get_output_serializer(self, data) -> BaseSerializer:
        if self.output_serializer_class is None:
            raise ValidationError("output_serializer_class is not defined")
        return self.output_serializer_class(data)
    
    def get_token_payload(self) -> dict|None:
        if hasattr(self.request, "token_payload") and isinstance(
            self.request.token_payload, dict
        ):
            return self.request.token_payload
        return None
    
    def get_rest_token_key(self) -> str:
        token_payload = self.get_token_payload()
        if token_payload and token_payload.get("rest_token"):
            return token_payload.get("rest_token")
        return None


class BaseOpenApi(BaseApi):
    permission_classes = (AllowAny,)
