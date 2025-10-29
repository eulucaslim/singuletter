from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from dotenv import load_dotenv
import os

class Command(BaseCommand):
    help = 'Create super user case not exists.'

    def handle(self, *args, **options):
        User = get_user_model()
        
        USERNAME = os.getenv('ADMIN_USERNAME')
        EMAIL = os.getenv('ADMIN_EMAIL')
        PASSWORD = os.getenv('ADMIN_PASSWORD')

        if not PASSWORD:
             self.stdout.write(self.style.ERROR('DJANGO_ADMIN_PASSWORD not configurated.'))
             return

        if not User.objects.filter(username=USERNAME).exists():
            self.stdout.write(f"Creating super user -> '{USERNAME}'...")
            
            User.objects.create_superuser(
                username=USERNAME,
                email=EMAIL,
                password=PASSWORD
            )
            
            self.stdout.write(self.style.SUCCESS(f"Super User '{USERNAME}' created!"))
        else:
            self.stdout.write(self.style.WARNING(f"Super User '{USERNAME}' already exists."))