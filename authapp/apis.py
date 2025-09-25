from authapis.apis import BaseApi, BaseOpenApi
from rest_framework import serializers
from authapis.serializers import BaseSerializer
from authapp.services import AuthService
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from silk.profiling.profiler import silk_profile


class SignupApi(BaseOpenApi):
    class InputSerializer(BaseSerializer):
        email = serializers.EmailField(required=True)
        password = serializers.CharField(required=True, min_length=8)

    input_serializer_class = InputSerializer

    @silk_profile(name="SignupApi")
    def post(self, request, *args, **kwargs):
        data = self.validate_input_data()
        try:
            AuthService.signup_new_user(data["email"], data["password"])
        except AuthService.UserAlreadyExistsException as e:
            return Response(
                {"message": e.message},
                status=HTTP_400_BAD_REQUEST,
            )
        except AuthService.AuthServiceException as e:
            return Response(
                {"message": e.message},
                status=HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"message": "User created successfully"},
            status=HTTP_200_OK,
        )


class SignInApi(BaseOpenApi):
    class InputSerializer(BaseSerializer):
        email = serializers.EmailField(required=True)
        password = serializers.CharField(required=True, min_length=8)

    input_serializer_class = InputSerializer

    def post(self, request, *args, **kwargs):
        data = self.validate_input_data()
        try:
            token = AuthService.signin_user(data["email"], data["password"])
        except AuthService.UserDoesNotExistsException as e:
            return Response(
                {"message": e.message},
                status=HTTP_400_BAD_REQUEST,
            )
        except AuthService.WrongPasswordException as e:
            return Response(
                {"message": e.message},
                status=HTTP_400_BAD_REQUEST,
            )
        except AuthService.UserIsInactivatedException as e:
            return Response(
                {"message": e.message},
                status=HTTP_400_BAD_REQUEST,
            )
        except AuthService.AuthServiceException as e:
            return Response(
                {"message": e.message},
                status=HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"token": token, "messsage": "Signin Successful"},
            status=HTTP_200_OK,
        )


class RefreshTokenApi(BaseApi):
    def post(self, request, *args, **kwargs):
        try:
            token = AuthService.refresh_token(self.get_rest_token_key())
        except AuthService.AuthServiceException as e:
            return Response(
                {"message": e.message},
                status=HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"token": token, "message": "Token refreshed successfully"},
            status=HTTP_200_OK,
        )


class AuthorizedApi(BaseApi):
    def get(self, request, *args, **kwargs):
        return Response({"message": "Authenticated api"}, status=HTTP_200_OK)
