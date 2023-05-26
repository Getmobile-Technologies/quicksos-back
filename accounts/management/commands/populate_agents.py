from django.core.management.base import BaseCommand, CommandError
from ...models import User
import os
import csv

class Command(BaseCommand):
    help = 'Populates the DB with agencies, issues and questions'

    def handle(self, *args, **options):
        # User.objects.all().delete()
        
        with open('user_data.csv', "r") as file:
            csv_file = csv.DictReader(file)
            users = []
            dict_data = []
            for row in csv_file:
                clean_data = {}
                # name = row['\ufeffname'].title().split()
                name = row['name'].title().split()
                
                if len(name)==3:
                    first_name,middle_name,last_name = name
                    clean_data["first_name"] = first_name
                    if middle_name != "":
                        
                        clean_data['last_name'] = f'{middle_name} {last_name}'
                    
                        clean_data['username'] = f'{first_name.lower()}.{middle_name.lower()}.{last_name.lower()}'
                    else:
                        clean_data['last_name'] = last_name
                        clean_data['username'] = f'{first_name.lower()}.{last_name.lower()}'
                    
                else:
                    first_name,last_name = name
                    clean_data["first_name"] = first_name
                    clean_data['last_name'] = last_name
                    clean_data['username'] = f'{first_name.lower()}.{last_name.lower()}'
                    
                
                
                clean_data['phone']= "0" + row["phone"]
                clean_data['email'] = row['email']
                clean_data['password'] = 'Password1'
                # print(clean_data)
                dict_data.append(clean_data)
                users.append(User(**clean_data, role='agent', is_active=True))
            User.objects.bulk_create(users) 
            
            self.stdout.write(self.style.SUCCESS(f'Successfully added {len(users)} users'))
            
            
        with open('agents.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['first_name', 'last_name','username','phone', 'email', 'password'])
            writer.writeheader()
            for data in dict_data:
                writer.writerow(data)