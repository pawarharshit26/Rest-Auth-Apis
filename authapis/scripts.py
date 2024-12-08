from django.conf import settings
from authapp.models import User


def create_superuser():
    print("Superuser creation started")
    if (
        settings.SUPER_USER_NAME
        and settings.SUPER_USER_PASSWORD
    ):
        if not User.objects.filter(username=settings.SUPER_USER_NAME).exists():
            User.objects.create_superuser(
                username=settings.SUPER_USER_NAME,
                email=settings.SUPER_USER_NAME,
                password=settings.SUPER_USER_PASSWORD,
            )
            print("Superuser created")
        else:
            print("Superuser already exists")
    else:
        print(
            "Superuser not created. SUPER_USER_NAME and SUPER_USER_PASSWORD not found in settings"
        )


create_superuser()
