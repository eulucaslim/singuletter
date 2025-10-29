from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.contrib.auth import get_user_model
from setup.settings import USER_ADMIN


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        post_migrate.connect(create_default_superuser, sender=self)

def create_default_superuser(sender, **kwargs):
    User = get_user_model()
    if not User.objects.filter(username=USER_ADMIN["username"]).exists():
        User.objects.create_superuser(
            username=USER_ADMIN["username"],
            email=USER_ADMIN["email"],
            password=USER_ADMIN["password"]
        )
        print("Superuser created!")