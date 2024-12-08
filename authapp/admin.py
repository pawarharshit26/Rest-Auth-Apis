from django.contrib import admin, messages
from authapp.models import User
from rest_framework.authtoken.models import Token


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "is_active", "has_token")
    actions = [*admin.ModelAdmin.actions, "revoke_token"]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("auth_token")

    def revoke_token(self, request, queryset):
        user_ids = queryset.values_list("id", flat=True)
        Token.objects.filter(user_id__in=user_ids).delete()
        messages.success(request, "Token Revoked successfully.")

    revoke_token.description = "Revoke token"

    @admin.display(description="Has Token")
    def has_token(self, obj) -> bool:
        if hasattr(obj, "auth_token") and obj.auth_token:
            return True
        return False

