from django.core.management.base import BaseCommand, CommandError
from ...models import Agency, EmergencyCode, Message, Question
import json
import re
import csv

class Command(BaseCommand):
    help = 'Populates the DB with agencies, issues and questions'

    def handle(self, *args, **options):
        
        messages = Message.objects.all()
        
        for message in messages:
            quest = message.answers.all().first().question
            issue = Question.objects.filter(question__icontains = quest).first().issue
            message.incident = issue
            message.save()
            
        self.stdout.write(self.style.SUCCESS(f'Successfully updated incidents of cases'))