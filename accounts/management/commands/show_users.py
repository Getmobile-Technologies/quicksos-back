from django.core.management.base import BaseCommand, CommandError
from ...models import Agency, Issue, Question
import json
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Populates the DB with agencies, issues and questions'

    def handle(self, *args, **options):
        users = User.objects.all()
        for i in users:
            print(i.email, i.role)