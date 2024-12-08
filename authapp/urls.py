from django.urls import path

from authapp.apis import SignupApi, SignInApi, RefreshTokenApi, AuthorizedApi

urlpatterns = [
    path("signup/", SignupApi.as_view(), name="signup"),
    path("signin/", SignInApi.as_view(), name="signin"),
    path("authorized-api/", AuthorizedApi.as_view(), name="authorized-api"),
    path("refresh-token/", RefreshTokenApi.as_view(), name="refresh-token"),
]
