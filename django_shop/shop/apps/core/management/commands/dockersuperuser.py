from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

import os

class Command(BaseCommand):


    def handle(self,  **options):
        name = os.environ.get('DOCKER_SUPERUSER_NAME')
        password = os.environ.get('DOCKER_SUPERUSER_PASSWORD')
        email = os.environ.get('DOCKER_SUPERUSER_EMAIL')
        USER = get_user_model()
        if not USER.objects.filter(username=name).exists():
            USER.objects.create_superuser(username=name, password=password, email=email)
            self.stdout.write('SUPERUSER CREATE!')
        else:
            self.stderr.write('SUPERUSER ALREADY EXISTS!')

