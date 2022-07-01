from django.core.management.base import BaseCommand, CommandError
import json


class Command(BaseCommand):
    help = 'Add firebase cred'


    def handle(self, *args, **options):
        
        with open('quicksos-dev-cred.json', 'r') as f:
            info = json.load(f)
            credentials = json.dumps(info)
            
        with open('.env', 'a') as f:
            f.write(f'\nFIREBASE_CREDENTIALS={credentials}')
            
        
        self.stdout.write('firebase credentials updated')